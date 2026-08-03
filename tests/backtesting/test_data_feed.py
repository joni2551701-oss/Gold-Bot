"""
Phase 60.2, TASK 2 -- backtesting/data_feed.py tests.
"""

from datetime import datetime, timezone

from backtesting.data_feed import LiveDataFeed, ReplayDataFeed
from backtesting.replay_feed import ReplayFeed
from data_layer.providers.twelve_data_client import Candle


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


def test_live_and_replay_feeds_both_satisfy_idatafeed():
    """
    Phase 60.8 TASK 4 architecture confirmation: LiveDataFeed and
    ReplayDataFeed both really implement the one common IDataFeed
    contract -- BacktestEngine already only depends on ReplayDataFeed
    through this interface (backtesting/backtest_engine.py's own
    `self.data_feed: IDataFeed` field).
    """
    from backtesting.data_feed import IDataFeed

    assert issubclass(LiveDataFeed, IDataFeed)
    assert issubclass(ReplayDataFeed, IDataFeed)


def test_live_data_feed_call_signature_matches_core_pipelines_own_market_data_stage():
    """
    Phase 60.8 TASK 4 architecture confirmation, not a pipeline.py
    change: core/pipeline.py's live `market_data` stage still calls
    `MarketDataNormalizer.get_candles(symbol, interval, outputsize)`
    directly this phase (see docs/PIPELINE_GUARD.md's "Disclosed
    Findings" for why TASK 4 stops at confirmation rather than swapping
    that call site). This proves `LiveDataFeed(data_normalizer, symbol,
    interval).get_candles(outputsize)` is a byte-for-byte equivalent
    wrapper over that exact same call -- a future, separately-approved
    phase could swap the pipeline's call site for LiveDataFeed with
    zero behavior change.
    """
    calls = []

    class _StubNormalizer:
        def get_candles(self, symbol, interval, outputsize):
            calls.append((symbol, interval, outputsize))
            return ["candle-a", "candle-b"]

    normalizer = _StubNormalizer()
    direct_result = normalizer.get_candles("XAUUSD", "M15", 200)

    feed = LiveDataFeed(normalizer, symbol="XAUUSD", interval="M15")
    feed_result = feed.get_candles(200)

    assert direct_result == feed_result
    assert calls == [("XAUUSD", "M15", 200), ("XAUUSD", "M15", 200)]
