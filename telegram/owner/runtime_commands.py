"""
Telegram Layer — Owner Runtime Commands (Phase 61.6: AI Operations &
Reliability Foundation, TASK 6; extended Phase 61.7: AI Platform
Stabilization & Integration, TASK 7/8).

Real, tested, standalone service-shaped functions -- same convention as
every other `telegram/owner/*_commands.py` module (see
`ai_commands.py`'s own docstring): every `ai/runtime` dependency is
injectable, and this module never constructs a live, persistently-
running `AIService` and never reaches into its internals; it formats
already-built `RuntimeManager`/`EventBus`/`RuntimeMetricsCollector`
instances a caller passes in.

Because this codebase's Telegram command handlers construct fresh
objects per call (no live shared state across Telegram commands --
the same posture `ai_cost_handler`'s own empty-dict default already
documents), a command invoked with no injected runtime object reports
a fresh, empty/default state rather than a fabricated one:

    /runtime         -- a fresh RuntimeManager() defaults to READY
                        (RuntimeManager's own documented default)
    /runtime_events  -- a fresh EventBus() has empty history
    /runtime_metrics -- a fresh RuntimeMetricsCollector has zero counts

This is not a bug: these commands are the observability surface for
whichever `RuntimeManager`/`EventBus` a live `AIService` was actually
constructed with. Wiring a persistent, process-wide `AIService`
instance into a running bot process is out of scope for this phase
(Rule 1: Trading Pipeline untouched; Rule 3: no new orchestration
introduced here) -- a future phase can pass that same instance's
`RuntimeManager`/`EventBus`/collector into these functions to make
them reflect real, accumulated state, exactly as `ai_cost_handler`'s
own docstring already promises for its own empty-dict input today.
"""

from typing import Optional

from ai.audit.provider_stats import RuntimeMetricsCollector
from ai.providers.circuit_breaker import ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.runtime.event_bus import EventBus
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_profiles import RuntimeProfile
from ai.runtime.self_check import CheckStatus, RuntimeSelfCheckReport, run_self_check
from core.logger import setup_logger

logger = setup_logger("RuntimeCommands")

_STATUS_ICON = {CheckStatus.PASS: "✓", CheckStatus.WARNING: "⚠", CheckStatus.FAILED: "✗"}


class RuntimeCommandResult:
    """Never raises: every function below returns one of these, matching telegram/owner/provider_commands.py's ProviderCommandResult convention."""

    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def __repr__(self):
        return f"RuntimeCommandResult(success={self.success}, message={self.message!r})"


def runtime_status(runtime_manager: Optional[RuntimeManager] = None) -> RuntimeCommandResult:
    """The /runtime command's payload -- current lifecycle state, health, and how many transitions have been recorded."""
    runtime_manager = runtime_manager or RuntimeManager()

    try:
        state = runtime_manager.current_state()
        message = (
            "AI RUNTIME STATUS\n"
            f"State:\n{state.value}\n"
            f"Healthy:\n{'🟢 Yes' if runtime_manager.is_healthy() else '🔴 No'}\n"
            f"Transitions Recorded:\n{len(runtime_manager.history())}"
        )
        return RuntimeCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"runtime_status failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")


def runtime_events(event_bus: Optional[EventBus] = None, limit: int = 10) -> RuntimeCommandResult:
    """The /runtime_events command's payload -- the `limit` most recent published events, newest first. Never fabricates: an empty history reports 'No events recorded.' rather than a blank panel."""
    event_bus = event_bus or EventBus()

    try:
        recent = list(reversed(event_bus.history()))[:limit]
        if not recent:
            return RuntimeCommandResult(success=True, message="RUNTIME EVENTS\nNo events recorded.")

        lines = [f"{event.occurred_at.isoformat()} — {event.event_type.value} {event.payload}" for event in recent]
        return RuntimeCommandResult(success=True, message="RUNTIME EVENTS\n" + "\n".join(lines))
    except Exception as e:
        logger.warning(f"runtime_events failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")


