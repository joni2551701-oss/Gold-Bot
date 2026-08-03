"""
Phase 59 Preparation, TASK 3 -- backtesting_layer/statistics/strategy_report.py tests.
"""

from datetime import datetime, timezone

from backtesting_layer.statistics.signal_performance import SignalPerformance
from backtesting_layer.statistics.strategy_report import build_strategy_report, filter_performances


def _perf(strategy_id, result, r_multiple=None, signal_id="s", session=None, market_phase=None, timeframe=None):
    return SignalPerformance(
        performance_id="p",
        signal_id=signal_id,
        strategy_id=strategy_id,
        result=result,
        r_multiple=r_multiple,
        session=session,
        market_phase=market_phase,
        timeframe=timeframe,
        created_at=datetime.now(timezone.utc),
    )


def test_empty_input_produces_empty_report():
    assert build_strategy_report([]) == {}


def test_groups_by_strategy_id():
    performances = [
        _perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0),
        _perf("FVG_STRATEGY", "SL", -1.0),
    ]

    report = build_strategy_report(performances)

    assert set(report.keys()) == {"LIQUIDITY_SWEEP_STRATEGY", "FVG_STRATEGY"}


def test_matches_the_briefs_own_worked_example_shape():
    """Liquidity Sweep: 100 trades, Win: 62, Loss: 38 -- the exact scenario named in this task's brief."""
    performances = (
        [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 2.1) for _ in range(62)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "SL", -1.0) for _ in range(38)]
    )

    report = build_strategy_report(performances)
    stats = report["LIQUIDITY_SWEEP_STRATEGY"]

    assert stats.total_signals == 100
    assert stats.win_count == 62
    assert stats.loss_count == 38
    assert stats.win_rate == 0.62
    assert round(stats.average_r_multiple, 4) == round((62 * 2.1 + 38 * -1.0) / 100, 4)


def test_breakeven_counted_but_excluded_from_win_rate():
    performances = [
        _perf("AMD_STRATEGY", "TP", 1.5),
        _perf("AMD_STRATEGY", "SL", -1.0),
        _perf("AMD_STRATEGY", "BE", 0.0),
    ]

    report = build_strategy_report(performances)
    stats = report["AMD_STRATEGY"]

    assert stats.total_signals == 3
    assert stats.breakeven_count == 1
    assert stats.win_rate == 0.5  # 1 win / (1 win + 1 loss), BE excluded


def test_win_rate_zero_when_no_decided_trades():
    performances = [_perf("FVG_STRATEGY", None), _perf("FVG_STRATEGY", "EXPIRED")]

    report = build_strategy_report(performances)
    stats = report["FVG_STRATEGY"]

    assert stats.win_rate == 0.0
    assert stats.total_signals == 2


def test_average_r_multiple_none_when_no_r_multiples_known():
    performances = [_perf("FVG_STRATEGY", "EXPIRED", r_multiple=None)]

    report = build_strategy_report(performances)

    assert report["FVG_STRATEGY"].average_r_multiple is None


def test_records_without_strategy_id_are_skipped():
    performances = [_perf(None, "TP", 2.0), _perf("AMD_STRATEGY", "TP", 1.0)]

    report = build_strategy_report(performances)

    assert set(report.keys()) == {"AMD_STRATEGY"}


def test_never_raises_on_mixed_valid_and_incomplete_records():
    performances = [
        _perf("LIQUIDITY_SWEEP_STRATEGY", None),
        _perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 3.0),
        _perf(None, "SL", -1.0),
    ]

    build_strategy_report(performances)  # must not raise


# --- Phase 59.4 TASK 3: expired/cancelled counts ---

