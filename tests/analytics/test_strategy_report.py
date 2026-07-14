"""
Phase 59 Preparation, TASK 3 -- analytics/strategy_report.py tests.
"""

from datetime import datetime, timezone

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import build_strategy_report


def _perf(strategy_id, result, r_multiple=None, signal_id="s"):
    return SignalPerformance(
        performance_id="p",
        signal_id=signal_id,
        strategy_id=strategy_id,
        result=result,
        r_multiple=r_multiple,
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
