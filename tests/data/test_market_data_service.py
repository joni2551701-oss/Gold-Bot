"""Unit tests for data_layer/live_data/market_data_service.py (TASK-DATA-001, Phase 2;
TASK-DATA-004 MarketMemory hydrate wiring)."""

from datetime import datetime, timedelta, timezone

from data_layer.live_data.market_data import MarketSnapshot
from data_layer.live_data.market_data_service import MarketDataService
from data_layer.market_memory import MarketMemoryRegistry
from data_layer.providers.twelve_data_client import Candle


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
        "data_layer.historical_data.historical_data_collector.collect_historical_candles", fake_collect
    )

    service = MarketDataService()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 2, tzinfo=timezone.utc)
    result = service.get_historical_candles(
        "XAUUSD", "H1", start, end, provider="fake-provider"
    )

    assert result == "RESULT"
    assert calls == [("fake-provider", "XAUUSD", "H1", start, end)]


# ---------------- TASK-DATA-004: MarketMemory hydrate wiring ----------------

def _m15_candles(n=3):
    base = datetime(2026, 7, 24, 13, tzinfo=timezone.utc)
    return [Candle(timestamp=base + timedelta(minutes=15 * i),
                   open=1.0 + i, high=2.0 + i, low=0.5 + i, close=1.5 + i)
            for i in range(n)]


class _SnapshotNormalizer:
    """Returns a real multi-timeframe snapshot for hydrate tests."""
    def get_candles(self, symbol, interval, outputsize):
        return _m15_candles()

    def get_snapshot(self, symbol, intervals):
        candles = {tf: _m15_candles() for tf in intervals if tf != "Daily"}
        return MarketSnapshot(symbol=symbol, candles=candles,
                              quality={tf: "OK" for tf in candles})


def test_get_candles_hydrates_market_memory_when_registry_supplied():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)

    returned = service.get_candles("XAUUSD", "M15", 200)

    # return value is unchanged (still the fetched candles)...
    assert len(returned) == 3
    # ...and the same closed candles were hydrated into MarketMemory.
    mem = registry.get("XAUUSD").timeframe("M15")
    assert mem.closed_count() == 3
    assert mem.get_last_closed().close == returned[-1].close


def test_get_snapshot_hydrates_each_known_timeframe():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)

    service.get_snapshot("XAUUSD", ["M15", "H1", "H4"])

    mem = registry.get("XAUUSD")
    assert mem.timeframe("M15").closed_count() == 3
    assert mem.timeframe("H1").closed_count() == 3
    assert mem.timeframe("H4").closed_count() == 3


def test_unknown_timeframe_daily_is_skipped_not_errored():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)

    # "Daily" is not a MarketMemory timeframe (memory uses "D1"); must be
    # silently skipped, and the call must still return normally.
    snap = service.get_snapshot("XAUUSD", ["Daily", "M15"])
    assert snap.symbol == "XAUUSD"
    mem = registry.get("XAUUSD")
    assert not mem.has_timeframe("Daily")
    assert mem.timeframe("M15").closed_count() == 3


def test_hydrate_is_fail_safe_never_breaks_get_candles():
    class _BrokenRegistry:
        def get_or_create(self, symbol):
            raise RuntimeError("boom")

    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=_BrokenRegistry())
    # Memory write blows up internally but get_candles still returns data.
    returned = service.get_candles("XAUUSD", "M15", 200)
    assert len(returned) == 3


def test_default_no_registry_writes_no_memory():
    normalizer = FakeNormalizer()
    service = MarketDataService(normalizer=normalizer)
    # No registry -> no memory attribute wiring; behavior identical to Phase 2.
    assert service._memory_registry is None
    candles = service.get_candles("XAUUSD", "M15", 200)
    assert len(candles) == 1