def runtime_metrics(
    collector: Optional[RuntimeMetricsCollector] = None,
    event_bus: Optional[EventBus] = None,
) -> RuntimeCommandResult:
    """
    The /runtime_metrics command's payload. A `collector` (already
    accumulating counts from a live `EventBus`) is preferred; if
    omitted, a fresh one is attached to `event_bus` (or a fresh
    `EventBus`), which necessarily reports zero counts -- a collector
    only accumulates counts published *after* it subscribes.
    """
    if collector is None:
        event_bus = event_bus or EventBus()
        collector = RuntimeMetricsCollector(event_bus)

    try:
        metrics = collector.snapshot()
        message = (
            "AI RUNTIME METRICS\n"
            f"Requests/min:\n{metrics.requests_per_minute:.1f}\n"
            f"Cache Hits:\n{metrics.cache_hits}\n"
            f"Cache Misses:\n{metrics.cache_misses}\n"
            f"Cache Hit Rate:\n{metrics.cache_hit_rate * 100:.0f}%\n"
            f"Validation Failures:\n{metrics.validation_failures}\n"
            f"Retries:\n{metrics.retries}\n"
            f"Failover Count:\n{metrics.failover_count}"
        )
        return RuntimeCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"runtime_metrics failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")


def runtime_full_status(
    runtime_manager: Optional[RuntimeManager] = None,
    runtime_profile: Optional[RuntimeProfile] = None,
    metrics_collector: Optional[RuntimeMetricsCollector] = None,
    event_bus: Optional[EventBus] = None,
    circuit_breaker: Optional[ProviderCircuitBreaker] = None,
    provider_manager: Optional[ProviderManager] = None,
    health_tracker: Optional[ProviderHealthTracker] = None,
) -> RuntimeCommandResult:
    """
    The `/runtime_status` command's payload (Phase 61.7 TASK 7) -- one
    combined panel over everything `/runtime`, `/runtime_events`, and
    `/runtime_metrics` show separately, plus per-provider circuit
    state (`runtime_status()`/`runtime_events()`/`runtime_metrics()`
    themselves are unchanged -- this is a fourth, composing function,
    same "compose Runtime* objects into an Owner panel" responsibility
    this file already owns). Same fresh-defaults-report-fresh-state
    posture as every function above.
    """
    runtime_manager = runtime_manager or RuntimeManager()
    event_bus = event_bus or EventBus()
    metrics_collector = metrics_collector or RuntimeMetricsCollector(event_bus)
    health_tracker = health_tracker or ProviderHealthTracker()
    circuit_breaker = circuit_breaker or ProviderCircuitBreaker(health_tracker=health_tracker)
    provider_manager = provider_manager or ProviderManager()

    try:
        metrics = metrics_collector.snapshot()
        provider_lines = [
            f"{name.title()} {'🟢' if health_tracker.is_available(name) else '🔴'} {circuit_breaker.state_of(name).value}"
            for name in provider_manager.list_providers()
        ] or ["No providers registered."]

        message = (
            "AI RUNTIME STATUS\n"
            f"State:\n{runtime_manager.current_state().value}\n"
            f"Profile:\n{runtime_profile.name if runtime_profile is not None else 'None (default)'}\n"
            f"Requests/min:\n{metrics.requests_per_minute:.1f}\n"
            "Providers:\n" + "\n".join(provider_lines) + "\n"
            f"Validation Failures:\n{metrics.validation_failures}\n"
            f"Cache Hit Rate:\n{metrics.cache_hit_rate * 100:.0f}%\n"
            f"Failover Count:\n{metrics.failover_count}\n"
            f"Recent Events:\n{len(event_bus.history())}"
        )
        return RuntimeCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"runtime_full_status failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")


def runtime_check(report: Optional[RuntimeSelfCheckReport] = None) -> RuntimeCommandResult:
    """
    The `/runtime_check` command's payload (Phase 61.7 TASK 8) --
    formats an `ai.runtime.self_check.RuntimeSelfCheckReport`. `report`
    is preferred pre-computed (e.g. against a live AIService's own
    components); if omitted, `run_self_check()` is called with every
    default (fresh instances, same fresh-state posture as every other
    function in this file).
    """
    report = report or run_self_check()

    try:
        lines = [f"{_STATUS_ICON[r.status]} {r.name}: {r.status.value} ({r.detail})" for r in report.results]
        message = "AI RUNTIME SELF CHECK\n" + "\n".join(lines) + f"\nOverall:\n{report.overall_status.value}"
        return RuntimeCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"runtime_check failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")
