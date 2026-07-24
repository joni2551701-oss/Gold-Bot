"""
Phase 60.4, TASK 7 -- telegram/owner/performance_commands.py tests.
No mocks: real SignalPerformance/PerformanceMetrics/EquityPoint
construction, same convention as every other telegram/owner/ test.
"""

from datetime import datetime, timezone

from telegram.owner.performance_commands import (
    get_backtest_performance_report,
    get_equity_curve_report,
    get_performance_report,
)
from telegram.owner.provider_commands import ProviderCommandResult
from analytics.signal_performance import SignalPerformance


def _perf(result, r_multiple=None, created_at=None):
    return SignalPerformance(
        performance_id="p", signal_id="s", result=result, r_multiple=r_multiple, created_at=created_at
    )


def test_get_performance_report_returns_a_report():
    performances = [_perf("TP", 2.0), _perf("SL", -1.0)]

    result = get_performance_report(performances)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "Total Trades: 2" in result.message
    assert "Win Rate: 50.0%" in result.message


def test_get_performance_report_never_raises_on_empty_input():
    result = get_performance_report([])

    assert result.success is True
    assert "Total Trades: 0" in result.message


def test_get_equity_curve_report_returns_a_report():
    now = datetime.now(timezone.utc)
    performances = [_perf("TP", 0.3, created_at=now)]

    result = get_equity_curve_report(performances)

    assert result.success is True
    assert "Starting Balance: 1000.00" in result.message
    assert "Ending Balance: 1030.00" in result.message


def test_get_equity_curve_report_respects_config_overrides():
    now = datetime.now(timezone.utc)
    performances = [_perf("TP", 1.0, created_at=now)]

    result = get_equity_curve_report(performances, starting_balance=5000.0, unit_risk_amount=50.0)

    assert "Starting Balance: 5000.00" in result.message
    assert "Ending Balance: 5050.00" in result.message


def test_get_equity_curve_report_never_raises_on_empty_input():
    result = get_equity_curve_report([])

    assert result.success is True
    assert "Points: 1" in result.message


def test_get_backtest_performance_report_without_benchmark():
    performances = [_perf("TP", 2.0)]

    result = get_backtest_performance_report(performances)

    assert result.success is True
    assert "Performance Metrics" in result.message
    assert "Alpha" not in result.message


def test_get_backtest_performance_report_with_benchmark():
    now = datetime.now(timezone.utc)
    performances = [_perf("TP", 0.1, created_at=now)]

    result = get_backtest_performance_report(
        performances, benchmark_start_price=2000.0, benchmark_end_price=2100.0
    )

    assert result.success is True
    assert "Performance Metrics" in result.message
    assert "Alpha" in result.message


def test_get_backtest_performance_report_never_raises_on_empty_input():
    result = get_backtest_performance_report([], benchmark_start_price=2000.0, benchmark_end_price=2100.0)

    assert result.success is True
