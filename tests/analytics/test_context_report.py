"""
Phase 59.4, TASK 4 -- analytics/context_report.py tests.
"""

from datetime import datetime, timezone

from analytics.context_report import build_context_report
from analytics.signal_performance import SignalPerformance


def _perf(session, strategy_id, result, r_multiple=None, market_phase=None):
    return SignalPerformance(
        performance_id="p", signal_id="s", strategy_id=strategy_id, session=session,
        market_phase=market_phase, result=result, r_multiple=r_multiple,
        created_at=datetime.now(timezone.utc),
    )


def test_empty_input_produces_empty_report():
    assert build_context_report([]) == {}


def test_groups_by_session_and_strategy():
    performances = [
        _perf("LONDON", "LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0),
        _perf("ASIA", "AMD_STRATEGY", "SL", -1.0),
    ]

    report = build_context_report(performances)

    assert set(report.keys()) == {("LONDON", "LIQUIDITY_SWEEP_STRATEGY"), ("ASIA", "AMD_STRATEGY")}


def test_matches_the_briefs_own_worked_example_shape():
    """London + Liquidity Sweep -- winrate 71% (approximated with a small, exact sample here)."""
    performances = (
        [_perf("LONDON", "LIQUIDITY_SWEEP_STRATEGY", "TP", 2.0) for _ in range(71)]
        + [_perf("LONDON", "LIQUIDITY_SWEEP_STRATEGY", "SL", -1.0) for _ in range(29)]
    )

    report = build_context_report(performances)
    stats = report[("LONDON", "LIQUIDITY_SWEEP_STRATEGY")]

    assert stats.total_signals == 100
    assert stats.win_count == 71
    assert stats.win_rate == 0.71


def test_different_sessions_same_strategy_stay_separate():
    performances = [
        _perf("LONDON", "BREAKOUT_STRATEGY", "TP", 2.0),
        _perf("ASIA", "BREAKOUT_STRATEGY", "SL", -1.0),
    ]

    report = build_context_report(performances)

    assert report[("LONDON", "BREAKOUT_STRATEGY")].win_count == 1
    assert report[("ASIA", "BREAKOUT_STRATEGY")].loss_count == 1


def test_records_missing_session_are_skipped():
    performances = [_perf(None, "AMD_STRATEGY", "TP", 2.0)]
    assert build_context_report(performances) == {}


def test_records_missing_strategy_id_are_skipped():
    performances = [_perf("LONDON", None, "TP", 2.0)]
    assert build_context_report(performances) == {}


def test_expired_and_cancelled_counted_but_excluded_from_win_rate():
    performances = [
        _perf("LONDON", "FVG_STRATEGY", "TP", 2.0),
        _perf("LONDON", "FVG_STRATEGY", "EXPIRED"),
        _perf("LONDON", "FVG_STRATEGY", "CANCELLED"),
    ]

    report = build_context_report(performances)
    stats = report[("LONDON", "FVG_STRATEGY")]

    assert stats.expired_count == 1
    assert stats.cancelled_count == 1
    assert stats.win_rate == 1.0


def test_average_r_multiple_computed_per_combo():
    performances = [
        _perf("LONDON", "AMD_STRATEGY", "TP", 2.0),
        _perf("LONDON", "AMD_STRATEGY", "TP", 4.0),
    ]

    report = build_context_report(performances)

    assert report[("LONDON", "AMD_STRATEGY")].average_r_multiple == 3.0


# --- include_market_phase ---

def test_include_market_phase_adds_a_third_grouping_dimension():
    performances = [
        _perf("LONDON", "AMD_STRATEGY", "TP", 2.0, market_phase="MARKUP"),
        _perf("LONDON", "AMD_STRATEGY", "SL", -1.0, market_phase="MARKDOWN"),
    ]

    report = build_context_report(performances, include_market_phase=True)

    assert set(report.keys()) == {
        ("LONDON", "AMD_STRATEGY", "MARKUP"),
        ("LONDON", "AMD_STRATEGY", "MARKDOWN"),
    }
    assert report[("LONDON", "AMD_STRATEGY", "MARKUP")].market_phase == "MARKUP"


def test_include_market_phase_skips_records_missing_it():
    performances = [_perf("LONDON", "AMD_STRATEGY", "TP", 2.0, market_phase=None)]

    report = build_context_report(performances, include_market_phase=True)

    assert report == {}


def test_default_market_phase_is_none_when_not_grouping_by_it():
    performances = [_perf("LONDON", "AMD_STRATEGY", "TP", 2.0, market_phase="MARKUP")]

    report = build_context_report(performances)  # include_market_phase=False

    assert report[("LONDON", "AMD_STRATEGY")].market_phase is None


def test_never_raises_on_mixed_valid_and_incomplete_records():
    performances = [
        _perf(None, "AMD_STRATEGY", "TP", 2.0),
        _perf("LONDON", None, "SL", -1.0),
        _perf("LONDON", "AMD_STRATEGY", "TP", 3.0),
    ]

    build_context_report(performances)  # must not raise
