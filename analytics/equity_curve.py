"""
Analytics Layer — Equity Curve Engine (Phase 60.4: Performance
Validation Foundation, TASK 3).

Reuse-audit finding (TASK 1): no PnL/dollar computation exists
anywhere in this codebase — `analytics.signal_performance.SignalPerformance.profit_loss`
is always `None`, an honest hook, per that module's own docstring
("no PnL/lot-value computation exists anywhere in this codebase
today"). The Director's own worked example (`1000$ -> +30 -> 1030$`)
is expressed in dollars, so this module makes one explicit,
documented, *visualization-only* assumption to bridge that gap:
`EquityCurveConfig.unit_risk_amount` — a configurable dollar value
representing "1R" — converts each trade's already-computed
`r_multiple` (real, from `compute_r_multiple()`) into a dollar delta.
This is not a sizing or PnL computation, and `risk_layer/risk_engine/risk_manager.py`
is completely untouched — it exists only so this module can render an
equity curve shape, the same disclosed-assumption posture
`backtesting/backtest_engine.py`'s own HTF-neutral-fallback used in
Phase 60.2.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from analytics.signal_performance import SignalPerformance


@dataclass(frozen=True)
class EquityCurveConfig:
    starting_balance: float = 1000.0
    unit_risk_amount: float = 100.0


@dataclass(frozen=True)
class EquityPoint:
    """drawdown is a fraction (0.0-1.0) below the running peak balance, 0.0 at or above a new peak."""
    timestamp: Optional[datetime]
    balance: float
    drawdown: float


def build_equity_curve(
    performances: Sequence['SignalPerformance'], config: Optional[EquityCurveConfig] = None
) -> List[EquityPoint]:
    """
    Ordered by `SignalPerformance.created_at` (the only timestamp a
    `SignalPerformance` carries — not a close timestamp, since none
    exists on that model either; see its own docstring). Records with
    `r_multiple is None` (never resolved, e.g. still open or no
    `PaperTrade` at all) are skipped — they contributed no realized
    outcome to walk the curve forward on. Never raises: an empty or
    all-unresolved list produces a single starting point.
    """
    config = config or EquityCurveConfig()
    resolved = sorted(
        (p for p in performances if p.r_multiple is not None),
        key=lambda p: p.created_at or datetime.min,
    )

    balance = config.starting_balance
    peak = balance
    points = [EquityPoint(timestamp=None, balance=balance, drawdown=0.0)]

    for performance in resolved:
        balance += performance.r_multiple * config.unit_risk_amount
        peak = max(peak, balance)
        drawdown = (peak - balance) / peak if peak > 0 else 0.0
        points.append(EquityPoint(timestamp=performance.created_at, balance=balance, drawdown=drawdown))

    return points


def max_drawdown(points: Sequence[EquityPoint]) -> float:
    """The largest drawdown fraction reached anywhere on the curve -- 0.0 for an empty or ever-rising curve."""
    return max((p.drawdown for p in points), default=0.0)


def format_equity_curve_summary(points: Sequence[EquityPoint]) -> str:
    """
    Phase 60.4 TASK 7 -- a text summary for
    telegram/owner/performance_commands.py, not the full point-by-point
    curve (a Telegram message has no chart). Pure formatting, no
    computation beyond max_drawdown() (this module, above). Never
    raises: build_equity_curve() always returns at least one point.
    """
    start = points[0]
    end = points[-1]
    lines = [
        "Equity Curve",
        f"Starting Balance: {start.balance:.2f}",
        f"Ending Balance: {end.balance:.2f}",
        f"Net Change: {end.balance - start.balance:+.2f}",
        f"Max Drawdown: {max_drawdown(points) * 100:.1f}%",
        f"Points: {len(points)}",
    ]
    return "\n".join(lines)
