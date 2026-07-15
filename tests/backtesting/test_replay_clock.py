"""
Phase 60.1, TASK 3 -- backtesting/replay_clock.py tests.
"""

import pytest

from backtesting.replay_clock import ReplayClock
from backtesting.replay_models import ReplayState


def test_new_clock_starts_pending():
    clock = ReplayClock()
    assert clock.state == ReplayState.PENDING
    assert clock.position == -1


def test_play_sets_running():
    clock = ReplayClock()
    clock.play()
    assert clock.is_running is True


def test_pause_sets_paused():
    clock = ReplayClock()
    clock.play()
    clock.pause()
    assert clock.is_paused is True


def test_resume_sets_running_again():
    clock = ReplayClock()
    clock.play()
    clock.pause()
    clock.resume()
    assert clock.is_running is True


def test_stop_sets_stopped():
    clock = ReplayClock()
    clock.play()
    clock.stop()
    assert clock.is_stopped is True


def test_advance_only_moves_while_running():
    clock = ReplayClock()
    clock.advance()
    assert clock.position == -1

    clock.play()
    clock.advance()
    assert clock.position == 0


def test_advance_respects_speed():
    clock = ReplayClock(speed=3.0)
    clock.play()
    clock.advance()
    assert clock.position == 2


def test_advance_minimum_one_step_below_speed_one():
    clock = ReplayClock(speed=0.3)
    clock.play()
    clock.advance()
    assert clock.position == 0


def test_advance_does_not_move_while_paused():
    clock = ReplayClock()
    clock.play()
    clock.advance()
    clock.pause()
    clock.advance()
    assert clock.position == 0


def test_set_speed_rejects_zero_and_negative():
    clock = ReplayClock()
    with pytest.raises(ValueError):
        clock.set_speed(0)
    with pytest.raises(ValueError):
        clock.set_speed(-1.0)


def test_seek_sets_position_directly():
    clock = ReplayClock()
    clock.seek(50)
    assert clock.position == 50


def test_seek_clamps_to_minus_one():
    clock = ReplayClock()
    clock.seek(-10)
    assert clock.position == -1
