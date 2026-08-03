"""
Telegram Layer — Owner Validation Commands (Phase 59 Real Market
Validation Foundation, TASK 8). Same "real function, not live-wired"
posture as provider_commands.py/system_commands.py/feature_commands.py/
report_commands.py (same package) -- see provider_commands.py's own
docstring.

Takes already-computed data as input (Sequence[SignalSchema]/
Sequence[SignalPerformance]), same "compute from supplied data, don't
fetch" posture every function in this package already uses -- nothing
in this codebase persists a day's/week's worth of these anywhere yet
(see docs/PHASE59_VALIDATION.md's "Known gaps"), so a real command
still needs that data source wired up first, a separate future step.
"""

from datetime import datetime
from typing import Sequence

from analytics.signal_performance import SignalPerformance
from analytics.validation_report import build_validation_report, format_validation_report
from config import Config
from signal_layer.signal_builder.schema import SignalSchema
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("ValidationCommands")


def get_validation_status() -> ProviderCommandResult:
    """
    Reports config.Config.VALIDATION_MODE's current value (Phase 59
    Real Market Validation Foundation, TASK 1) -- the single real
    switch this whole phase's foundation reads. Never raises.
    """
    state = "ON" if Config.VALIDATION_MODE else "OFF"
    return ProviderCommandResult(success=True, message=f"Validation Mode: {state}")


def get_today_signals(signals: Sequence[SignalSchema]) -> ProviderCommandResult:
    """
    `signals` must already be filtered to the caller's definition of
    "today" -- this function has no clock and no database access, same
    posture as report_commands.format_daily_stats(). Reports the
    total count plus a BUY/SELL breakdown. Never raises: an empty
    `signals` produces an all-zero report, not an exception.
    """
    try:
        buy_count = sum(1 for s in signals if s.direction == "BUY")
        sell_count = sum(1 for s in signals if s.direction == "SELL")

        lines = [
            "Today's Signals:",
            f"Total: {len(signals)}",
            f"BUY: {buy_count}",
            f"SELL: {sell_count}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_today_signals failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_validation_report(
    signals: Sequence[SignalSchema],
    performances: Sequence[SignalPerformance],
    period_start: datetime,
    period_end: datetime,
) -> ProviderCommandResult:
    """
    Wraps analytics.validation_report.build_validation_report()/
    format_validation_report() (same phase, TASK 5) unmodified -- this
    function adds nothing but the ProviderCommandResult envelope so a
    future handler has one consistent return shape across this whole
    package. Never raises: build/format themselves never raise on
    empty input.
    """
    try:
        report = build_validation_report(signals, performances, period_start, period_end)
        text = format_validation_report(report)
        return ProviderCommandResult(success=True, message=text)
    except Exception as e:
        logger.warning(f"get_validation_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
