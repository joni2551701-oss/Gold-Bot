"""
Monitoring Layer — Owner Snapshot Collector (GoldBot Core Owner
Snapshot Reporter Alpha, TASK 2).

Pure aggregation: every field comes from an existing monitoring/*
function or database/signal_repository.py's own get_latest_signal()
-- no new health-check logic is written here (see
docs/PHASE_OWNER_SNAPSHOT_AUDIT.md). Never raises: each source is
read defensively so one failing subsystem degrades its own snapshot
field instead of preventing the rest of the snapshot from being
collected.
"""

from datetime import datetime, timezone
from typing import Optional

from config import Config
from core.logger import setup_logger
from database.signal_repository import SignalRepository
from monitoring.error_monitor import ErrorMonitor
from monitoring.market_monitor import get_market_health
from monitoring.signal_monitor import get_signal_health
from monitoring.snapshot_models import OwnerSnapshot
from monitoring.system_monitor import get_health as get_core_health
from telegram.bot import TelegramBot

logger = setup_logger("SnapshotCollector")

# Same default this phase's Foundation Reuse Audit found already used
# by telegram/owner/monitoring_commands.py's DEFAULT_SYMBOL -- not a
# new convention.
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


def _telegram_status() -> str:
    """
    Reflects whether *this run's own* TelegramBot construction
    succeeded (a valid TELEGRAM_BOT_TOKEN was readable) -- not
    whether the separate, long-running telegram.polling listener is
    up, which this one-shot script has no way to observe. See
    docs/OWNER_SNAPSHOT_REPORTER.md.
    """
    try:
        bot = TelegramBot()
        return "OK" if bot._bot is not None else "NOT_CONFIGURED"
    except Exception as e:
        logger.warning(f"_telegram_status: TelegramBot construction failed: {e}")
        return "NOT_CONFIGURED"


def _last_signal_summary(signal_repository: Optional[SignalRepository] = None) -> Optional[str]:
    try:
        row = (signal_repository or SignalRepository()).get_latest_signal()
    except Exception as e:
        logger.warning(f"_last_signal_summary: get_latest_signal failed: {e}")
        return None
    if not row:
        return None
    direction = row.get("direction", "?")
    created_at = row.get("created_at", "?")
    return f"{direction} @ {created_at}"


def collect_snapshot(
    symbol: str = DEFAULT_SYMBOL,
    provider_name: Optional[str] = None,
    signal_repository: Optional[SignalRepository] = None,
) -> OwnerSnapshot:
    """
    Aggregates the current OwnerSnapshot. Never raises: each source
    below degrades to a safe default on its own failure rather than
    propagating -- this function's whole purpose is to always produce
    a reportable snapshot, even a partially degraded one.
    """
    try:
        core_health = get_core_health()
        core_status = core_health.status
        database_status = core_health.database_status
        uptime_info = _format_uptime(core_health.uptime_seconds)
    except Exception as e:
        logger.warning(f"collect_snapshot: get_core_health failed: {e}")
        core_status = "UNKNOWN"
        database_status = "UNKNOWN"
        uptime_info = "N/A"

    try:
        market_health = get_market_health(
            symbol=symbol,
            provider_name=provider_name or Config.MARKET_DATA_PROVIDER,
        )
        market_data_status = market_health.data_source_status
    except Exception as e:
        logger.warning(f"collect_snapshot: get_market_health failed: {e}")
        market_data_status = "UNKNOWN"

    try:
        error_count = sum(ErrorMonitor().get_error_counts(hours=24).values())
    except Exception as e:
        logger.warning(f"collect_snapshot: get_error_counts failed: {e}")
        error_count = 0

    try:
        signals_today = get_signal_health(signal_repository=signal_repository).total_signals
    except Exception as e:
        logger.warning(f"collect_snapshot: get_signal_health failed: {e}")
        signals_today = 0

    telegram_status = _telegram_status()
    last_signal = _last_signal_summary(signal_repository)

    status = "OK" if core_status == "RUNNING" and database_status == "OK" else "DEGRADED"

    return OwnerSnapshot(
        timestamp=datetime.now(timezone.utc).isoformat(),
        status=status,
        core_status=core_status,
        database_status=database_status,
        telegram_status=telegram_status,
        market_data_status=market_data_status,
        last_signal=last_signal,
        error_count=error_count,
        uptime_info=uptime_info,
        signals_today=signals_today,
    )
