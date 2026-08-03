"""
AI Layer — Provider Circuit Breaker (Phase 61.6: AI Operations &
Reliability Foundation, TASK 3).

**Rule 4 is decisive**: "Provider holati faqat ProviderManager /
ProviderHealth" (provider state lives only in ProviderManager /
ProviderHealth) -- this module introduces no third "is this provider
available" store. `CLOSED`/`OPEN`/`HALF_OPEN` are breaker-internal
bookkeeping (a failure count and the timestamp a circuit opened, per
provider name) used only to *decide* a transition; the moment a
transition happens, this module writes the result into the existing
`ai.providers.provider_health.ProviderHealthTracker` -- the single
source of truth `ai.router.router.AIRouter.route()` already reads via
`ProviderHealthTracker.is_available()`. **`ai/router/router.py` is not
modified this phase** -- "Router faqat healthy provider ishlatadi"
(the router only uses healthy providers) already holds today, for
free, because the breaker speaks the router's existing language.

State mapping into `HealthStatus` (`ai.providers.provider_status`):
    OPEN       -> HealthStatus.OFFLINE   (not in AVAILABLE_STATUSES -- no request reaches this provider)
    HALF_OPEN  -> HealthStatus.DEGRADED  (in AVAILABLE_STATUSES -- exactly the one probe request is allowed through)
    CLOSED     -> HealthStatus.ONLINE    (fully recovered)

Worked example (the Director's own): Gemini times out 5 times ->
`record_failure()` reaches `failure_threshold` -> circuit opens ->
`ProviderHealthTracker` reports OFFLINE -> 30s elapse ->
`allow_request()` transitions to HALF_OPEN, reports DEGRADED -> the
next `AIService.ask()` attempt is the one probe request -> success
calls `record_success()` -> CLOSED, ONLINE; failure calls
`record_failure()` -> back to OPEN, OFFLINE, and the 30s timer resets.

Phase 61.6 TASK 7: `event_bus` is an optional, injectable dependency
(same convention as every other Phase 61.x constructor) -- when
provided, opening the circuit (`_open()`) publishes the existing
`EventType.PROVIDER_FAILED` with `payload["circuit_state"] = "OPEN"`,
and `record_success()` recovering from OPEN/HALF_OPEN publishes the
existing `EventType.PROVIDER_RECOVERED`. No new event type is added
here -- the Runtime Notification Layer (`telegram/owner/
runtime_notifications.py`) distinguishes a circuit-breaker-driven
"Provider DOWN" alert from a single per-attempt `ai_service.py`
failure by checking for that `circuit_state` payload key.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional

from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_status import HealthStatus
from ai.event_bus import EventBus, EventType, RuntimeEvent
from core_layer.logger.logger import setup_logger

logger = setup_logger("ProviderCircuitBreaker")

DEFAULT_FAILURE_THRESHOLD = 5
DEFAULT_RECOVERY_TIMEOUT_SECONDS = 30


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


@dataclass(frozen=True)
class CircuitBreakerConfig:
    failure_threshold: int = DEFAULT_FAILURE_THRESHOLD
    recovery_timeout_seconds: int = DEFAULT_RECOVERY_TIMEOUT_SECONDS


class ProviderCircuitBreaker:
    """
    One breaker instance covers every provider name (per-name state
    kept internally), same "one tracker, many names" shape
    `ProviderHealthTracker` itself already uses. `health_tracker` is
    injectable (defaults to a fresh `ProviderHealthTracker()`) --
    a caller integrating this with a live `AIService` passes the same
    tracker instance `AIService` already uses, so a breaker transition
    is immediately visible to the router.
    """

    def __init__(
        self,
        health_tracker: Optional[ProviderHealthTracker] = None,
        config: Optional[CircuitBreakerConfig] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._health_tracker = health_tracker or ProviderHealthTracker()
        self._config = config or CircuitBreakerConfig()
        self._event_bus = event_bus or EventBus()
        self._states: Dict[str, CircuitState] = {}
        self._failure_counts: Dict[str, int] = {}
        self._opened_at: Dict[str, datetime] = {}

    def state_of(self, provider_name: str) -> CircuitState:
        """A provider never seen by this breaker is CLOSED -- the optimistic default, same posture ProviderHealthTracker's own constructor uses for a freshly-registered provider."""
        return self._states.get(provider_name, CircuitState.CLOSED)

    def allow_request(self, provider_name: str, now: Optional[datetime] = None) -> bool:
        """
        Whether a request should be attempted against `provider_name`
        right now. CLOSED always allows; OPEN allows only after
        `recovery_timeout_seconds` have elapsed since it opened (and
        transitions to HALF_OPEN when it does, recording that as a
        DEGRADED probe window); HALF_OPEN allows exactly the one
        request already in flight for the probe -- `record_success()`/
        `record_failure()` resolve it. Never raises.
        """
        now = now if now is not None else datetime.now(timezone.utc)
        state = self.state_of(provider_name)

        if state == CircuitState.CLOSED:
            return True

        if state == CircuitState.OPEN:
            opened_at = self._opened_at.get(provider_name)
            if opened_at is not None and (now - opened_at).total_seconds() >= self._config.recovery_timeout_seconds:
                self._states[provider_name] = CircuitState.HALF_OPEN
                self._health_tracker.record(provider_name, HealthStatus.DEGRADED, reason="circuit breaker HALF_OPEN (recovery probe)")
                logger.info(f"Circuit breaker HALF_OPEN: provider={provider_name}")
                return True
            return False

        return True  # HALF_OPEN: allow the single probe through

    def record_success(self, provider_name: str) -> None:
        """Never raises. A success while HALF_OPEN closes the circuit (recovered); a success while CLOSED just resets the failure count. A success while OPEN is impossible via allow_request()'s own gate, but is handled the same as HALF_OPEN defensively -- never raises on an unexpected call order."""
        if self.state_of(provider_name) in (CircuitState.HALF_OPEN, CircuitState.OPEN):
            self._states[provider_name] = CircuitState.CLOSED
            self._opened_at.pop(provider_name, None)
            self._health_tracker.record(provider_name, HealthStatus.ONLINE, reason="circuit breaker CLOSED (recovered)")
            logger.info(f"Circuit breaker CLOSED (recovered): provider={provider_name}")
            self._event_bus.publish(RuntimeEvent(
                event_type=EventType.PROVIDER_RECOVERED,
                payload={"provider_name": provider_name, "circuit_state": "CLOSED"},
            ))
        self._failure_counts[provider_name] = 0

    def record_failure(self, provider_name: str, now: Optional[datetime] = None) -> None:
        """Never raises. A failure while HALF_OPEN immediately re-opens the circuit (the probe failed). A failure while CLOSED increments the count and opens once failure_threshold is reached."""
        now = now if now is not None else datetime.now(timezone.utc)

        if self.state_of(provider_name) == CircuitState.HALF_OPEN:
            self._open(provider_name, now)
            return

        count = self._failure_counts.get(provider_name, 0) + 1
        self._failure_counts[provider_name] = count
        if count >= self._config.failure_threshold:
            self._open(provider_name, now)

    def _open(self, provider_name: str, now: datetime) -> None:
        self._states[provider_name] = CircuitState.OPEN
        self._opened_at[provider_name] = now
        self._failure_counts[provider_name] = 0
        self._health_tracker.record(provider_name, HealthStatus.OFFLINE, reason="circuit breaker OPEN")
        logger.info(f"Circuit breaker OPEN: provider={provider_name}")
        self._event_bus.publish(RuntimeEvent(
            event_type=EventType.PROVIDER_FAILED,
            payload={"provider_name": provider_name, "circuit_state": "OPEN"},
        ))
