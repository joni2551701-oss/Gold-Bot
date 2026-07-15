"""
Telegram Layer — Owner Performance Commands (Phase 60.4: Performance
Validation Foundation, TASK 7). Same "real function, not live-wired"
posture as backtest_commands.py/execution_commands.py (same package)
-- see provider_commands.py's own docstring. NOT registered into
telegram/commands.py, NOT called from telegram/command_router.py or
telegram/handlers.py.

Thin wrappers over analytics.performance_metrics/analytics.equity_curve/
analytics.benchmark (Phase 60.4, TASKS 2-4) -- this module writes no
metric/curve/comparison computation of its own, only the
ProviderCommandResult envelope, same "compute from supplied data,
don't fetch" posture validation_commands.py already established: the
caller supplies an already-built Sequence[SignalPerformance] (nothing
in this codebase persists one yet -- see analytics/README.md's own
"Future Roadmap"), same honest gap disclosed there, not hidden here.
"""

from typing import Optional, Sequence

from analytics.benchmark import compute_benchmark_comparison, format_benchmark_comparison
from analytics.equity_curve import EquityCurveConfig, build_equity_curve, format_equity_curve_summary
from analytics.performance_metrics import compute_performance_metrics, format_performance_metrics
from analytics.signal_performance import SignalPerformance
from telegram.owner.provider_commands import ProviderCommandResult
from core.logger import setup_logger

logger = setup_logger("PerformanceCommands")


def get_performance_report(performances: Sequence[SignalPerformance]) -> ProviderCommandResult:
    """
    The future `/performance` command's payload -- wraps
    analytics.performance_metrics.compute_performance_metrics()/
    format_performance_metrics() unmodified. No equity curve is built
    here, so max_drawdown/recovery_factor report "N/A" -- use
    get_equity_curve_report() for the dollar-shaped view. Never raises.
    """
    try:
        metrics = compute_performance_metrics(performances)
        return ProviderCommandResult(success=True, message=format_performance_metrics(metrics))
    except Exception as e:
        logger.warning(f"get_performance_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_equity_curve_report(
    performances: Sequence[SignalPerformance],
    starting_balance: Optional[float] = None,
    unit_risk_amount: Optional[float] = None,
) -> ProviderCommandResult:
    """
    The future `/equity_curve` command's payload -- wraps
    analytics.equity_curve.build_equity_curve()/
    format_equity_curve_summary() unmodified. starting_balance/
    unit_risk_amount, when supplied, override EquityCurveConfig's own
    defaults (1000.0/100.0) -- the same disclosed, visualization-only
    assumption equity_curve.py's own module docstring names. Never
    raises: build_equity_curve() always returns at least one point.
    """
    try:
        config = None
        if starting_balance is not None or unit_risk_amount is not None:
            config = EquityCurveConfig(
                starting_balance=starting_balance if starting_balance is not None else EquityCurveConfig.starting_balance,
                unit_risk_amount=unit_risk_amount if unit_risk_amount is not None else EquityCurveConfig.unit_risk_amount,
            )
        points = build_equity_curve(performances, config)
        return ProviderCommandResult(success=True, message=format_equity_curve_summary(points))
    except Exception as e:
        logger.warning(f"get_equity_curve_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_backtest_performance_report(
    performances: Sequence[SignalPerformance],
    benchmark_start_price: Optional[float] = None,
    benchmark_end_price: Optional[float] = None,
) -> ProviderCommandResult:
    """
    The future `/backtest_report` command's payload -- combines
    get_performance_report()'s metrics with a benchmark comparison
    (analytics.benchmark, TASK 4) when both benchmark prices are
    supplied; falls back to metrics only otherwise, matching this
    package's existing "don't fetch, only compute from what's given"
    posture (no candle/database access here). Never raises.
    """
    try:
        metrics = compute_performance_metrics(performances)
        sections = [format_performance_metrics(metrics)]

        if benchmark_start_price is not None and benchmark_end_price is not None:
            points = build_equity_curve(performances)
            comparison = compute_benchmark_comparison(points, benchmark_start_price, benchmark_end_price)
            if comparison is not None:
                sections.append(format_benchmark_comparison(comparison))

        return ProviderCommandResult(success=True, message="\n\n".join(sections))
    except Exception as e:
        logger.warning(f"get_backtest_performance_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
