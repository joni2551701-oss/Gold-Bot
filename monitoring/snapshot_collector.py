"""
Monitoring Layer — Owner Snapshot Collector (GoldBot Core Owner
Snapshot Reporter Alpha, TASK 2; extended by the v1.1 Operational
Intelligence Upgrade, TASK 1-8).

Pure aggregation: every field comes from an existing monitoring/*
function or database/signal_repository.py's own get_latest_signal()
-- no new health-check logic is written here (see
docs/PHASE_OWNER_SNAPSHOT_AUDIT.md, docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md).
Never raises: each source is read defensively so one failing subsystem
degrades its own snapshot field instead of preventing the rest of the
snapshot from being collected.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from config import Config
from core.logger import setup_logger
from database.monitoring_repository import MonitoringRepository
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

# v1.1 TASK 5: the single interval main.py actually configures
# (TradingPipeline(symbol="XAUUSD", interval="M15", ...)) -- reporting
# any other timeframe here would misrepresent what the live pipeline
# does (see docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md's TASK 5 finding).
DEFAULT_TIMEFRAME = "M15"

# v1.1 TASK 8: monitoring_decision_pipeline has no COUNT(*) method and
# no production writer yet (see the v1.1 audit's TASK 1/8 findings) --
# this is a "most recent up to N" proxy for a total, not a true count.
_PIPELINE_EVENTS_SCAN_LIMIT = 1000

# v1.1 TASK 7: matches .github/workflows/owner_snapshot.yml's own
# `cron: "*/15 * * * *"` -- a deterministic computation from the known
# schedule, not a guess.
_SNAPSHOT_INTERVAL_MINUTES = 15


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


def _decision_rows_today(signal_repository: Optional[SignalRepository] = None) -> List[Dict]:
    """Shared source for TASK 1/2/3/8 -- one read of today's `signals` table rows. Never raises: a database failure (or a non-list-like return value) returns an empty list, degrading every dependent field to its own zero/N/A default. Always returns a real list -- never the caller's own iterable/truthiness quirks (e.g. a test double)."""
    try:
        return list((signal_repository or SignalRepository()).get_signals_today())
    except Exception as e:
        logger.warning(f"_decision_rows_today: get_signals_today failed: {e}")
        return []


def _pipeline_activity(rows: List[Dict]):
    """
    v1.1 TASK 1 -- Pipeline Activity. `rows` is today's `signals` table
    rows (a proxy for pipeline cycles that reached the persistence
    stage, not a literal execution count -- see
    docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md's TASK 1 finding). Returns
    (runs_today, last_at, status). Never raises: converts to a real
    list first (rather than trusting `rows`'s own truthiness), which
    also protects against a caller passing something merely
    iterable-looking.
    """
    rows_list = list(rows)
    if not rows_list:
        return 0, None, "NO_RUNS_TODAY"
    latest = max(rows_list, key=lambda r: r.get("created_at") or "")
    return len(rows_list), latest.get("created_at"), "SUCCESS"


def _decision_breakdown(rows: List[Dict]):
    """
    v1.1 TASK 2/3 -- Signal Intelligence + Decision Engine Snapshot,
    both read from the same `rows` (no second dataset exists -- see
    the audit doc). Returns (approved, rejected, strategy_breakdown_text,
    avg_confidence_pct, risk_pass_rate_pct).
    """
    approved = sum(1 for r in rows if r.get("ai_decision") == "APPROVE")
    rejected = sum(1 for r in rows if r.get("ai_decision") in ("REJECT", "NO_TRADE"))

    strategy_counts: Dict[str, int] = {}
    for r in rows:
        name = r.get("strategy_name") or r.get("strategy") or "UNKNOWN"
        short_name = name[:-len("_STRATEGY")] if name.endswith("_STRATEGY") else name
        strategy_counts[short_name] = strategy_counts.get(short_name, 0) + 1
    strategy_breakdown = ", ".join(f"{name}: {count}" for name, count in sorted(strategy_counts.items()))

    confidences = [r.get("confidence_score") for r in rows if isinstance(r.get("confidence_score"), (int, float))]
    avg_confidence_pct = round((sum(confidences) / len(confidences)) * 100, 1) if confidences else 0.0

    passed = sum(1 for r in rows if r.get("risk_status") == "PASSED")
    risk_pass_rate_pct = round((passed / len(rows)) * 100, 1) if rows else 0.0

    return approved, rejected, strategy_breakdown, avg_confidence_pct, risk_pass_rate_pct


def _last_signal_score(signal_repository: Optional[SignalRepository] = None) -> Optional[int]:
    """v1.1 TASK 2 -- confidence_score (0.0-1.0 scale) of the latest signal, as a 0-100 display score. Never raises: any failure or missing row returns None."""
    try:
        row = (signal_repository or SignalRepository()).get_latest_signal()
    except Exception as e:
        logger.warning(f"_last_signal_score: get_latest_signal failed: {e}")
        return None
    if not row:
        return None
    score = row.get("confidence_score")
    return round(score * 100) if isinstance(score, (int, float)) else None


def _error_breakdown(hours: int = 24):
    """v1.1 TASK 6 -- Error Intelligence, aggregated from ErrorMonitor.get_recent_errors()'s already-returned fields. Returns (critical, warning, last_module, last_time)."""
    try:
        events = ErrorMonitor().get_recent_errors(hours=hours)
    except Exception as e:
        logger.warning(f"_error_breakdown: get_recent_errors failed: {e}")
        return 0, 0, None, None

    critical = sum(1 for e in events if e.severity.value == "CRITICAL")
    warning = sum(1 for e in events if e.severity.value == "WARNING")
    if events:
        latest = events[0]  # get_recent_errors() returns newest first
        return critical, warning, latest.module, latest.timestamp
    return critical, warning, None, None


def _pipeline_events_total() -> int:
    """v1.1 TASK 8 -- a 'most recent up to _PIPELINE_EVENTS_SCAN_LIMIT' proxy for a total row count (monitoring_decision_pipeline has no COUNT(*) method). Reads 0 today: no production caller writes this table yet (see the audit doc's TASK 1/8 finding). Never raises."""
    try:
        return len(MonitoringRepository().get_recent_decision_entries(limit=_PIPELINE_EVENTS_SCAN_LIMIT))
    except Exception as e:
        logger.warning(f"_pipeline_events_total: get_recent_decision_entries failed: {e}")
        return 0


def next_check_time(now: Optional[datetime] = None) -> str:
    """v1.1 TASK 7 -- deterministic next cron fire time, rounded up to the next _SNAPSHOT_INTERVAL_MINUTES boundary. Not a guess: matches .github/workflows/owner_snapshot.yml's own schedule exactly."""
    now = now or datetime.now(timezone.utc)
    minutes_past = now.minute % _SNAPSHOT_INTERVAL_MINUTES
    minutes_to_add = _SNAPSHOT_INTERVAL_MINUTES - minutes_past if minutes_past else _SNAPSHOT_INTERVAL_MINUTES
    next_time = (now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add))
    return next_time.strftime("%H:%M UTC")


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

    # v1.1 TASK 1/2/3/8: one shared read of today's decision rows,
    # never raises (see _decision_rows_today's own docstring).
    decision_rows = _decision_rows_today(signal_repository)
    pipeline_runs_today, pipeline_last_at, pipeline_last_status = _pipeline_activity(decision_rows)
    (
        signals_approved, signals_rejected, strategy_breakdown,
        decision_avg_confidence_pct, decision_risk_pass_rate_pct,
    ) = _decision_breakdown(decision_rows)
    last_signal_score = _last_signal_score(signal_repository)
    errors_critical, errors_warning, last_error_module, last_error_time = _error_breakdown()

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
        pipeline_runs_today=pipeline_runs_today,
        pipeline_last_at=pipeline_last_at,
        pipeline_last_status=pipeline_last_status,
        signals_approved=signals_approved,
        signals_rejected=signals_rejected,
        strategy_breakdown=strategy_breakdown,
        last_signal_score=last_signal_score,
        decision_total=len(decision_rows),
        decision_approved=signals_approved,
        decision_rejected=signals_rejected,
        decision_avg_confidence_pct=decision_avg_confidence_pct,
        decision_risk_pass_rate_pct=decision_risk_pass_rate_pct,
        # v1.1 TASK 4: always NO_DATA/0 -- AI request/response logs are
        # in-memory only, never persisted (see the audit doc's TASK 4
        # finding). Not fabricated.
        ai_requests_today=0,
        ai_status="NO_DATA",
        market_provider=provider_name or Config.MARKET_DATA_PROVIDER,
        market_symbol=symbol,
        market_timeframe=DEFAULT_TIMEFRAME,
        market_candles_configured=Config.TIMEFRAME_HISTORY.get(DEFAULT_TIMEFRAME, 0),
        errors_critical=errors_critical,
        errors_warning=errors_warning,
        last_error_module=last_error_module,
        last_error_time=last_error_time,
        db_signals_total=len(decision_rows),
        db_errors_total=error_count,
        db_pipeline_events_total=_pipeline_events_total(),
        runtime_next_check=next_check_time(),
    )
