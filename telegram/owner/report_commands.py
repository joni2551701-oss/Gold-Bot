"""
Telegram Layer — Owner Report Commands (Phase 59.4, TASK 5: Owner
Report Foundation). Same "real function, not live-wired" posture as
provider_commands.py/system_commands.py/feature_commands.py (same
package, Phase 59.3) -- see provider_commands.py's own docstring.

Matches this task's own worked example:

    /stats
    Today:
    Signals 5
    Approved: 3
    TP: 2
    SL: 1
    Best Strategy: Liquidity Sweep

Takes already-computed data as input (List[SignalSchema] for the
total/approved counts, List[SignalPerformance] for the TP/SL/result
counts) -- same "compute from supplied data, don't fetch" posture
every analytics/ function already uses. Nothing in this codebase
persists a day's worth of SignalSchema/SignalPerformance records
anywhere yet (see docs/PHASE59_VALIDATION.md's own "Known gaps"
section) -- a real /stats command would need that data source wired
up first, a separate, future step.
"""

from typing import Dict, Optional, Sequence

from analytics.strategy_report import StrategyPerformanceReport, build_strategy_report
from analytics.signal_performance import SignalPerformance
from signals.schema import SignalSchema
from telegram.owner.provider_commands import ProviderCommandResult
from core.logger import setup_logger

logger = setup_logger("ReportCommands")


def pick_best_strategy(
    reports: Dict[str, StrategyPerformanceReport],
    minimum_signals: int = 1,
) -> Optional[StrategyPerformanceReport]:
    """
    Highest win_rate, ties broken by more total_signals (a high win
    rate on one trade is not as meaningful as the same rate on fifty --
    disclosed tie-break rule, not an arbitrary pick).
    `minimum_signals` excludes strategies with too few decided trades
    to be meaningful (default 1 -- excludes only genuinely empty
    entries). Never raises: an empty `reports` dict returns None.
    """
    eligible = [r for r in reports.values() if r.total_signals >= minimum_signals]
    if not eligible:
        return None
    return max(eligible, key=lambda r: (r.win_rate, r.total_signals))


def format_daily_stats(
    signals: Sequence[SignalSchema],
    performances: Sequence[SignalPerformance],
) -> ProviderCommandResult:
    """
    The future /stats command's payload. `signals` supplies the total/
    approved counts (SignalPerformance itself has no decision field);
    `performances` supplies the TP/SL/Expired/Cancelled counts and the
    best-strategy pick, via analytics/strategy_report.py's
    build_strategy_report() (reused, not reimplemented). Never raises:
    empty inputs produce an all-zero report, not an exception.
    """
    try:
        total_signals = len(signals)
        approved_count = sum(1 for s in signals if s.decision == "APPROVED")

        tp_count = sum(1 for p in performances if p.result == "TP")
        sl_count = sum(1 for p in performances if p.result == "SL")
        expired_count = sum(1 for p in performances if p.result == "EXPIRED")
        cancelled_count = sum(1 for p in performances if p.result == "CANCELLED")

        strategy_reports = build_strategy_report(performances)
        best = pick_best_strategy(strategy_reports)

        lines = [
            "Today:",
            f"Signals: {total_signals}",
            f"Approved: {approved_count}",
            f"TP: {tp_count}",
            f"SL: {sl_count}",
            f"Expired: {expired_count}",
            f"Cancelled: {cancelled_count}",
            f"Best Strategy: {best.strategy_id if best else 'N/A'}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"format_daily_stats failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
