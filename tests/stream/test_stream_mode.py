"""TASK-CORE-004 -- StreamMode + weekend/pause resolution."""

from datetime import datetime, timezone

from data_layer.live_data.stream.stream_mode import StreamMode, is_market_open, is_weekend, resolve_mode

# 2026-01-03 is a Saturday; 2026-01-05 is a Monday; 2026-01-02 is a Friday.
SATURDAY = datetime(2026, 1, 3, 12, tzinfo=timezone.utc)
SUNDAY_EARLY = datetime(2026, 1, 4, 10, tzinfo=timezone.utc)
SUNDAY_OPEN = datetime(2026, 1, 4, 23, tzinfo=timezone.utc)
MONDAY = datetime(2026, 1, 5, 12, tzinfo=timezone.utc)
FRIDAY_OPEN = datetime(2026, 1, 2, 12, tzinfo=timezone.utc)
FRIDAY_CLOSED = datetime(2026, 1, 2, 23, tzinfo=timezone.utc)


def test_is_weekend_saturday():
    assert is_weekend(SATURDAY) is True


def test_is_weekend_sunday_before_open():
    assert is_weekend(SUNDAY_EARLY) is True


def test_is_weekend_sunday_after_open_is_open():
    assert is_weekend(SUNDAY_OPEN) is False


def test_friday_before_close_open():
    assert is_weekend(FRIDAY_OPEN) is False


def test_friday_after_close_weekend():
    assert is_weekend(FRIDAY_CLOSED) is True


def test_weekday_is_open():
    assert is_market_open(MONDAY) is True


def test_resolve_mode_active_on_weekday():
    assert resolve_mode(now=MONDAY) is StreamMode.ACTIVE


def test_resolve_mode_weekend_wait():
    assert resolve_mode(now=SATURDAY) is StreamMode.WEEKEND_WAIT


def test_resolve_mode_manual_hold_wins():
    assert resolve_mode(now=MONDAY, manual_hold=True) is StreamMode.MANUAL_HOLD


def test_resolve_mode_paused():
    assert resolve_mode(now=MONDAY, paused=True) is StreamMode.PAUSED


def test_manual_hold_beats_weekend():
    assert resolve_mode(now=SATURDAY, manual_hold=True) is StreamMode.MANUAL_HOLD


def test_mode_is_flowing():
    assert StreamMode.ACTIVE.is_flowing() is True
    assert StreamMode.WEEKEND_WAIT.is_flowing() is False
    assert StreamMode.WEEKEND_WAIT.is_waiting() is True
