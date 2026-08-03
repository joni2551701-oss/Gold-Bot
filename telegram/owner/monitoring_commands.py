"""
Telegram Layer — Owner Monitoring Commands (GoldBot Core Owner
Monitoring Alpha, TASK 7; extended by Phase B.0 with `get_performance_report()`
and resource/health lines appended to `get_status_report()`, see
`docs/PHASE_B0_AUDIT.md`). Same "real function, not live-wired until
wired in `telegram/handlers.py`" posture as every other module in
`telegram/owner/` -- see `telegram/owner/provider_commands.py`'s own
docstring for the established convention.

`/health` reuses `telegram.owner.system_commands.get_system_health()`
outright -- a direct, strong match confirmed by
`docs/PHASE_CORE_MONITORING_AUDIT.md` -- no new "full diagnostics"
function is written here. Every other command composes this phase's
own new `monitoring/` modules.

Security (TASK 8): every function here is read-only and produces no
output that itself checks permission -- gating happens once, in
`telegram/commands.py`'s `OWNER_COMMANDS` registration + the existing,
live `telegram.permissions`/`telegram.command_router` gate (see the
audit's own "Security" section for why no new `access_control.py` is
created). Phase B.0's own new surface (`get_performance_report()`, the
resource/health lines) is additionally gated by
`core_layer.health_monitor.access.is_owner_monitoring_enabled()`.
"""

from config import Config
from core_layer.health_monitor.access import is_owner_monitoring_enabled
from decision_layer.decision_logger.decision_logger import DecisionLogger
from core_layer.health_monitor.error_monitor import ErrorMonitor
from core_layer.health_monitor.health_monitor import classify_health
from core_layer.health_monitor.market_monitor import get_market_health
from core_layer.health_monitor.performance_collector import get_counts as get_performance_counts
from core_layer.health_monitor.resource_monitor import get_resource_snapshot
from core_layer.health_monitor.signal_monitor import get_signal_health
from core_layer.health_monitor.system_monitor import get_health as get_system_health_snapshot
from telegram.owner.provider_commands import ProviderCommandResult
from telegram.owner.system_commands import get_system_health
from core_layer.logger.logger import setup_logger

logger = setup_logger("MonitoringCommands")

DEFAULT_SYMBOL = "XAUUSD"


