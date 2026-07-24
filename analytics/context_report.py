"""
Analytics Layer — Context Performance (Phase 59.4, TASK 4).

The Director's own framing: "Bu keyinchalik AI uchun oltin dataset"
(this becomes a golden dataset for AI later) — aggregates
`SignalPerformance` by market context (`session`, `strategy_id`, and
optionally `market_phase`), not just by strategy alone
(`strategy_report.py`, same package). Matches this task's own worked
example shape:

    London + Liquidity Sweep  ->  Winrate 71%
    Asia + Breakout           ->  Winrate 42%

Real available dimensions on `SignalPerformance` are `session` and
`strategy_id` (both already real since Phase 59 Preparation/AC-03) —
the default grouping here. The brief's own example additionally
mentions "+ FVG", which reads as a third dimension; the cleanest
real third dimension `SignalPerformance` actually carries is
`market_phase` (Phase A/AC-02), not a strategy-name repeated a second
time — `include_market_phase=True` groups by
`(session, strategy_id, market_phase)` instead, a disclosed,
deliberate substitution for the brief's own illustrative "+FVG",
rather than inventing a fourth field this codebase has no source for.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple, Union

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import compute_win_rate

# (session, strategy_id) by default; (session, strategy_id, market_phase) when include_market_phase=True.
ContextKey = Union[Tuple[str, str], Tuple[str, str, str]]


@dataclass(frozen=True)
class ContextPerformanceReport:
    """Same shape and counting convention as StrategyPerformanceReport (same package) -- see that module's own docstring for each field's meaning."""
    session: str
    strategy_id: str
    market_phase: Optional[str] = None
    total_signals: int = 0
    win_count: int = 0
    loss_count: int = 0
    breakeven_count: int = 0
    expired_count: int = 0
    cancelled_count: int = 0
    win_rate: float = 0.0
    average_r_multiple: Optional[float] = None


def build_context_report(
    performances: Sequence[SignalPerformance],
    include_market_phase: bool = False,
) -> Dict[ContextKey, ContextPerformanceReport]:
    """
    Groups by (session, strategy_id) -- or (session, strategy_id,
    market_phase) when include_market_phase=True -- skipping any
    record missing session or strategy_id (nothing to group it under;
    same "skip incomplete records" posture as
    strategy_report.build_strategy_report()'s own strategy_id=None
    handling). Never raises: an empty input list produces an empty
    dict.
    """
    grouped: Dict[ContextKey, List[SignalPerformance]] = {}
    for performance in performances:
        if performance.session is None or performance.strategy_id is None:
            continue
        if include_market_phase:
            if performance.market_phase is None:
                continue
            key = (performance.session, performance.strategy_id, performance.market_phase)
        else:
            key = (performance.session, performance.strategy_id)
        grouped.setdefault(key, []).append(performance)

    report: Dict[ContextKey, ContextPerformanceReport] = {}
    for key, records in grouped.items():
        win_count = sum(1 for r in records if r.result == "TP")
        loss_count = sum(1 for r in records if r.result == "SL")
        breakeven_count = sum(1 for r in records if r.result == "BE")
        expired_count = sum(1 for r in records if r.result == "EXPIRED")
        cancelled_count = sum(1 for r in records if r.result == "CANCELLED")

        r_multiples = [r.r_multiple for r in records if r.r_multiple is not None]
        average_r_multiple = sum(r_multiples) / len(r_multiples) if r_multiples else None

        session, strategy_id = key[0], key[1]
        market_phase = key[2] if include_market_phase else None

        report[key] = ContextPerformanceReport(
            session=session,
            strategy_id=strategy_id,
            market_phase=market_phase,
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
