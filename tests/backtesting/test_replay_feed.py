"""
Phase 60.1, TASK 4 -- backtesting_layer/replay_engine/replay_feed.py tests.
"""

from datetime import datetime, timezone

from backtesting_layer.replay_engine.replay_feed import ReplayFeed
from data_layer.providers.twelve_data_client import Candle


def _candles(n=5):
    return [
        Candle(timestamp=datetime(2026, 1, 1, i, tzinfo=timezone.utc), open=1.0, high=2.0, low=0.5, close=1.5)
        for i in range(n)
    ]


def test_current_candle_is_none_before_any_advance():
    feed = ReplayFeed(_candles())
    assert feed.current_candle() is None


def test_next_candle_advances_and_returns():
    feed = ReplayFeed(_candles())
    first = feed.next_candle()
    assert first is not None
    assert feed.current_candle() == first


def test_next_candle_returns_none_once_exhausted():
    feed = ReplayFeed(_candles(2))
    feed.next_candle()
    feed.next_candle()
    assert feed.next_candle() is None


def test_is_exhausted_reflects_cursor_position():
    feed = ReplayFeed(_candles(2))
    assert feed.is_exhausted is False
    feed.next_candle()
    assert feed.is_exhausted is False
    feed.next_candle()
    assert feed.is_exhausted is True


def test_previous_candle_retreats_cursor():
    feed = ReplayFeed(_candles(3))
    feed.next_candle()
    second = feed.next_candle()
    back = feed.previous_candle()
    assert back != second
    assert feed.current_candle() == back


def test_previous_candle_none_at_start():
    feed = ReplayFeed(_candles())
    assert feed.previous_candle() is None
    feed.next_candle()
    assert feed.previous_candle() is None  # cursor at 0, can't retreat further


def test_jump_moves_directly_to_index():
    feed = ReplayFeed(_candles(5))
    candle = feed.jump(3)
    assert candle == feed.candles[3]
    assert feed.cursor == 3


def test_jump_clamps_to_valid_range():
    feed = ReplayFeed(_candles(3))
    feed.jump(99)
    assert feed.cursor == 2
    feed.jump(-99)
    assert feed.cursor == -1


def test_window_returns_last_n_up_to_cursor():
    feed = ReplayFeed(_candles(10))
    feed.jump(5)
    window = feed.window(3)
    assert window == feed.candles[3:6]


def test_window_empty_before_first_advance():
    feed = ReplayFeed(_candles())
    assert feed.window(5) == []


def test_window_shorter_than_size_near_start():
    feed = ReplayFeed(_candles(10))
    feed.jump(1)
    window = feed.window(5)
    assert window == feed.candles[0:2]


def test_total_reflects_candle_count():
    feed = ReplayFeed(_candles(7))
    assert feed.total == 7
