"""Unit tests for data/market_data_service.py (TASK-DATA-001, Phase 2)."""

from datetime import datetime, timezone

from data.market_data import MarketSnapshot
from data.market_data_service import MarketDataService
from data.twelve_data_client import Candle


class FakeNormalizer:
    def __init__(self):
        self.get_candles_calls = []
        self.get_snapshot_calls = []

    def get_candles(self, symbol, interval, outputsize):
        self.get_candles_calls.append((symbol, interval, outputsize))
        return [Candle(timestamp=datetime(2026, 7, 24, 13, tzinfo=timezone.utc),
                        open=1.0, high=2.0, low=0.5, close=1.5)]

    def get_snapshot(self, symbol, intervals):
        self.get_snapshot_calls.append((symbol, tuple(intervals)))
        return MarketSnapshot(symbol=symbol, candles={}, quality={})


def test_get_candles_delegates_to_normalizer_unchanged():
    normalizer = FakeNormalizer()
    service = MarketDataService(normalizer=normalizer)

    candles = service.get_candles("XAUUSD", "M15", 200)

    assert normalizer.get_candles_calls == [("XAUUSD", "M15", 200)]
    assert len(candles) == 1
    assert candles[0].close == 1.5


def test_get_snapshot_delegates_to_normalizer_unchanged():
    normalizer = FakeNormalizer()
    service = MarketDataService(normalizer=normalizer)

    snapshot = service.get_snapshot("XAUUSD", ["Daily", "H4", "H1"])

    assert normalizer.get_snapshot_calls == [("XAUUSD", ("Daily", "H4", "H1"))]
    assert snapshot.symbol == "XAUUSD"


def test_defaults_to_a_real_market_data_normalizer():
    service = MarketDataService()
    assert service._normalizer is not None


def test_get_historical_candles_delegates_to_collector(monkeypatch):
    calls = []

    def fake_collect(provider, symbol, timeframe, start, end):
        calls.append((provider, symbol, timeframe, start, end))
        return "RESULT"

    monkeypatch.setattr(
        "data.historical_data_collector.collect_historical_candles", fake_collect
    )

    service = MarketDataService()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 2, tzinfo=timezone.utc)
    result = service.get_historical_candles(
        "XAUUSD", "H1", start, end, provider="fake-provider"
    )

    assert result == "RESULT"
    assert calls == [("fake-provider", "XAUUSD", "H1", start, end)]
