"""
Phase 59 Real Market Validation Foundation, TASK 5 --
backtesting_layer/statistics/validation_report.py tests.
"""

from datetime import datetime, timezone

from backtesting_layer.statistics.signal_performance import SignalPerformance
from backtesting_layer.statistics.validation_report import ValidationReport, build_validation_report, format_validation_report
from signal_layer.signal_builder.schema import SignalSchema

P0 = datetime(2026, 8, 1, tzinfo=timezone.utc)
P1 = datetime(2026, 8, 8, tzinfo=timezone.utc)


def _signal(signal_id, direction):
    return SignalSchema(
        signal_id=signal_id, created_at=datetime.now(timezone.utc), symbol="XAUUSD",
        timeframe="M15", direction=direction, decision="APPROVED",
    )


def _perf(signal_id="s", strategy_id="LIQUIDITY_SWEEP_STRATEGY", session=None, market_phase=None,
          result=None, r_multiple=None):
    return SignalPerformance(
        performance_id="p", signal_id=signal_id, strategy_id=strategy_id, session=session,
        market_phase=market_phase, result=result, r_multiple=r_multiple,
        created_at=datetime.now(timezone.utc),
    )


def test_empty_input_never_raises_and_produces_zero_report():
    report = build_validation_report([], [], P0, P1)

    assert isinstance(report, ValidationReport)
    assert report.total_signals == 0
    assert report.buy_count == 0
    assert report.sell_count == 0
    assert report.strategy_reports == {}
    assert report.best_session is None
    assert report.best_market_phase is None


def test_counts_buy_and_sell_signals():
    signals = [_signal("s1", "BUY"), _signal("s2", "BUY"), _signal("s3", "SELL")]

    report = build_validation_report(signals, [], P0, P1)

    assert report.total_signals == 3
    assert report.buy_count == 2
    assert report.sell_count == 1


def test_strategy_reports_reuses_build_strategy_report():
    performances = [_perf(result="TP", r_multiple=2.0), _perf(result="SL", r_multiple=-1.0)]

    report = build_validation_report([], performances, P0, P1)

    assert "LIQUIDITY_SWEEP_STRATEGY" in report.strategy_reports
    assert report.strategy_reports["LIQUIDITY_SWEEP_STRATEGY"].win_count == 1


def test_best_session_picks_highest_win_rate():
    performances = (
        [_perf(session="LONDON", result="TP", r_multiple=2.0) for _ in range(8)]
        + [_perf(session="LONDON", result="SL", r_multiple=-1.0) for _ in range(2)]
        + [_perf(session="ASIA", result="TP", r_multiple=2.0) for _ in range(3)]
        + [_perf(session="ASIA", result="SL", r_multiple=-1.0) for _ in range(3)]
    )

    report = build_validation_report([], performances, P0, P1)

    assert report.best_session == "LONDON"


def test_best_market_phase_picks_highest_win_rate():
    performances = (
        [_perf(market_phase="ACCUMULATION", result="TP", r_multiple=2.0) for _ in range(9)]
        + [_perf(market_phase="ACCUMULATION", result="SL", r_multiple=-1.0) for _ in range(1)]
        + [_perf(market_phase="MARKUP", result="SL", r_multiple=-1.0) for _ in range(5)]
    )

    report = build_validation_report([], performances, P0, P1)

    assert report.best_market_phase == "ACCUMULATION"


def test_best_session_none_when_no_session_data():
    performances = [_perf(session=None, result="TP", r_multiple=2.0)]

    report = build_validation_report([], performances, P0, P1)

    assert report.best_session is None


def test_period_is_preserved_exactly():
    report = build_validation_report([], [], P0, P1)

    assert report.period_start == P0
    assert report.period_end == P1


# --- format_validation_report ---

def test_format_matches_the_briefs_own_worked_example_shape():
    signals = [_signal(f"s{i}", "BUY" if i < 70 else "SELL") for i in range(120)]
    performances = (
        [_perf(result="TP", r_multiple=2.0) for _ in range(28)]
        + [_perf(result="SL", r_multiple=-1.0) for _ in range(17)]
    )
    report = build_validation_report(signals, performances, P0, P1)

    text = format_validation_report(report)

    assert "GoldBot Validation Report" in text
    assert "Signals: 120" in text
    assert "BUY: 70" in text
    assert "SELL: 50" in text
    assert "Strategy: LIQUIDITY_SWEEP_STRATEGY" in text
    assert "Win: 28" in text
    assert "Loss: 17" in text
    assert "Winrate: 62%" in text


def test_format_never_raises_on_empty_report():
    report = build_validation_report([], [], P0, P1)
    text = format_validation_report(report)
    assert "Best Session: N/A" in text
    assert "Best Market Phase: N/A" in text


def test_format_handles_missing_average_r_multiple():
    performances = [_perf(result="EXPIRED", r_multiple=None)]
    report = build_validation_report([], performances, P0, P1)

    text = format_validation_report(report)

    assert "Average R: N/A" in text
