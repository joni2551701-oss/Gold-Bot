"""
Telegram Layer — Owner Snapshot Formatter (GoldBot Core Owner
Snapshot Reporter Alpha, TASK 3).

Pure formatting: turns an OwnerSnapshot into the message text. No
Telegram sending here -- that is telegram/owner/snapshot_sender.py's
job (TASK 4), same "format vs. send" split
telegram/owner/monitoring_commands.py's own report functions already
establish.
"""

from datetime import datetime

from monitoring.snapshot_models import OwnerSnapshot

_STATUS_ICON = {
    "OK": "✅",
    "RUNNING": "✅",
    "ONLINE": "✅",
    "CONNECTED": "✅",
    "DEGRADED": "⚠️",
    "UNKNOWN": "⚠️",
    "NOT_CONFIGURED": "⚠️",
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
    lines = [
        f"{overall_icon} GoldBot Snapshot",
        "Time:",
        _format_time(snapshot.timestamp),
        "Core:",
        f"{_icon(snapshot.core_status)} {snapshot.core_status}",
        "Database:",
        f"{_icon(snapshot.database_status)} {snapshot.database_status}",
        "Telegram:",
        f"{_icon(snapshot.telegram_status)} {snapshot.telegram_status}",
        "Market Data:",
        f"{_icon(snapshot.market_data_status)} {snapshot.market_data_status}",
        "Signals Today:",
        str(snapshot.signals_today),
        "Last Signal:",
        snapshot.last_signal or "N/A",
        "Errors:",
        str(snapshot.error_count),
        "Runtime:",
        snapshot.uptime_info,
    ]
    return "\n".join(lines)
