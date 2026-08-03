"""
Backtesting Layer — Backtest Result (Phase 60.2: Backtesting Engine,
TASK 4).

BacktestResult is the final report `backtesting_layer/backtest_engine/backtest_engine.py`
(TASK 3) produces -- one record per backtest run, holding every
`analytics.signal_performance.SignalPerformance` it computed plus the
`analytics.strategy_report.build_strategy_report()` grouping over
them. No new performance-computation logic here: this module only
packages already-computed `analytics/` output into one immutable
value and formats it for `platform_layer/telegram/owner/backtest_commands.py`
(TASK 5) — the same "compose, don't reimplement" posture every prior
Phase 59.x/60.x report module already established.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import StrategyPerformanceReport, build_strategy_report, compute_win_rate


@dataclass(frozen=True)
class BacktestResult:
    """
    candles_processed: how many candles the replay window actually
        advanced through (may be less than the configured range's
        total if the run was stopped early).
    signals_generated: every SignalCandidate the Strategy layer
        produced, regardless of AI/Decision/Risk outcome.
    trades_opened: how many of those were APPROVE + risk-approved,
        i.e. how many actually became a `trade_monitoring_layer.paper_trading.paper_trade.PaperTrade`.
    performances: one `SignalPerformance` per generated signal (Phase
        60.2's own new caller of `analytics.signal_performance.compute_signal_performance()`
        -- unmodified, same function every other performance figure in
        this codebase already uses).
    strategy_report: `build_strategy_report(performances)`'s own
        output, grouped by `strategy_id` -- unmodified.
    """
    symbol: str
    timeframe: str
    candles_processed: int
    signals_generated: int
    trades_opened: int
    performances: List[SignalPerformance] = field(default_factory=list)
    strategy_report: Dict[str, StrategyPerformanceReport] = field(default_factory=dict)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    @property
    def overall_win_rate(self) -> float:
        """Across every strategy combined -- compute_win_rate() unmodified, same formula as every other win-rate figure in this codebase."""
        wins = sum(r.win_count for r in self.strategy_report.values())
        losses = sum(r.loss_count for r in self.strategy_report.values())
        return compute_win_rate(wins, losses)


def build_backtest_result(
    symbol: str,
    timeframe: str,
    candles_processed: int,
    signals_generated: int,
    trades_opened: int,
    performances: List[SignalPerformance],
    started_at: Optional[datetime] = None,
    finished_at: Optional[datetime] = None,
) -> BacktestResult:
    """Wraps build_strategy_report(performances) (analytics/strategy_report.py, unmodified) alongside the run's own counters."""
    return BacktestResult(
        symbol=symbol,
        timeframe=timeframe,
        candles_processed=candles_processed,
        signals_generated=signals_generated,
        trades_opened=trades_opened,
        performances=performances,
        strategy_report=build_strategy_report(performances),
        started_at=started_at,
        finished_at=finished_at,
    )


def format_backtest_report(result: BacktestResult) -> str:
    """The future `/backtest_report` command's payload. Never raises: an empty strategy_report produces a report with zero strategy lines, not an error."""
    lines = [
        f"Dataset: {result.symbol} {result.timeframe}",
        f"Candles processed: {result.candles_processed}",
        f"Signals generated: {result.signals_generated}",
        f"Trades opened: {result.trades_opened}",
        f"Overall win rate: {result.overall_win_rate:.1%}",
        "",
        "Strategy breakdown:",
    ]
    if not result.strategy_report:
        lines.append("  (no strategy-linked signals)")
    for strategy_id, report in result.strategy_report.items():
        lines.append(
            f"  {strategy_id}: {report.total_signals} signals, "
            f"win={report.win_count} loss={report.loss_count} "
            f"win_rate={report.win_rate:.1%}"
        )
    return "\n".join(lines)