def test_expired_count_matches_the_briefs_own_example():
    """Liquidity Sweep: 100 trades, Win 62, Loss 28, Expired 10 -- the exact scenario this task's brief names."""
    performances = (
        [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0) for _ in range(62)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "SL", -1.0) for _ in range(28)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "EXPIRED", None) for _ in range(10)]
    )

    report = build_strategy_report(performances)
    stats = report["LIQUIDITY_SWEEP_STRATEGY"]

    assert stats.total_signals == 100
    assert stats.win_count == 62
    assert stats.loss_count == 28
    assert stats.expired_count == 10
    assert stats.win_rate == 62 / 90


def test_cancelled_count_is_tracked_separately_from_expired():
    performances = [
        _perf("AMD_STRATEGY", "CANCELLED", None),
        _perf("AMD_STRATEGY", "EXPIRED", None),
        _perf("AMD_STRATEGY", "TP", 2.0),
    ]

    report = build_strategy_report(performances)
    stats = report["AMD_STRATEGY"]

    assert stats.cancelled_count == 1
    assert stats.expired_count == 1
    assert stats.total_signals == 3


def test_expired_and_cancelled_excluded_from_win_rate():
    performances = [
        _perf("FVG_STRATEGY", "TP", 2.0),
        _perf("FVG_STRATEGY", "EXPIRED", None),
        _perf("FVG_STRATEGY", "CANCELLED", None),
    ]

    report = build_strategy_report(performances)
    stats = report["FVG_STRATEGY"]

    assert stats.win_rate == 1.0  # 1 win / (1 win + 0 loss) -- expired/cancelled don't count as decided


def test_default_expired_and_cancelled_counts_are_zero():
    performances = [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0)]

    report = build_strategy_report(performances)

    assert report["LIQUIDITY_SWEEP_STRATEGY"].expired_count == 0
    assert report["LIQUIDITY_SWEEP_STRATEGY"].cancelled_count == 0


# --- Phase 59 Real Market Validation Foundation, TASK 6: filter_performances ---

def test_filter_performances_empty_filters_returns_everything():
    performances = [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0), _perf("FVG_STRATEGY", "SL", -1.0)]

    result = filter_performances(performances)

    assert result == performances


def test_filter_performances_by_strategy_id():
    performances = [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP"), _perf("FVG_STRATEGY", "SL")]

    result = filter_performances(performances, strategy_id="LIQUIDITY_SWEEP_STRATEGY")

    assert len(result) == 1
    assert result[0].strategy_id == "LIQUIDITY_SWEEP_STRATEGY"


def test_filter_performances_combines_all_four_dimensions():
    """The brief's own worked example shape: Liquidity Sweep / London / M15 winrate."""
    matching = _perf("LIQUIDITY_SWEEP_STRATEGY", "TP", session="LONDON", market_phase="MARKUP", timeframe="M15")
    wrong_session = _perf("LIQUIDITY_SWEEP_STRATEGY", "TP", session="ASIA", market_phase="MARKUP", timeframe="M15")
    wrong_timeframe = _perf("LIQUIDITY_SWEEP_STRATEGY", "TP", session="LONDON", market_phase="MARKUP", timeframe="H1")
    performances = [matching, wrong_session, wrong_timeframe]

    result = filter_performances(
        performances, strategy_id="LIQUIDITY_SWEEP_STRATEGY", session="LONDON", timeframe="M15"
    )

    assert result == [matching]


def test_filter_performances_no_match_returns_empty_list():
    performances = [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP")]

    result = filter_performances(performances, strategy_id="NONEXISTENT")

    assert result == []


def test_filter_performances_combines_with_build_strategy_report():
    performances = (
        [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP", session="LONDON") for _ in range(6)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "SL", session="LONDON") for _ in range(2)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "SL", session="ASIA") for _ in range(5)]
    )

    filtered = filter_performances(performances, session="LONDON")
    report = build_strategy_report(filtered)

    assert report["LIQUIDITY_SWEEP_STRATEGY"].total_signals == 8
    assert report["LIQUIDITY_SWEEP_STRATEGY"].win_rate == 0.75
