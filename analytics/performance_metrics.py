"""
Analytics Layer — Performance Metrics Engine (Phase 60.4: Performance
Validation Foundation, TASK 2).

Reuse-audit finding (TASK 1): neither `monitoring/performance.py`'s
`PerformanceTracker` (database-driven, win/loss/win_rate only) nor
`analytics/strategy_report.py`'s `StrategyPerformanceReport`
(win/loss/breakeven/expired/cancelled counts + average R, grouped per
strategy) computes expectancy, profit factor, drawdown, recovery
factor, or a risk-adjusted return anywhere in this codebase. This
module adds exactly those five metrics, ungrouped (portfolio-wide, not
per-strategy — `strategy_report.py` already owns the per-strategy
view; a caller that wants per-strategy metrics groups with
`filter_performances()` first, same composition pattern
`strategy_report.py`/`context_report.py` already use).

`compute_win_rate()` is reused directly from `strategy_report.py`, not
reimplemented — the same WIN/(WIN+LOSS) convention, BE excluded from
both sides, this codebase has used since Phase 59.

All R-based, not dollar-based: no PnL/lot-value model exists anywhere
in this codebase (see `signal_performance.py`'s own docstring), so
Profit Factor and Average Win/Loss are computed on `r_multiple`
directly — a gross-R ratio, not a gross-dollar one. Max Drawdown and
Recovery Factor are the one exception: they require a dollar-shaped
curve to be meaningful (a drawdown "fraction of peak" needs a peak
that exists in the first place), so both are optional here and only
populate when the caller supplies an already-built
`equity_curve.EquityPoint` sequence (Phase 60.4 TASK 3) — this module
does not build one itself, and never re-derives
`EquityCurveConfig.unit_risk_amount`'s disclosed assumption on its
own; it only reads whatever curve it is handed.
"""

import statistics
from dataclasses import dataclass
from typing import Optional, Sequence, TYPE_CHECKING

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import compute_win_rate

if TYPE_CHECKING:
    from analytics.equity_curve import EquityPoint


@dataclass(frozen=True)
class PerformanceMetrics:
    """
    total_trades: every SignalPerformance passed in, regardless of
        result.
    winning_trades/losing_trades/breakeven_trades: counts of
        "TP"/"SL"/"BE" results specifically — same vocabulary as
        `strategy_report.StrategyPerformanceReport`.
    win_rate: `compute_win_rate(winning_trades, losing_trades)`.
    average_win_r/average_loss_r: mean r_multiple among winners
        (typically positive) / mean absolute r_multiple among losers
        (typically 1.0R); None if that side has no decided trades.
    expectancy: (win_rate * average_win_r) - (loss_rate *
        average_loss_r), the Director's own formula, in R units. None
        if there are no decided (TP/SL) trades at all.
    profit_factor: gross winning R / gross losing R (both magnitudes).
        None if there are no losing trades (undefined, not infinite).
    max_drawdown/recovery_factor: None unless an equity curve was
        supplied to `compute_performance_metrics()` — see module
        docstring.
    risk_adjusted_return: expectancy / stdev(r_multiple) across every
        decided trade — a Sharpe-like ratio that stays in R units, so
        it needs no dollar amount at all. None with fewer than 2
        decided trades or a zero stdev (a flat run has no ratio to
        report, not an infinite one).
    """
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    breakeven_trades: int = 0
    win_rate: float = 0.0
    average_win_r: Optional[float] = None
    average_loss_r: Optional[float] = None
    expectancy: Optional[float] = None
    profit_factor: Optional[float] = None
    max_drawdown: Optional[float] = None
    recovery_factor: Optional[float] = None
    risk_adjusted_return: Optional[float] = None


def compute_performance_metrics(
    performances: Sequence[SignalPerformance],
    equity_curve: Optional[Sequence['EquityPoint']] = None,
) -> PerformanceMetrics:
    """
    Never raises: an empty or all-undecided input produces an
    all-default/None `PerformanceMetrics`, not an exception.
    """
    total_trades = len(performances)
    winning = [p for p in performances if p.result == "TP"]
    losing = [p for p in performances if p.result == "SL"]
    breakeven_trades = sum(1 for p in performances if p.result == "BE")

    winning_trades = len(winning)
    losing_trades = len(losing)
    win_rate = compute_win_rate(winning_trades, losing_trades)

    winning_r = [p.r_multiple for p in winning if p.r_multiple is not None]
    losing_r = [abs(p.r_multiple) for p in losing if p.r_multiple is not None]

    average_win_r = sum(winning_r) / len(winning_r) if winning_r else None
    average_loss_r = sum(losing_r) / len(losing_r) if losing_r else None

    decided = winning_trades + losing_trades
    expectancy = None
    if decided > 0:
        loss_rate = losing_trades / decided
        expectancy = (win_rate * (average_win_r or 0.0)) - (loss_rate * (average_loss_r or 0.0))

    profit_factor = None
    if losing_r and sum(losing_r) > 0:
        gross_win = sum(winning_r)
        gross_loss = sum(losing_r)
        profit_factor = gross_win / gross_loss

    max_dd = None
    recovery_factor = None
    if equity_curve:
        from analytics.equity_curve import max_drawdown as compute_max_drawdown

        max_dd = compute_max_drawdown(equity_curve)
        starting_balance = equity_curve[0].balance
        net_profit = equity_curve[-1].balance - starting_balance
        if max_dd and max_dd > 0 and starting_balance > 0:
            recovery_factor = net_profit / (max_dd * starting_balance)

    all_decided_r = winning_r + [-r for r in losing_r]
    risk_adjusted_return = None
    if expectancy is not None and len(all_decided_r) >= 2:
        stdev = statistics.pstdev(all_decided_r)
        if stdev > 0:
            risk_adjusted_return = expectancy / stdev

    return PerformanceMetrics(
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        breakeven_trades=breakeven_trades,
        win_rate=win_rate,
        average_win_r=average_win_r,
        average_loss_r=average_loss_r,
        expectancy=expectancy,
        profit_factor=profit_factor,
        max_drawdown=max_dd,
        recovery_factor=recovery_factor,
        risk_adjusted_return=risk_adjusted_return,
    )


def _fmt(value: Optional[float], suffix: str = "", digits: int = 2) -> str:
    return f"{value:.{digits}f}{suffix}" if value is not None else "N/A"


def format_performance_metrics(metrics: PerformanceMetrics) -> str:
    """
    Phase 60.4 TASK 7 -- a text summary for
    telegram/owner/performance_commands.py. Pure formatting, no
    computation. Never raises: every field on PerformanceMetrics is
    either a plain number or None.
    """
    lines = [
        "Performance Metrics",
        f"Total Trades: {metrics.total_trades}",
        f"Win: {metrics.winning_trades}  Loss: {metrics.losing_trades}  BE: {metrics.breakeven_trades}",
        f"Win Rate: {metrics.win_rate * 100:.1f}%",
        f"Average Win: {_fmt(metrics.average_win_r, 'R')}",
        f"Average Loss: {_fmt(metrics.average_loss_r, 'R')}",
        f"Expectancy: {_fmt(metrics.expectancy, 'R')}",
        f"Profit Factor: {_fmt(metrics.profit_factor)}",
        f"Max Drawdown: {_fmt(metrics.max_drawdown * 100 if metrics.max_drawdown is not None else None, '%', 1)}",
        f"Recovery Factor: {_fmt(metrics.recovery_factor)}",
        f"Risk-Adjusted Return: {_fmt(metrics.risk_adjusted_return)}",
    ]
    return "\n".join(lines)
