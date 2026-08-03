"""State machine + clock tests (module 8)."""

from datetime import timedelta

import pytest

from backtesting_layer.replay_engine.replay_state import (
    ReplayState, can_transition, assert_transition, ReplayStateError,
)
from backtesting_layer.replay_engine.replay_clock import ReplayClock
from data_layer.market_memory.candle_record import MemoryMode
from _rfakes import ts


def test_legal_transitions():
    assert can_transition(ReplayState.IDLE, ReplayState.LOADED)
    assert can_transition(ReplayState.LOADED, ReplayState.PLAYING)
    assert can_transition(ReplayState.PLAYING, ReplayState.PAUSED)
    assert can_transition(ReplayState.PAUSED, ReplayState.PLAYING)
    assert can_transition(ReplayState.PLAYING, ReplayState.FINISHED)
    assert can_transition(ReplayState.FINISHED, ReplayState.LIVE)


def test_illegal_transitions_rejected():
    assert not can_transition(ReplayState.IDLE, ReplayState.PLAYING)
    assert not can_transition(ReplayState.LIVE, ReplayState.PLAYING)
    with pytest.raises(ReplayStateError):
        assert_transition(ReplayState.IDLE, ReplayState.LIVE)


def test_clock_advance_by_speed():
    c = ReplayClock(ts(0), speed=2.0)
    c.advance(timedelta(minutes=1))     # 1 min real * 2 = 2 min virtual
    assert c.now() == ts(2)


def test_clock_speed_change_and_seek():
    c = ReplayClock(ts(0))
    c.set_speed(5.0)
    c.advance(timedelta(minutes=1))
    assert c.now() == ts(5)
    c.seek(ts(0))
    assert c.now() == ts(0)


def test_clock_switch_live_stops_replay_advance():
    c = ReplayClock(ts(0))
    c.switch_live(ts(10))
    assert c.mode() is MemoryMode.LIVE
    c.advance(timedelta(minutes=5))     # LIVE: replay advance is a no-op
    assert c.now() == ts(10)


def test_clock_rejects_bad_speed_and_naive_time():
    with pytest.raises(ValueError):
        ReplayClock(ts(0), speed=0)
    import datetime as _dt
    with pytest.raises(ValueError):
        ReplayClock(_dt.datetime(2026, 7, 24))
