"""
Phase 60.4: Performance Validation Foundation, TASK 3 --
analytics/equity_curve.py tests.
"""

from datetime import datetime, timedelta, timezone

from analytics.equity_curve import EquityCurveConfig, build_equity_curve, max_drawdown
from analytics.signal_performance import SignalPerformance


def _perf(r_multiple, created_at=None, signal_id="s"):
    return SignalPerformance(
        performance_id="p",
        signal_id=signal_id,
        r_multiple=r_multiple,
        created_at=created_at,
    )


def test_empty_input_produces_single_starting_point():
    points = build_equity_curve([])

    assert len(points) == 1
    assert points[0].timestamp is None
    assert points[0].balance == 1000.0
    assert points[0].drawdown == 0.0


def test_all_unresolved_records_produce_only_starting_point():
    performances = [_perf(None), _perf(None)]

    points = build_equity_curve(performances)

    assert len(points) == 1
    assert points[0].balance == 1000.0


def test_matches_the_directors_own_worked_example():
    """1000$ -> +30 -> 1030$ -- a +0.3R trade against the default 100$ unit_risk_amount."""
    performances = [_perf(0.3, created_at=datetime.now(timezone.utc))]

    points = build_equity_curve(performances)

    assert len(points) == 2
    assert points[-1].balance == 1030.0


def test_losing_trade_after_winning_trade_creates_drawdown():
    now = datetime.now(timezone.utc)
    performances = [
        _perf(0.3, created_at=now),
        _perf(-0.15, created_at=now + timedelta(minutes=1)),
    ]

    points = build_equity_curve(performances)

    assert points[1].balance == 1030.0
    assert points[1].drawdown == 0.0
    assert points[2].balance == 1015.0
    assert round(points[2].drawdown, 4) == round((1030.0 - 1015.0) / 1030.0, 4)


def test_records_are_ordered_by_created_at_regardless_of_input_order():
    now = datetime.now(timezone.utc)
    earlier = _perf(1.0, created_at=now)
    later = _perf(-1.0, created_at=now + timedelta(minutes=5))

    points = build_equity_curve([later, earlier])

    assert points[1].timestamp == earlier.created_at
    assert points[2].timestamp == later.created_at


def test_records_with_none_r_multiple_are_skipped():
    now = datetime.now(timezone.utc)
    performances = [
        _perf(1.0, created_at=now),
        _perf(None, created_at=now + timedelta(minutes=1)),
    ]

    points = build_equity_curve(performances)

    assert len(points) == 2  # starting point + the one resolved trade


def test_custom_config_changes_starting_balance_and_unit_risk_amount():
    config = EquityCurveConfig(starting_balance=5000.0, unit_risk_amount=50.0)
    performances = [_perf(2.0, created_at=datetime.now(timezone.utc))]

    points = build_equity_curve(performances, config)

    assert points[0].balance == 5000.0
    assert points[-1].balance == 5100.0


def test_never_raises_on_records_missing_created_at():
    performances = [_perf(1.0, created_at=None), _perf(-1.0, created_at=None)]

    build_equity_curve(performances)  # must not raise


def test_max_drawdown_empty_list_returns_zero():
    assert max_drawdown([]) == 0.0


def test_max_drawdown_ever_rising_curve_returns_zero():
    now = datetime.now(timezone.utc)
    performances = [
        _perf(1.0, created_at=now),
        _perf(2.0, created_at=now + timedelta(minutes=1)),
    ]

    points = build_equity_curve(performances)

    assert max_drawdown(points) == 0.0


def test_max_drawdown_picks_the_largest_dip():
    now = datetime.now(timezone.utc)
    performances = [
        _perf(1.0, created_at=now),                        # 1000 -> 1100, peak 1100
        _perf(-0.5, created_at=now + timedelta(minutes=1)),  # 1100 -> 1050, dd ~4.5%
        _perf(1.0, created_at=now + timedelta(minutes=2)),   # 1050 -> 1150, new peak
        _perf(-1.0, created_at=now + timedelta(minutes=3)),  # 1150 -> 1050, dd ~8.7%
    ]

    points = build_equity_curve(performances)

    expected = (1150.0 - 1050.0) / 1150.0
    assert round(max_drawdown(points), 4) == round(expected, 4)
