"""
AI Layer — Runtime Self Check (Phase 61.7: AI Platform Stabilization &
Integration, TASK 8).

Genuinely new (Module Reuse Principle steps 1/2 both "no" -- nothing in
this codebase runs a single, AI-runtime-scoped reachability sweep
today). Closest precedent is `platform_layer.telegram.owner.dashboard.get_doctor_report()`
(Phase 61.5 Addendum) -- reuses its own "each check independently
wrapped so one failing check never hides the rest, PASS/WARNING/FAILED
never a raised exception" posture, but narrower in scope: seven
AI-runtime-specific subsystems (Provider/Runtime/Validation/Cache/
Audit/EventBus/CircuitBreaker), not `get_doctor_report()`'s whole-bot
sweep (Database/Telegram/Market Data/...).

Every dependency is injectable, same convention as every other Phase
61.x foundation piece -- `run_self_check()` never constructs a live,
persistently-running `AIService`; it accepts already-built component
instances (the same ones a caller would pass to `AIService`'s own
constructor) and reports on their current, already-observable state.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from ai_layer.ai_service.audit.request_log import RequestLog
from ai_layer.ai_service.audit.response_log import ResponseLog
from ai_layer.ai_engine.cache.response_cache import ResponseCache
from ai_layer.ai_engine.providers.circuit_breaker import ProviderCircuitBreaker
from ai_layer.ai_engine.providers.provider_health import ProviderHealthTracker
from ai_layer.ai_engine.providers.provider_manager import ProviderManager
from ai_layer.ai_service.event_bus import EventBus
from ai_layer.ai_engine.runtime.runtime_manager import RuntimeManager
from core_layer.logger.logger import setup_logger

logger = setup_logger("RuntimeSelfCheck")


class CheckStatus(Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAILED = "FAILED"


@dataclass(frozen=True)
class SelfCheckResult:
    name: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True)
class RuntimeSelfCheckReport:
    results: List[SelfCheckResult] = field(default_factory=list)

    @property
    def overall_status(self) -> CheckStatus:
        """FAILED if any check FAILED; else WARNING if any check WARNING; else PASS. Never raises: an empty results list reports PASS -- vacuously, nothing failed."""
        if any(r.status == CheckStatus.FAILED for r in self.results):
            return CheckStatus.FAILED
        if any(r.status == CheckStatus.WARNING for r in self.results):
            return CheckStatus.WARNING
        return CheckStatus.PASS


def _check_provider(provider_manager: ProviderManager, health_tracker: ProviderHealthTracker) -> SelfCheckResult:
    try:
        names = provider_manager.list_providers()
        if not names:
            return SelfCheckResult("Provider", CheckStatus.FAILED, "no providers registered")
        healthy = [name for name in names if health_tracker.is_available(name)]
        if not healthy:
            return SelfCheckResult("Provider", CheckStatus.WARNING, f"{len(names)} registered, none currently healthy")
        return SelfCheckResult("Provider", CheckStatus.PASS, f"{len(healthy)}/{len(names)} healthy")
    except Exception as e:
        logger.warning(f"Provider self-check failed: {e}")
        return SelfCheckResult("Provider", CheckStatus.FAILED, f"error: {e}")


def _check_runtime(runtime_manager: RuntimeManager) -> SelfCheckResult:
    try:
        if runtime_manager.is_healthy():
            return SelfCheckResult("Runtime", CheckStatus.PASS, f"state={runtime_manager.current_state().value}")
        return SelfCheckResult("Runtime", CheckStatus.FAILED, f"state={runtime_manager.current_state().value}")
    except Exception as e:
        logger.warning(f"Runtime self-check failed: {e}")
        return SelfCheckResult("Runtime", CheckStatus.FAILED, f"error: {e}")


def _check_validation() -> SelfCheckResult:
    """Reachability only -- imports and calls validate_response() against a synthetic, always-valid ProviderResult. Never touches a live request."""
    try:
        from ai_layer.ai_engine.providers.base_provider import ProviderResult
        from ai_layer.confidence_ai.response_validator import validate_response

        result = validate_response(ProviderResult(content="self-check probe", metadata={}))
        if result.accepted:
            return SelfCheckResult("Validation", CheckStatus.PASS, "reachable")
        return SelfCheckResult("Validation", CheckStatus.WARNING, f"reachable but rejected a trivial probe: {result.errors}")
    except Exception as e:
        logger.warning(f"Validation self-check failed: {e}")
        return SelfCheckResult("Validation", CheckStatus.FAILED, f"error: {e}")


def _check_cache(response_cache: ResponseCache) -> SelfCheckResult:
    try:
        if not callable(getattr(response_cache, "get", None)):
            return SelfCheckResult("Cache", CheckStatus.FAILED, "response_cache.get is not callable")
        return SelfCheckResult("Cache", CheckStatus.PASS, "reachable")
    except Exception as e:
        logger.warning(f"Cache self-check failed: {e}")
        return SelfCheckResult("Cache", CheckStatus.FAILED, f"error: {e}")


def _check_audit(request_log: RequestLog, response_log: ResponseLog) -> SelfCheckResult:
    try:
        request_count = len(request_log.all())
        response_count = len(response_log.all())
        return SelfCheckResult("Audit", CheckStatus.PASS, f"{request_count} request(s), {response_count} response(s) logged")
    except Exception as e:
        logger.warning(f"Audit self-check failed: {e}")
        return SelfCheckResult("Audit", CheckStatus.FAILED, f"error: {e}")


def _check_event_bus(event_bus: EventBus) -> SelfCheckResult:
    """Reads-only -- never publishes a synthetic probe event, which would pollute a live bus's real history."""
    try:
        count = len(event_bus.history())
        return SelfCheckResult("EventBus", CheckStatus.PASS, f"{count} event(s) in history")
    except Exception as e:
        logger.warning(f"EventBus self-check failed: {e}")
        return SelfCheckResult("EventBus", CheckStatus.FAILED, f"error: {e}")


