"""
Phase 60.4: Performance Validation Foundation, TASK 4 --
backtesting_layer/statistics/benchmark.py tests.
"""

from datetime import datetime, timedelta, timezone

from backtesting_layer.statistics.benchmark import compute_benchmark_comparison, format_benchmark_comparison
from backtesting_layer.statistics.equity_curve import EquityCurveConfig, build_equity_curve
from backtesting_layer.statistics.signal_performance import SignalPerformance


def _perf(r_multiple, created_at):
    return SignalPerformance(performance_id="p", signal_id="s", r_multiple=r_multiple, created_at=created_at)


def test_matches_the_directors_own_worked_example():
    """Gold +5%, Strategy +18% -> Alpha: +13%."""
    now = datetime.now(timezone.utc)
    config = EquityCurveConfig(starting_balance=1000.0, unit_risk_amount=1800.0)
    performances = [_perf(0.1, now)]  # 1000 -> 1180, +18%
    curve = build_equity_curve(performances, config)

    comparison = compute_benchmark_comparison(curve, benchmark_start_price=2000.0, benchmark_end_price=2100.0)

    assert round(comparison.strategy_return_pct, 1) == 18.0
    assert round(comparison.benchmark_return_pct, 1) == 5.0
    assert round(comparison.alpha_pct, 1) == 13.0
    assert format_benchmark_comparison(comparison) == "Gold +5.0%, Strategy +18.0% -> Alpha: +13.0%"


def test_none_when_equity_curve_has_only_the_starting_point():
    curve = build_equity_curve([])

    comparison = compute_benchmark_comparison(curve, benchmark_start_price=2000.0, benchmark_end_price=2100.0)

    assert comparison is None


def test_none_when_benchmark_start_price_is_not_positive():
    now = datetime.now(timezone.utc)
    curve = build_equity_curve([_perf(1.0, now)])

    comparison = compute_benchmark_comparison(curve, benchmark_start_price=0.0, benchmark_end_price=2100.0)

    assert comparison is None


def test_negative_alpha_when_benchmark_outperforms():
    now = datetime.now(timezone.utc)
    config = EquityCurveConfig(starting_balance=1000.0, unit_risk_amount=10.0)
    curve = build_equity_curve([_perf(0.1, now)], config)  # +1%

    comparison = compute_benchmark_comparison(curve, benchmark_start_price=2000.0, benchmark_end_price=2200.0)  # +10%

    assert comparison.alpha_pct < 0


def test_never_raises_on_declining_equity_curve():
    now = datetime.now(timezone.utc)
    curve = build_equity_curve([_perf(-1.0, now), _perf(-1.0, now + timedelta(minutes=1))])

    compute_benchmark_comparison(curve, benchmark_start_price=2000.0, benchmark_end_price=1900.0)  # must not raise
