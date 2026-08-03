"""
Phase 60.4: Performance Validation Foundation, TASK 2 --
backtesting_layer/statistics/performance_metrics.py tests.
"""

from datetime import datetime, timedelta, timezone

from backtesting_layer.statistics.equity_curve import build_equity_curve
from backtesting_layer.statistics.performance_metrics import compute_performance_metrics
from backtesting_layer.statistics.signal_performance import SignalPerformance


def _perf(result, r_multiple=None, created_at=None, signal_id="s"):
    return SignalPerformance(
        performance_id="p",
        signal_id=signal_id,
        result=result,
        r_multiple=r_multiple,
        created_at=created_at,
    )


def test_empty_input_produces_all_default_metrics():
    metrics = compute_performance_metrics([])

    assert metrics.total_trades == 0
    assert metrics.win_rate == 0.0
    assert metrics.expectancy is None
    assert metrics.profit_factor is None
    assert metrics.max_drawdown is None
    assert metrics.recovery_factor is None
    assert metrics.risk_adjusted_return is None


def test_counts_and_win_rate_match_strategy_reports_own_convention():
    performances = (
        [_perf("TP", 2.1) for _ in range(62)]
        + [_perf("SL", -1.0) for _ in range(38)]
    )

    metrics = compute_performance_metrics(performances)

    assert metrics.total_trades == 100
    assert metrics.winning_trades == 62
    assert metrics.losing_trades == 38
    assert metrics.win_rate == 0.62


def test_breakeven_counted_but_excluded_from_win_rate_and_decided_totals():
    performances = [_perf("TP", 1.5), _perf("SL", -1.0), _perf("BE", 0.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.breakeven_trades == 1
    assert metrics.win_rate == 0.5


def test_average_win_and_loss_r_are_magnitudes():
    performances = [_perf("TP", 2.0), _perf("TP", 4.0), _perf("SL", -1.0), _perf("SL", -0.5)]

    metrics = compute_performance_metrics(performances)

    assert metrics.average_win_r == 3.0
    assert metrics.average_loss_r == 0.75


def test_expectancy_matches_the_directors_own_formula():
    """Expectancy = (WinRate * AvgWin) - (LossRate * AvgLoss)."""
    performances = [_perf("TP", 2.0), _perf("TP", 2.0), _perf("SL", -1.0)]

    metrics = compute_performance_metrics(performances)

    win_rate = 2 / 3
    loss_rate = 1 / 3
    expected = (win_rate * 2.0) - (loss_rate * 1.0)
    assert round(metrics.expectancy, 6) == round(expected, 6)


def test_expectancy_none_with_no_decided_trades():
    performances = [_perf(None), _perf("EXPIRED")]

    metrics = compute_performance_metrics(performances)

    assert metrics.expectancy is None


def test_profit_factor_is_gross_win_r_over_gross_loss_r():
    performances = [_perf("TP", 2.0), _perf("TP", 1.0), _perf("SL", -1.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.profit_factor == 3.0  # (2.0 + 1.0) / 1.0


def test_profit_factor_none_with_no_losing_trades():
    performances = [_perf("TP", 2.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.profit_factor is None


def test_max_drawdown_and_recovery_factor_none_without_equity_curve():
    performances = [_perf("TP", 1.0), _perf("SL", -1.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.max_drawdown is None
    assert metrics.recovery_factor is None


def test_max_drawdown_and_recovery_factor_populate_with_equity_curve():
    now = datetime.now(timezone.utc)
    performances = [
        _perf("TP", 1.0, created_at=now),
        _perf("SL", -0.5, created_at=now + timedelta(minutes=1)),
    ]
    curve = build_equity_curve(performances)

    metrics = compute_performance_metrics(performances, equity_curve=curve)

    assert metrics.max_drawdown is not None
    assert metrics.max_drawdown > 0.0
    assert metrics.recovery_factor is not None


def test_recovery_factor_none_when_curve_never_draws_down():
    now = datetime.now(timezone.utc)
    performances = [_perf("TP", 1.0, created_at=now)]
    curve = build_equity_curve(performances)

    metrics = compute_performance_metrics(performances, equity_curve=curve)

    assert metrics.max_drawdown == 0.0
    assert metrics.recovery_factor is None


def test_risk_adjusted_return_none_with_fewer_than_two_decided_trades():
    performances = [_perf("TP", 2.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.risk_adjusted_return is None


def test_risk_adjusted_return_populates_with_varied_results():
    performances = [_perf("TP", 3.0), _perf("SL", -1.0), _perf("TP", 1.0)]

    metrics = compute_performance_metrics(performances)

    assert metrics.risk_adjusted_return is not None


def test_never_raises_on_mixed_valid_and_incomplete_records():
    performances = [_perf(None), _perf("TP", None), _perf("SL", -1.0), _perf("EXPIRED")]

    compute_performance_metrics(performances)  # must not raise
