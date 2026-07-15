"""
Phase 60.2, TASK 2 -- backtesting/data_feed.py tests.
"""

from datetime import datetime, timezone

from backtesting.data_feed import LiveDataFeed, ReplayDataFeed
from backtesting.replay_feed import ReplayFeed
from data.twelve_data_client import Candle


def test_live_data_feed_delegates_to_market_data_normalizer():
    calls = []

    class _StubNormalizer:
        def get_candles(self, symbol, interval, outputsize):
            calls.append((symbol, interval, outputsize))
            return ["stub-candle"]

    feed = LiveDataFeed(_StubNormalizer(), symbol="XAUUSD", interval="M15")

    result = feed.get_candles(50)

    assert result == ["stub-candle"]
    assert calls == [("XAUUSD", "M15", 50)]


def test_replay_data_feed_delegates_to_replay_feed_window():
    candles = [
        Candle(timestamp=datetime(2026, 1, 1, i, tzinfo=timezone.utc), open=1.0, high=2.0, low=0.5, close=1.5)
        for i in range(5)
    ]
    replay_feed = ReplayFeed(candles)
    replay_feed.jump(4)

    feed = ReplayDataFeed(replay_feed)
    result = feed.get_candles(3)

    assert result == candles[2:5]


def test_replay_data_feed_empty_before_any_advance():
    replay_feed = ReplayFeed([])
    feed = ReplayDataFeed(replay_feed)
    assert feed.get_candles(10) == []