def _format_uptime(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def get_status_report() -> ProviderCommandResult:
    """
    /status -> `core_layer.health_monitor.system_monitor.get_health()`. Never raises:
    the underlying `get_health()` already never raises; this function
    only formats its output. When `enable_owner_monitoring` is on
    (Phase B.0), appends an overall health classification
    (`core_layer.health_monitor.health_monitor.classify_health()`) and a resource
    snapshot line (`core_layer.health_monitor.resource_monitor.get_resource_snapshot()`)
    -- both additive, never replacing the existing lines above.
    """
    try:
        health = get_system_health_snapshot()
        lines = [
            "GoldBot Status",
            f"GoldBot: {health.status}",
            f"Uptime: {_format_uptime(health.uptime_seconds)}",
            f"Last scan: {health.last_scan or 'N/A'}",
            f"Data feed: {health.data_connection}",
            f"Database: {health.database_status}",
        ]
        if health.last_error:
            lines.append(f"Last error: {health.last_error}")

        if is_owner_monitoring_enabled():
            overall = classify_health(health, ErrorMonitor().get_error_counts(hours=24))
            lines.append(f"Overall health: {overall.value}")

            resources = get_resource_snapshot()
            cpu = f"{resources.cpu_time_seconds:.1f}s" if resources.cpu_time_seconds is not None else "N/A"
            ram = f"{resources.max_rss_kb} KB" if resources.max_rss_kb is not None else "N/A"
            lines.append(
                f"Resources: CPU {cpu} | RAM {ram} | Threads {resources.thread_count} | "
                f"Restarts {resources.restart_count} | Heartbeat {resources.heartbeat_at}"
            )

        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_status_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_performance_report() -> ProviderCommandResult:
    """
    /performance -> `core_layer.health_monitor.performance_collector.get_counts()`
    (Phase B.0 TASK 7 -- a pure counter collector, never a computed
    metric; `core_layer.health_monitor.performance.PerformanceTracker`'s own win-rate
    stats are a separate, already-existing concern). Owner-gated by
    `enable_owner_monitoring` (Rule 5) in addition to the live
    OWNER_COMMANDS gate. Never raises.
    """
    try:
        if not is_owner_monitoring_enabled():
            return ProviderCommandResult(success=False, message="Owner monitoring is not enabled.")

        counts = get_performance_counts()
        lines = [
            "Performance Counters",
            f"Signals: {counts.signal_count}",
            f"Decisions: {counts.decision_count}",
            f"Trades: {counts.trade_count}",
            f"Rejects: {counts.reject_count}",
            f"Errors: {counts.error_count}",
            f"Reconnects: {counts.reconnect_count}",
            f"Runtime: {_format_uptime(counts.runtime_seconds)}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_performance_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_health_report() -> ProviderCommandResult:
    """/health -> telegram.owner.system_commands.get_system_health() (reused as-is, per the audit)."""
    return get_system_health()


def get_market_report(symbol: str = DEFAULT_SYMBOL) -> ProviderCommandResult:
    """/market -> `core_layer.health_monitor.market_monitor.get_market_health()` for the configured provider."""
    try:
        health = get_market_health(symbol=symbol, provider_name=Config.MARKET_DATA_PROVIDER)
        lines = [
            f"{health.symbol}",
            f"Price: {health.last_price if health.last_price is not None else 'N/A'}",
            f"Last update: {health.last_update or 'N/A'}",
            f"Data source: {health.data_source_status}",
            f"Latency: {health.latency_ms:.0f} ms" if health.latency_ms is not None else "Latency: N/A",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_market_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_signals_report() -> ProviderCommandResult:
    """/signals -> `core_layer.health_monitor.signal_monitor.get_signal_health()`."""
    try:
        health = get_signal_health()
        lines = [
            "Today",
            f"BUY: {health.buy_count}",
            f"SELL: {health.sell_count}",
            f"NONE: {health.none_count}",
            f"Average confidence: {health.average_confidence * 100:.0f}%",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_signals_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_errors_report(hours: int = 24) -> ProviderCommandResult:
    """/errors -> `core_layer.health_monitor.error_monitor.ErrorMonitor.get_error_counts()`."""
    try:
        counts = ErrorMonitor().get_error_counts(hours=hours)
        lines = [f"Last {hours}h"]
        if not counts:
            lines.append("No errors recorded.")
        else:
            for error_type, count in sorted(counts.items()):
                lines.append(f"{error_type}: {count}")
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_errors_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_pipeline_report(limit: int = 1) -> ProviderCommandResult:
    """/pipeline -> `decision_layer.decision_logger.decision_logger.DecisionLogger.get_recent_entries()` -- most recent decision trace(s)."""
    try:
        entries = DecisionLogger().get_recent_entries(limit=limit)
        if not entries:
            return ProviderCommandResult(success=True, message="No decision pipeline entries recorded yet.")

        blocks = []
        for entry in entries:
            lines = [f"{entry.symbol} | {entry.timeframe}"]
            for criterion in entry.criteria_met:
                lines.append(f"{criterion}: PASS")
            failed_count = entry.criteria_total - len(entry.criteria_met)
            if failed_count > 0:
                lines.append(f"({failed_count} criteria FAIL)")
            lines.append(f"Decision: {entry.decision}")
            if entry.reason:
                lines.append(f"Reason: {entry.reason}")
            blocks.append("\n".join(lines))
        return ProviderCommandResult(success=True, message="\n\n".join(blocks))
    except Exception as e:
        logger.warning(f"get_pipeline_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_daily_report() -> ProviderCommandResult:
    """/report -> a digest composing this phase's own system/signal/error summaries (report_commands.py's own pre-fetch-only functions are not reusable here, per the audit)."""
    try:
        system = get_system_health_snapshot()
        signals = get_signal_health()
        errors = ErrorMonitor().get_error_counts(hours=24)

        lines = [
            "GoldBot Daily Report",
            "",
            "System",
            f"Status: {system.status} (uptime {_format_uptime(system.uptime_seconds)})",
            f"Database: {system.database_status}",
            f"Data feed: {system.data_connection}",
            "",
            "Signals",
            f"BUY: {signals.buy_count}  SELL: {signals.sell_count}  NONE: {signals.none_count}",
            f"Average confidence: {signals.average_confidence * 100:.0f}%",
            "",
            "Errors (24h)",
            str(sum(errors.values())) if errors else "0",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_daily_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
