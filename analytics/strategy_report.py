"""
Analytics Layer — Strategy Report (Phase 59 Preparation, TASK 3:
Trading Performance Schema Foundation).

Aggregates a list of already-built SignalPerformance records
(signal_performance.py, same package) into one report per strategy --
the shape this task's own brief names as its goal:

    Liquidity Sweep: 100 trades, Win: 62, Loss: 38, RR: 2.1

win_rate here deliberately reuses monitoring/performance.py's own
PerformanceTracker._win_rate() formula (WIN / (WIN + LOSS), BE
excluded from both sides) -- the same convention, not a competing one,
so a future consumer never has to reconcile two different definitions
of "win rate" for the same underlying question. This module does not
import PerformanceTracker (that class reads its own input from the
database via SignalRepository; this module's input is an in-memory
List[SignalPerformance], a different data source) -- the formula is
independently, deliberately duplicated, three lines, disclosed here
rather than hidden, the same "small documented duplication" precedent
already accepted for Wyckoff-vs-AMD and Data Quality-vs-market_data.py.

"TP" is this module's WIN, "SL" is its LOSS, "BE" is its breakeven --
SignalPerformance.result's own vocabulary (lifecycle/paper_trade.py's
ALLOWED_PAPER_TRADE_RESULTS), not database/signal_repository.py's
WIN/LOSS/BE labels (a different table, untouched by this phase).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from analytics.signal_performance import SignalPerformance


@dataclass(frozen=True)
class StrategyPerformanceReport:
    """
    total_signals: every SignalPerformance grouped under this
        strategy_id, regardless of result (including still-open/
        expired ones).
    win_count/loss_count/breakeven_count: counts of "TP"/"SL"/"BE"
        results specifically.
    expired_count/cancelled_count (Phase 59.4, TASK 3): counts of
        "EXPIRED"/"CANCELLED" results specifically -- named explicitly
        in this task's own worked example ("Expired: 10"), additive to
        the four counts already here. Neither counts toward win_rate
        (only decided TP/SL outcomes do), same as breakeven_count.
    win_rate: win_count / (win_count + loss_count); 0.0 if both are
        zero (matches PerformanceTracker._win_rate()'s own
        zero-division guard exactly).
    average_r_multiple: the mean of every non-None r_multiple among
        this strategy's records; None if none are known yet.
    """
    strategy_id: str
    total_signals: int = 0
    win_count: int = 0
    loss_count: int = 0
    breakeven_count: int = 0
    expired_count: int = 0
    cancelled_count: int = 0
    win_rate: float = 0.0
    average_r_multiple: Optional[float] = None


def compute_win_rate(win_count: int, loss_count: int) -> float:
    """
    Same formula and zero-division guard as monitoring/performance.py's
    PerformanceTracker._win_rate() -- see module docstring. Renamed
    from a private _win_rate() to this public name in Phase 59.4
    (TASK 4) once analytics/context_report.py (same package) became a
    second real caller -- no behavior change.
    """
    decided = win_count + loss_count
    if decided == 0:
        return 0.0
    return win_count / decided


def filter_performances(
    performances: Sequence[SignalPerformance],
    strategy_id: Optional[str] = None,
    market_phase: Optional[str] = None,
    session: Optional[str] = None,
    timeframe: Optional[str] = None,
) -> List[SignalPerformance]:
    """
    Phase 59 Real Market Validation Foundation, TASK 6 -- a generic
    AND-filter over the four dimensions this task's own brief names
    (strategy_id, market_phase, session, timeframe), e.g. combined
    with build_strategy_report() to answer "Liquidity Sweep / London /
    M15 winrate?" without either function needing to know about the
    other's job. Any argument left None is not filtered on. Never
    raises: no matches returns an empty list.

    Note: the brief's own worked example ("Liquidity Sweep / London /
    M15 / BULLISH HTF") lists a fifth value, HTF bias, under this same
    filter set -- but HTF bias (context_layer/trend/htf_bias.py's HTFBias enum:
    BULLISH/BEARISH/NEUTRAL/UNKNOWN) is a different concept from
    market_phase (MarketPhase: ACCUMULATION/MANIPULATION/
    DISTRIBUTION/MARKUP/MARKDOWN), and SignalPerformance carries no
    htf_bias field. This function implements exactly the four
    dimensions the brief explicitly declares as the filter set;
    htf_bias filtering is out of scope here, not silently folded into
    market_phase.
    """
    def _matches(performance: SignalPerformance) -> bool:
        if strategy_id is not None and performance.strategy_id != strategy_id:
            return False
        if market_phase is not None and performance.market_phase != market_phase:
            return False
        if session is not None and performance.session != session:
            return False
        if timeframe is not None and performance.timeframe != timeframe:
            return False
        return True

    return [performance for performance in performances if _matches(performance)]


def build_strategy_report(
    performances: Sequence[SignalPerformance],
) -> Dict[str, StrategyPerformanceReport]:
    """
    Groups by strategy_id, skipping any record with strategy_id=None
    (no strategy reference -- nothing to group it under). Never
    raises: an empty input list produces an empty dict, not an error.
    """
    grouped: Dict[str, List[SignalPerformance]] = {}
    for performance in performances:
        if performance.strategy_id is None:
            continue
        grouped.setdefault(performance.strategy_id, []).append(performance)

    report: Dict[str, StrategyPerformanceReport] = {}
    for strategy_id, records in grouped.items():
        win_count = sum(1 for r in records if r.result == "TP")
        loss_count = sum(1 for r in records if r.result == "SL")
        breakeven_count = sum(1 for r in records if r.result == "BE")
        expired_count = sum(1 for r in records if r.result == "EXPIRED")
        cancelled_count = sum(1 for r in records if r.result == "CANCELLED")

        r_multiples = [r.r_multiple for r in records if r.r_multiple is not None]
        average_r_multiple = sum(r_multiples) / len(r_multiples) if r_multiples else None

        report[strategy_id] = StrategyPerformanceReport(
            strategy_id=strategy_id,
            total_signals=len(records),
            win_count=win_count,
            loss_count=loss_count,
            breakeven_count=breakeven_count,
            expired_count=expired_count,
            cancelled_count=cancelled_count,
            win_rate=compute_win_rate(win_count, loss_count),
            average_r_multiple=average_r_multiple,
        )

    return report
