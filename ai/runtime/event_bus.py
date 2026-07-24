"""
AI Layer — Runtime Event Bus (Phase 61.6: AI Operations & Reliability
Foundation, TASK 5).

Genuinely new (Module Reuse Principle steps 1/2 both "no" — no
pub/sub mechanism exists anywhere in `ai/` today). Its entire purpose
is decoupling: `ai/runtime/ai_service.py`, `ai/providers/
circuit_breaker.py`, and `ai/runtime/runtime_manager.py` each publish
events about their own state without knowing who (if anyone) is
listening -- "Hech kim bir-birini to'g'ridan-to'g'ri chaqirmaydi" (no
module calls another directly) per the Director's own brief.

The eight event types are exactly the Director's own list -- no extra
event type invented, no event type omitted.

Phase 61.6 TASK 7: one additional event type, `RUNTIME_FAILED`, added
in place (extending this same enum, not a new bus/module) -- the
Runtime Notification Layer's own "Runtime FAILED" alert needs a signal
distinct from `RUNTIME_STOPPED` (a clean, intentional SHUTDOWN, not an
alarming condition). `ai.runtime.runtime_manager.RuntimeManager.
transition()` publishes it the same way it already publishes
`RUNTIME_STARTED`/`RUNTIME_STOPPED` -- one more branch on the same
existing `if/elif` block, no new orchestration logic.

Phase 61.7 TASK 5: two more, `REQUEST_STARTED`/`REQUEST_COMPLETED` --
the Director's own `AI_REQUEST_STARTED`/`AI_REQUEST_COMPLETED`,
renamed to match this enum's existing un-prefixed convention (every
member is already domain-scoped by name alone, e.g. `RUNTIME_STARTED`
not `AI_RUNTIME_STARTED`). `ai.runtime.ai_service.AIService.ask()`
publishes both, bracketing its own existing body -- see that module's
own docstring for the wrapping shape.

Phase 61.7 TASK 7 (Runtime Event Validation, continuation session):
four more.

    REQUEST_FAILED        -- the Director's `AIRequestFailed`. Fires
        alongside REQUEST_COMPLETED (never instead of it -- a rejected
        request still completed, it just didn't succeed) whenever
        `RuntimeResponse.accepted` is False, for any rejection reason
        (runtime unavailable, access denied, capability disabled, no
        provider available, every provider failed, validation
        rejected). One extra `if` in ask()'s existing wrapper, no new
        control flow.
    RUNTIME_STATE_CHANGED -- the Director's `RuntimeStateChanged`. A
        generic "some transition just happened" signal, published
        unconditionally on every valid `RuntimeManager.transition()`
        call, in addition to (not instead of) the existing specific
        RUNTIME_STARTED/RUNTIME_STOPPED/RUNTIME_FAILED publishes for
        callers that only care "did the state change at all," not
        which one.
    RETRY_STARTED/RETRY_COMPLETED -- the Director's own names,
        unchanged. Fire around every attempt after the first inside
        AIService.ask()'s existing provider loop -- the loop already
        tracks `attempted`; `len(attempted) > 1` is exactly "this is a
        retry," reused as the guard rather than adding a new counter.
        RETRY_STARTED fires once a new provider is chosen for a retry
        attempt; RETRY_COMPLETED fires once that attempt's outcome
        (not-implemented / failed / validation-rejected / succeeded)
        is known -- both at points the loop already visits.

"ProviderDown" (the Director's TASK 7 name) is intentionally not a
new, separate event type -- it is `PROVIDER_FAILED` with
`payload["circuit_state"] == "OPEN"`, exactly as already documented in
`ai/providers/circuit_breaker.py` and relied on by
`telegram/owner/runtime_notifications.py`. Renaming the existing
member would break already-tested, already-relied-upon code across
three modules for a cosmetic difference -- Rule 5 (backward
compatibility) settles this in favor of the existing name plus a
documented mapping, not a rename.

Phase 62.2 TASK 6: "PROVIDER_TIMEOUT" (the Director's own name) is
resolved the identical way -- `PROVIDER_FAILED` with
`payload["error_type"] = "TIMEOUT"` (`ai/runtime/ai_service.py`'s own
`_ERROR_TYPE_LABEL` mapping, derived from the exception class
`ai/providers/runtime_errors.py` already raises), not a fifth event
type. A subscriber that only cares about timeouts specifically
filters `PROVIDER_FAILED` events on this payload key, same pattern
`telegram/owner/runtime_notifications.py` already uses for
`circuit_state`.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from core.logger import setup_logger

logger = setup_logger("EventBus")


class EventType(Enum):
    PROVIDER_CHANGED = "ProviderChanged"
    PROVIDER_FAILED = "ProviderFailed"
    PROVIDER_RECOVERED = "ProviderRecovered"
    CACHE_HIT = "CacheHit"
    CACHE_MISS = "CacheMiss"
    VALIDATION_FAILED = "ValidationFailed"
    RUNTIME_STARTED = "RuntimeStarted"
    RUNTIME_STOPPED = "RuntimeStopped"
    RUNTIME_FAILED = "RuntimeFailed"
    REQUEST_STARTED = "RequestStarted"
    REQUEST_COMPLETED = "RequestCompleted"
    REQUEST_FAILED = "RequestFailed"
    RUNTIME_STATE_CHANGED = "RuntimeStateChanged"
    RETRY_STARTED = "RetryStarted"
    RETRY_COMPLETED = "RetryCompleted"


@dataclass(frozen=True)
class RuntimeEvent:
    """payload: free-form, event-type-specific detail (e.g. {"provider_name": "gemini"}) -- never trading data, never a signal/decision object."""
    event_type: EventType
    payload: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """
    In-memory publish/subscribe, same "foundation, no persistence, no
    background thread" posture as every other Phase 61.x manager
    (`ai.session.session_manager.SessionManager`,
    `ai.providers.provider_health.ProviderHealthTracker`). `publish()`
    never raises, even if a subscribed handler does -- one bad
    subscriber must never break the publisher or any other subscriber.
    `history()` keeps every published event in-memory for inspection/
    testing (e.g. `/runtime_events`), same convention
    `core.emergency.emergency_manager.EmergencyManager`'s own
    transition history already uses.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[EventType, List[Callable[[RuntimeEvent], None]]] = {}
        self._history: List[RuntimeEvent] = []

    def subscribe(self, event_type: EventType, handler: Callable[[RuntimeEvent], None]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: RuntimeEvent) -> None:
        self._history.append(event)
        for handler in self._subscribers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as e:
                logger.warning(f"EventBus subscriber failed for {event.event_type.value}: {e}")

    def history(self, event_type: Optional[EventType] = None) -> List[RuntimeEvent]:
        """All published events, oldest first -- optionally filtered to one event_type."""
        if event_type is None:
            return list(self._history)
        return [e for e in self._history if e.event_type == event_type]
