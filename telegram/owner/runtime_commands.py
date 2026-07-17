"""
Telegram Layer — Owner Runtime Commands (Phase 61.6: AI Operations &
Reliability Foundation, TASK 6).

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
from ai.runtime.event_bus import EventBus
from ai.runtime.runtime_manager import RuntimeManager
from core.logger import setup_logger

logger = setup_logger("RuntimeCommands")


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
