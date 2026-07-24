"""
Unit tests for data/candle_clock.py (Candle Builder companion, module 3).

Covers window alignment for all six timeframes, next-boundary, is_boundary,
same_window, UTC enforcement, and clock independence (pure functions).
"""

from datetime import datetime, timezone, timedelta

import pytest

from data.candle_clock import CandleClock, TIMEFRAME_MINUTES, TIMEFRAME_ORDER


def _dt(y=2026, mo=7, d=24, h=0, mi=0, s=0):
    return datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)


@pytest.fixture
def clock():
    return CandleClock()


def test_timeframe_order_is_ascending():
    assert TIMEFRAME_ORDER == ["M1", "M5", "M15", "H1", "H4", "D1"]
    mins = [TIMEFRAME_MINUTES[tf] for tf in TIMEFRAME_ORDER]
    assert mins == sorted(mins)


@pytest.mark.parametrize("tf,when,expected", [
    ("M1",  _dt(h=13, mi=37, s=42), _dt(h=13, mi=37)),
    ("M5",  _dt(h=13, mi=37, s=42), _dt(h=13, mi=35)),
    ("M15", _dt(h=13, mi=37),       _dt(h=13, mi=30)),
    ("H1",  _dt(h=13, mi=37),       _dt(h=13, mi=0)),
    ("H4",  _dt(h=13, mi=37),       _dt(h=12, mi=0)),
    ("D1",  _dt(h=13, mi=37),       _dt(h=0,  mi=0)),
])
def test_window_start_alignment(clock, tf, when, expected):
    assert clock.window_start(tf, when) == expected


def test_next_boundary(clock):
    assert clock.next_boundary("M5", _dt(h=13, mi=37)) == _dt(h=13, mi=40)
    assert clock.next_boundary("H4", _dt(h=13)) == _dt(h=16)
    assert clock.next_boundary("D1", _dt(h=13)) == _dt(d=25, h=0)


def test_is_boundary(clock):
    assert clock.is_boundary("M15", _dt(h=13, mi=30))
    assert not clock.is_boundary("M15", _dt(h=13, mi=31))


def test_same_window(clock):
    a = _dt(h=13, mi=31)
    b = _dt(h=13, mi=34)
    c = _dt(h=13, mi=36)
    assert clock.same_window("M5", a, b)       # both in 13:30-13:35
    assert not clock.same_window("M5", a, c)   # c is in 13:35-13:40


def test_unknown_timeframe_raises(clock):
    with pytest.raises(KeyError):
        clock.window_start("M3", _dt())


def test_naive_datetime_rejected(clock):
    with pytest.raises(ValueError):
        clock.window_start("M1", datetime(2026, 7, 24, 13, 0))


def test_non_utc_is_normalized(clock):
    tz = timezone(timedelta(hours=2))
    local = datetime(2026, 7, 24, 15, 37, tzinfo=tz)   # == 13:37 UTC
    assert clock.window_start("M15", local) == _dt(h=13, mi=30)


def test_purity_no_side_effects(clock):
    when = _dt(h=9, mi=3)
    a = clock.window_start("M5", when)
    b = clock.window_start("M5", when)
    assert a == b   # deterministic, argument-only
