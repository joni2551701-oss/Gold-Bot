"""
Phase 60.2, TASK 4 -- backtesting_layer/backtest_report/backtest_result.py tests.
"""

from datetime import datetime, timezone

from analytics.signal_performance import SignalPerformance
from backtesting_layer.backtest_report.backtest_result import build_backtest_result, format_backtest_report


def _performance(strategy_id="LIQUIDITY_SWEEP", result=None):
    return SignalPerformance(
        performance_id="perf-1", signal_id="sig-1", strategy_id=strategy_id,
        context_id=None, session=None, market_phase=None, timeframe="M15",
        result=result, profit_loss=None, r_multiple=None, duration=None,
    )


def test_build_backtest_result_wraps_strategy_report():
    performances = [_performance(result="TP"), _performance(result="SL")]

    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=100,
        signals_generated=2, trades_opened=2, performances=performances,
    )

    assert "LIQUIDITY_SWEEP" in result.strategy_report
    assert result.strategy_report["LIQUIDITY_SWEEP"].win_count == 1
    assert result.strategy_report["LIQUIDITY_SWEEP"].loss_count == 1


def test_overall_win_rate_computed_across_all_strategies():
    performances = [
        _performance(strategy_id="A", result="TP"),
        _performance(strategy_id="B", result="TP"),
        _performance(strategy_id="B", result="SL"),
    ]

    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=10,
        signals_generated=3, trades_opened=3, performances=performances,
    )

    assert result.overall_win_rate == 2 / 3


def test_overall_win_rate_zero_for_no_decided_trades():
    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=10,
        signals_generated=0, trades_opened=0, performances=[],
    )
    assert result.overall_win_rate == 0.0


def test_format_backtest_report_never_raises_on_empty_result():
    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=0,
        signals_generated=0, trades_opened=0, performances=[],
    )
    text = format_backtest_report(result)
    assert "XAUUSD" in text
    assert "(no strategy-linked signals)" in text


def test_format_backtest_report_includes_strategy_breakdown():
    performances = [_performance(strategy_id="LIQUIDITY_SWEEP", result="TP")]
    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=50,
        signals_generated=1, trades_opened=1, performances=performances,
    )

    text = format_backtest_report(result)

    assert "LIQUIDITY_SWEEP" in text
    assert "Candles processed: 50" in text
    assert "Trades opened: 1" in text


def test_started_and_finished_at_round_trip():
    started = datetime(2026, 1, 1, tzinfo=timezone.utc)
    finished = datetime(2026, 1, 1, 1, tzinfo=timezone.utc)
    result = build_backtest_result(
        symbol="XAUUSD", timeframe="M15", candles_processed=1,
        signals_generated=0, trades_opened=0, performances=[],
        started_at=started, finished_at=finished,
    )
    assert result.started_at == started
    assert result.finished_at == finished
