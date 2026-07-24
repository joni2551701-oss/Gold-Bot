"""
Analytics Layer — Benchmark Comparison (Phase 60.4: Performance
Validation Foundation, TASK 4).

Compares the strategy's own equity curve (`equity_curve.py`, TASK 3)
against a buy-and-hold XAUUSD benchmark over the same period — the
Director's own worked example ("Gold +5%, Strategy +18% -> Alpha:
+13%"). Deliberately does not read candles itself: this package stays
database-free (see `analytics/README.md`'s "What this package does
NOT do") and has no dependency on `data/`/`database/` today. The
caller — a future `backtest_commands.py`/`performance_commands.py`
consumer — already has both endpoints (the first/last candle close of
the backtested range) and the equity curve; this module only does the
arithmetic, the same "adapter, not calculator" posture
`execution_report.py` already established for a different pair of
already-computed inputs.

Both returns are percentages of their own starting value — the
strategy's return uses `EquityCurveConfig.starting_balance`
(equity_curve.py's own disclosed dollar-per-1R assumption), the
benchmark's uses whatever price the caller supplies as the range's
opening gold price. Alpha is simply strategy_return_pct minus
benchmark_return_pct, not a risk-adjusted (beta-weighted) alpha — this
module makes no claim beyond the Director's own worked example's
shape.
"""

from dataclasses import dataclass
from typing import Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from analytics.equity_curve import EquityPoint


@dataclass(frozen=True)
class BenchmarkComparison:
    """
    strategy_return_pct: percentage change of the equity curve's last
        balance vs its first (starting_balance).
    benchmark_return_pct: percentage change of benchmark_end_price vs
        benchmark_start_price (buy-and-hold XAUUSD over the same
        period).
    alpha_pct: strategy_return_pct - benchmark_return_pct — positive
        means the strategy beat buy-and-hold over this period,
        negative means buy-and-hold would have done better.
    """
    strategy_return_pct: float
    benchmark_return_pct: float
    alpha_pct: float


def compute_benchmark_comparison(
    equity_curve: Sequence['EquityPoint'],
    benchmark_start_price: float,
    benchmark_end_price: float,
) -> Optional[BenchmarkComparison]:
    """
    None when there is nothing to compare: an equity curve with fewer
    than 2 points (no realized trade moved the balance at all) or a
    non-positive benchmark_start_price (a buy-and-hold return is
    undefined against a zero/negative starting price). Never raises.
    """
    if len(equity_curve) < 2 or benchmark_start_price <= 0:
        return None

    starting_balance = equity_curve[0].balance
    ending_balance = equity_curve[-1].balance
    if starting_balance <= 0:
        return None

    strategy_return_pct = ((ending_balance - starting_balance) / starting_balance) * 100.0
    benchmark_return_pct = (
        (benchmark_end_price - benchmark_start_price) / benchmark_start_price
    ) * 100.0
    alpha_pct = strategy_return_pct - benchmark_return_pct

    return BenchmarkComparison(
        strategy_return_pct=strategy_return_pct,
        benchmark_return_pct=benchmark_return_pct,
        alpha_pct=alpha_pct,
    )


def format_benchmark_comparison(comparison: BenchmarkComparison) -> str:
    """Matches the Director's own worked example shape: 'Gold +5%, Strategy +18% -> Alpha: +13%'."""
    return (
        f"Gold {comparison.benchmark_return_pct:+.1f}%, "
        f"Strategy {comparison.strategy_return_pct:+.1f}% "
        f"-> Alpha: {comparison.alpha_pct:+.1f}%"
    )