def _check_circuit_breaker(circuit_breaker: ProviderCircuitBreaker, provider_manager: ProviderManager) -> SelfCheckResult:
    try:
        names = provider_manager.list_providers()
        open_names = [name for name in names if circuit_breaker.state_of(name).value == "OPEN"]
        if open_names:
            return SelfCheckResult("CircuitBreaker", CheckStatus.WARNING, f"OPEN for: {', '.join(open_names)}")
        return SelfCheckResult("CircuitBreaker", CheckStatus.PASS, "no provider circuit is OPEN")
    except Exception as e:
        logger.warning(f"CircuitBreaker self-check failed: {e}")
        return SelfCheckResult("CircuitBreaker", CheckStatus.FAILED, f"error: {e}")


def run_self_check(
    provider_manager: Optional[ProviderManager] = None,
    health_tracker: Optional[ProviderHealthTracker] = None,
    runtime_manager: Optional[RuntimeManager] = None,
    circuit_breaker: Optional[ProviderCircuitBreaker] = None,
    event_bus: Optional[EventBus] = None,
    response_cache: Optional[ResponseCache] = None,
    request_log: Optional[RequestLog] = None,
    response_log: Optional[ResponseLog] = None,
) -> RuntimeSelfCheckReport:
    """
    Never raises: every check below is independently wrapped, so one
    failing check never prevents the rest from running. Every argument
    is optional and defaults to a fresh instance (same convention as
    `ai_layer.ai_engine.runtime.ai_service.AIService`'s own constructor) -- a caller
    integrating this with a live `AIService` passes that same
    instance's own component objects for a report that reflects real,
    accumulated state rather than a fresh, empty one.
    """
    provider_manager = provider_manager or ProviderManager()
    health_tracker = health_tracker or ProviderHealthTracker()
    runtime_manager = runtime_manager or RuntimeManager()
    circuit_breaker = circuit_breaker or ProviderCircuitBreaker(health_tracker=health_tracker)
    event_bus = event_bus or EventBus()
    response_cache = response_cache or ResponseCache()
    request_log = request_log or RequestLog()
    response_log = response_log or ResponseLog()

    results = [
        _check_provider(provider_manager, health_tracker),
        _check_runtime(runtime_manager),
        _check_validation(),
        _check_cache(response_cache),
        _check_audit(request_log, response_log),
        _check_event_bus(event_bus),
        _check_circuit_breaker(circuit_breaker, provider_manager),
    ]
    return RuntimeSelfCheckReport(results=results)
