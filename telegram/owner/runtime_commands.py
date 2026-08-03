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

from ai.audit.provider_stats import RuntimeMetricsCollector, compute_daily_usage, compute_provider_stats
from ai.audit.response_log import ResponseLog
from ai.providers.circuit_breaker import ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.event_bus import EventBus
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_profiles import RuntimeProfile
from ai.runtime.runtime_state import RuntimeState
from ai.runtime.self_check import CheckStatus, RuntimeSelfCheckReport, run_self_check
from core_layer.logger.logger import setup_logger
from telegram.owner.owner_roles import OwnerRole
from telegram.owner.security import log_owner_action, require_role

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
    response_log: Optional[ResponseLog] = None,
    daily_cost_limit: Optional[float] = None,
    daily_token_limit: Optional[int] = None,
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

    Phase 62.2 TASK 10 (Runtime Observability Review): `response_log`/
    `daily_cost_limit`/`daily_token_limit` are new, optional -- the
    audit found the Owner had no visibility into AI Cost Protection
    (Phase 62.2 TASK 8) anywhere, so this existing panel is extended
    in place (Article 7 -- no new monitoring module) with a "Cost
    Protection" line. Omitted `response_log` (the default) reports
    "N/A" honestly rather than fabricating a $0.00 that isn't real
    data, same posture `ai_cost_handler()` already uses for its own
    empty-dict input.
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

        if response_log is None:
            cost_line = "N/A (no response_log injected)"
        else:
            usage = compute_daily_usage(response_log.all())
            cost_limit_text = f"${daily_cost_limit:.2f}" if daily_cost_limit is not None else "none"
            token_limit_text = str(daily_token_limit) if daily_token_limit is not None else "none"
            cost_line = f"${usage.total_cost:.2f} / limit {cost_limit_text}, {usage.total_tokens} tokens / limit {token_limit_text}"

        message = (
            "AI RUNTIME STATUS\n"
            f"State:\n{runtime_manager.current_state().value}\n"
            f"Profile:\n{runtime_profile.name if runtime_profile is not None else 'None (default)'}\n"
            f"Requests/min:\n{metrics.requests_per_minute:.1f}\n"
            "Providers:\n" + "\n".join(provider_lines) + "\n"
            f"Validation Failures:\n{metrics.validation_failures}\n"
            f"Cache Hit Rate:\n{metrics.cache_hit_rate * 100:.0f}%\n"
            f"Failover Count:\n{metrics.failover_count}\n"
            f"Recent Events:\n{len(event_bus.history())}\n"
            f"Cost Protection (24h):\n{cost_line}"
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


def runtime_restart(
    telegram_id: str,
    runtime_manager: Optional[RuntimeManager] = None,
    audit_log_repository=None,
) -> RuntimeCommandResult:
    """
    The `/runtime_restart` command's payload (Phase 62.2 TASK 7). Flow:
    Permission -> Audit -> transition -> Result, Owner-only
    (`require_role(telegram_id, OwnerRole.OWNER)`).

    "Restart" means "force the runtime back to READY," not a literal
    shutdown-then-initialize two-step: `ai.runtime.runtime_state.
    VALID_TRANSITIONS` (Phase 61.6, exhaustively verified by the
    36-pair matrix in `tests/ai/runtime/test_runtime_state_matrix.py`)
    makes `SHUTDOWN` terminal by design -- no outgoing edge exists, and
    this phase does not touch that already-tested state machine
    (Constitution Article 7 / `CLAUDE.md`'s "no unnecessary refactor").
    `FAILED`/`DEGRADED`/`BUSY`/`INITIALIZING` -> `READY` are all valid,
    single-step transitions -- exactly what "restart" means for a
    stuck-but-not-terminated runtime. A runtime already `SHUTDOWN`
    cannot be restarted by this command; reported honestly as a
    rejection, not silently faked as a success.
    """
    security = require_role(telegram_id, OwnerRole.OWNER)
    if not security.allowed:
        return RuntimeCommandResult(success=False, message=f"Permission denied: {security.reason}")

    runtime_manager = runtime_manager or RuntimeManager()

    try:
        previous_state = runtime_manager.current_state()

        if previous_state == RuntimeState.READY:
            log_owner_action(
                str(telegram_id), "runtime_restart", target="ai_runtime",
                result="SUCCESS", details="already READY -- no-op", audit_log_repository=audit_log_repository,
            )
            return RuntimeCommandResult(success=True, message="AI Runtime already READY -- no restart needed.")

        if previous_state == RuntimeState.SHUTDOWN:
            log_owner_action(
                str(telegram_id), "runtime_restart", target="ai_runtime",
                result="REJECTED", details="runtime is SHUTDOWN (terminal)", audit_log_repository=audit_log_repository,
            )
            return RuntimeCommandResult(success=False, message="Cannot restart: runtime is SHUTDOWN (terminal state).")

        event = runtime_manager.transition(RuntimeState.READY, reason="owner restart")
        if event is None:
            log_owner_action(
                str(telegram_id), "runtime_restart", target="ai_runtime", result="FAILED",
                details=f"invalid transition from {previous_state.value}", audit_log_repository=audit_log_repository,
            )
            return RuntimeCommandResult(success=False, message=f"Restart failed: invalid transition from {previous_state.value}.")

        log_owner_action(
            str(telegram_id), "runtime_restart", target="ai_runtime", result="SUCCESS",
            details=f"{previous_state.value} -> READY", audit_log_repository=audit_log_repository,
        )
        return RuntimeCommandResult(success=True, message=f"AI Runtime restarted.\n{previous_state.value} -> READY")
    except Exception as e:
        logger.warning(f"runtime_restart failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")


def runtime_provider(
    provider_name: str,
    health_tracker: Optional[ProviderHealthTracker] = None,
    circuit_breaker: Optional[ProviderCircuitBreaker] = None,
    response_log: Optional[ResponseLog] = None,
) -> RuntimeCommandResult:
    """
    The `/runtime_provider` command's payload (Phase 62.2 TASK 7) -- the
    Director's own worked panel (Provider/Health/Circuit/Latency/
    Requests) for one named provider. Same fresh-defaults-report-fresh-
    state posture as every other function in this file; `response_log`
    (unmodified `ai.audit.response_log.ResponseLog`) is the same source
    `ai.audit.provider_stats.compute_provider_stats()` already reads
    for `/runtime_status` and Owner AI dashboards -- no new metrics
    store.
    """
    health_tracker = health_tracker or ProviderHealthTracker()
    circuit_breaker = circuit_breaker or ProviderCircuitBreaker(health_tracker=health_tracker)
    response_log = response_log or ResponseLog()

    try:
        status = health_tracker.status_of(provider_name)
        if status is None:
            return RuntimeCommandResult(success=False, message=f"Unknown provider: {provider_name}")

        stats = compute_provider_stats(response_log.all()).get(provider_name)
        latency_line = f"{stats.avg_latency_ms:.0f} ms" if stats is not None else "N/A"
        requests_line = str(stats.total_calls) if stats is not None else "0"

        message = (
            "AI PROVIDER STATUS\n"
            f"Provider:\n{provider_name.title()}\n"
            f"Health:\n{status.value}\n"
            f"Circuit:\n{circuit_breaker.state_of(provider_name).value}\n"
            f"Latency:\n{latency_line}\n"
            f"Requests:\n{requests_line}"
        )
        return RuntimeCommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"runtime_provider failed: {e}")
        return RuntimeCommandResult(success=False, message=f"Error: {e}")
