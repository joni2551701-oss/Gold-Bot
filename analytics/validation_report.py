"""
Analytics Layer — Validation Report (Phase 59 Real Market Validation
Foundation, TASK 5).

The weekly report shape this task's own brief names as its goal:

    GoldBot Validation Report
    Period: 01.08 - 08.08
    Signals: 120
    BUY: 70
    SELL: 50
    Strategy: Liquidity Sweep
    Signals: 45 Win: 28 Loss: 17 Winrate: 62% Average R: 1.8
    Best Session: London
    Best Market Phase: Accumulation

A standardization/aggregation layer, like every other analytics/
module before it: computes nothing new except two small, disclosed
"best of" picks (best_session/best_market_phase, each the same
highest-win_rate-then-more-signals tie-break
platform_layer/telegram/owner/report_commands.py's pick_best_strategy() already
established for strategies) -- it reuses build_strategy_report()
(same package) for the per-strategy breakdown rather than
reimplementing it.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Sequence

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import StrategyPerformanceReport, build_strategy_report, compute_win_rate
from signal_layer.signal_builder.schema import SignalSchema


@dataclass(frozen=True)
class ValidationReport:
    """
    period_start/period_end: the caller-supplied window this report
        covers -- never inferred from the data itself (a signal list
        spanning fewer days than requested is still reported honestly
        against the requested window, not silently narrowed).
    total_signals/buy_count/sell_count: from `signals` (SignalSchema.direction).
    strategy_reports: analytics.strategy_report.build_strategy_report()'s
        own output, unmodified -- one entry per strategy_id.
    best_session/best_market_phase: the single session/market_phase
        with the highest win_rate among decided (TP/SL) results, ties
        broken by more total signals; None if no `performances` carry
        that dimension at all.
    """
    period_start: datetime
    period_end: datetime
    total_signals: int = 0
    buy_count: int = 0
    sell_count: int = 0
    strategy_reports: Dict[str, StrategyPerformanceReport] = field(default_factory=dict)
    best_session: Optional[str] = None
    best_market_phase: Optional[str] = None
    created_at: Optional[datetime] = None


def _best_by_win_rate(performances: Sequence[SignalPerformance], dimension: str) -> Optional[str]:
    """
    Groups by a single SignalPerformance attribute (`"session"` or
    `"market_phase"`), computing win_rate via
    analytics.strategy_report.compute_win_rate() (reused, not
    reimplemented) -- the same tie-break rule
    platform_layer/telegram/owner/report_commands.py's pick_best_strategy() already
    established (highest win_rate, ties broken by more total records).
    Never raises: no eligible records returns None.
    """
    grouped: Dict[str, List[SignalPerformance]] = {}
    for performance in performances:
        value = getattr(performance, dimension)
        if value is None:
            continue
        grouped.setdefault(value, []).append(performance)

    if not grouped:
        return None

    best_key = None
    best_win_rate = -1.0
    best_count = -1
    for key, records in grouped.items():
        win_count = sum(1 for r in records if r.result == "TP")
        loss_count = sum(1 for r in records if r.result == "SL")
        win_rate = compute_win_rate(win_count, loss_count)
        total = len(records)
        if (win_rate, total) > (best_win_rate, best_count):
            best_key, best_win_rate, best_count = key, win_rate, total

    return best_key


def build_validation_report(
    signals: Sequence[SignalSchema],
    performances: Sequence[SignalPerformance],
    period_start: datetime,
    period_end: datetime,
) -> ValidationReport:
    """
    Never raises: empty `signals`/`performances` produce a report with
    zero counts and None best_session/best_market_phase, not an
    exception.
    """
    buy_count = sum(1 for s in signals if s.direction == "BUY")
    sell_count = sum(1 for s in signals if s.direction == "SELL")

    return ValidationReport(
        period_start=period_start,
        period_end=period_end,
        total_signals=len(signals),
        buy_count=buy_count,
        sell_count=sell_count,
        strategy_reports=build_strategy_report(performances),
        best_session=_best_by_win_rate(performances, "session"),
        best_market_phase=_best_by_win_rate(performances, "market_phase"),
        created_at=datetime.now(period_start.tzinfo) if period_start.tzinfo else datetime.now(),
    )


def format_validation_report(report: ValidationReport) -> str:
    """
    Text-format rendering matching this task's own worked example
    exactly -- a pure formatting function, no computation. Used by
    platform_layer/telegram/owner/validation_commands.py (same phase, TASK 8).
    """
    lines = [
        "GoldBot Validation Report",
        f"Period: {report.period_start.date()} - {report.period_end.date()}",
        f"Signals: {report.total_signals}",
        f"BUY: {report.buy_count}",
        f"SELL: {report.sell_count}",
        "",
    ]
    for strategy_id, stats in report.strategy_reports.items():
        lines.append(f"Strategy: {strategy_id}")
        lines.append(f"Signals: {stats.total_signals}")
        lines.append(f"Win: {stats.win_count}")
        lines.append(f"Loss: {stats.loss_count}")
        lines.append(f"Winrate: {stats.win_rate * 100:.0f}%")
        avg_r = f"{stats.average_r_multiple:.1f}" if stats.average_r_multiple is not None else "N/A"
        lines.append(f"Average R: {avg_r}")
        lines.append("")

    lines.append(f"Best Session: {report.best_session or 'N/A'}")
    lines.append(f"Best Market Phase: {report.best_market_phase or 'N/A'}")

    return "\n".join(lines)
