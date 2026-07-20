"""
Telegram Layer — Owner Snapshot Formatter (GoldBot Core Owner
Snapshot Reporter Alpha, TASK 3; reformatted to v1.1 by the
Operational Intelligence Upgrade, TASK 9).

Pure formatting: turns an OwnerSnapshot into the message text. No
Telegram sending here -- that is telegram/owner/snapshot_sender.py's
job (TASK 4), same "format vs. send" split
telegram/owner/monitoring_commands.py's own report functions already
establish. Every field an honest "N/A" caveat applies to (see
monitoring/snapshot_models.py's own docstring) prints that caveat
directly rather than a fabricated value -- e.g. pipeline duration was
never tracked, so it is never invented here.
"""

from datetime import datetime

from monitoring.snapshot_models import OwnerSnapshot

_STATUS_ICON = {
    "OK": "✅",
    "RUNNING": "✅",
    "ONLINE": "✅",
    "CONNECTED": "✅",
    "SUCCESS": "✅",
    "HEALTHY": "✅",
    "DEGRADED": "⚠️",
    "UNKNOWN": "⚠️",
    "NOT_CONFIGURED": "⚠️",
    "NO_RUNS_TODAY": "⚠️",
    "NO_DATA": "⚠️",
    "REVIEW": "⚠️",
    "OFFLINE": "❌",
    "DOWN": "❌",
}


def _icon(value: str) -> str:
    return _STATUS_ICON.get(value, "❓")


def _format_time(timestamp: str) -> str:
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H:%M UTC")
    except (ValueError, TypeError):
        return timestamp


def format_snapshot(snapshot: OwnerSnapshot) -> str:
    """Never raises: falls back to the snapshot's own field values if formatting fails."""
    overall_icon = "\U0001F7E2" if snapshot.status == "OK" else "\U0001F7E1"
    errors_status = "REVIEW" if snapshot.error_count else "OK"
    database_line_status = "HEALTHY" if snapshot.database_status == "OK" else snapshot.database_status

    lines = [
        f"{overall_icon} GoldBot Snapshot v1.1",
        "⏰ Time:",
        _format_time(snapshot.timestamp),
        "\U0001F5A5 Core:",
        f"{_icon(snapshot.core_status)} {snapshot.core_status}",
        "\U0001F4CA Pipeline:",
        f"Runs Today: {snapshot.pipeline_runs_today}",
        f"Last: {_icon(snapshot.pipeline_last_status)} {snapshot.pipeline_last_status}",
        f"Last At: {_format_time(snapshot.pipeline_last_at) if snapshot.pipeline_last_at else 'N/A'}",
        "Duration: N/A",
        "\U0001F4C8 Market:",
        f"{snapshot.market_symbol} ({snapshot.market_timeframe})",
        f"{snapshot.market_provider}:",
        f"{_icon(snapshot.market_data_status)} {snapshot.market_data_status}",
        "\U0001F3AF Signals:",
        f"Today: {snapshot.signals_today}",
        f"Approved: {snapshot.signals_approved}",
        f"Rejected: {snapshot.signals_rejected}",
        f"Strategies: {snapshot.strategy_breakdown or 'N/A'}",
        "Last Signal:",
        snapshot.last_signal or "N/A",
        f"Score: {snapshot.last_signal_score if snapshot.last_signal_score is not None else 'N/A'}",
        "\U0001F9E0 AI:",
        (
            f"Requests: {snapshot.ai_requests_today}, {_icon(snapshot.ai_status)} {snapshot.ai_status}"
            if snapshot.ai_status != "NO_DATA"
            else "No data collected yet"
        ),
        "⚖️ Decision:",
        f"Total: {snapshot.decision_total}",
        f"Approved: {snapshot.decision_approved}",
        f"Rejected: {snapshot.decision_rejected}",
        f"Avg Confidence: {snapshot.decision_avg_confidence_pct}%",
        f"Risk Pass Rate: {snapshot.decision_risk_pass_rate_pct}%",
        "\U0001F4BE Database:",
        f"Signals: {snapshot.db_signals_total}",
        f"Errors: {snapshot.db_errors_total}",
        f"Pipeline Events: {snapshot.db_pipeline_events_total}",
        f"{_icon(database_line_status)} {database_line_status}",
        "⚠️ Errors:",
        f"Today: {snapshot.error_count}",
        f"Critical: {snapshot.errors_critical}",
        f"Warning: {snapshot.errors_warning}",
        (
            f"Last: {snapshot.last_error_module} @ {_format_time(snapshot.last_error_time)}"
            if snapshot.last_error_module
            else "Last: N/A"
        ),
        f"{_icon(errors_status)} {errors_status}",
        "\U0001F4E1 Telegram:",
        f"{_icon(snapshot.telegram_status)} {snapshot.telegram_status}",
        "Runtime:",
        snapshot.uptime_info,
        f"Next Check: {snapshot.runtime_next_check or 'N/A'}",
    ]
    return "\n".join(lines)
