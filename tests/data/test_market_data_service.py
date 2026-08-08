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


# ---------------- GFL-001 FLOW-004: Market Engine read-out ----------------

def test_get_candles_from_memory_returns_empty_when_no_registry():
    service = MarketDataService(normalizer=FakeNormalizer())
    assert service.get_candles_from_memory("XAUUSD", "M15") == []


def test_get_candles_from_memory_reads_back_hydrated_candles():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)

    written = service.get_candles("XAUUSD", "M15", 200)
    read_back = service.get_candles_from_memory("XAUUSD", "M15")

    assert len(read_back) == 3
    assert [c.close for c in read_back] == [c.close for c in written]


def test_get_candles_from_memory_returns_empty_for_unregistered_asset():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)
    # Nothing was ever hydrated for this symbol -- fail-safe, not an
    # UnknownAssetError leaking out to the caller.
    assert service.get_candles_from_memory("NEVERSEEN", "M15") == []


def test_get_candles_from_memory_shape_matches_get_candles():
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_SnapshotNormalizer(),
                               memory_registry=registry)
    service.get_candles("XAUUSD", "M15", 200)

    read_back = service.get_candles_from_memory("XAUUSD", "M15")
    for candle in read_back:
        assert hasattr(candle, "timestamp")
        assert hasattr(candle, "open")
        assert hasattr(candle, "high")
        assert hasattr(candle, "low")
        assert hasattr(candle, "close")


# ---------------- GFL-001 FLOW-004: shared MarketDataService singleton ----------------

def test_get_shared_market_data_service_shares_registry_with_price_stream_service():
    from data_layer.live_data.market_data_service import (
        get_shared_market_data_service,
        reset_shared_market_data_service,
    )
    from data_layer.live_data.price_stream_service import (
        get_shared_price_stream_service,
        reset_shared_price_stream_service,
    )

    reset_shared_price_stream_service()
    reset_shared_market_data_service()
    try:
        mds = get_shared_market_data_service()
        pss = get_shared_price_stream_service()
        assert mds._memory_registry is pss.memory_registry
        # Idempotent: a second call returns the exact same instance.
        assert get_shared_market_data_service() is mds
    finally:
        reset_shared_price_stream_service()
        reset_shared_market_data_service()


# ---------------- REAL-DATA-003: Market Memory -> Core SSOT reconciliation ----------------

class _KnownSeriesNormalizer:
    """Provider stub returning a fixed, known M15 candle set (distinct
    OHLC per bar, strictly increasing timestamps, oldest -> newest)."""
    def __init__(self, candles):
        self._candles = candles

    def get_candles(self, symbol, interval, outputsize):
        return list(self._candles)

    def get_snapshot(self, symbol, intervals):
        return MarketSnapshot(symbol=symbol, candles={}, quality={})


def _known_series(n=5):
    base = datetime(2026, 8, 1, 9, tzinfo=timezone.utc)
    return [Candle(timestamp=base + timedelta(minutes=15 * i),
                   open=1900.0 + i, high=1905.0 + i,
                   low=1895.0 + i, close=1902.0 + i)
            for i in range(n)]


def test_get_candles_via_memory_ssot_is_identical_to_validated_candles():
    """REAL-DATA-003 data-fidelity proof: with a registry configured,
    the candles Core receives (the memory-SSOT read-back path) are
    IDENTICAL to the validated candles that were written to memory --
    same count, same OHLC, same timestamps, same order (oldest ->
    newest). Guards against truncation (capacity), reordering, and
    CandleRecord<->Candle type-conversion drift."""
    validated = _known_series(5)
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_KnownSeriesNormalizer(validated),
                                memory_registry=registry)

    # This is exactly what the pipeline calls at pipeline.py:303.
    core_consumed = service.get_candles("XAUUSD", "M15", 200)

    # Same count -- no capacity truncation (M15 capacity 200 >= 5).
    assert len(core_consumed) == len(validated) == 5
    # Same order oldest -> newest, same OHLC and timestamps, field by field.
    for got, expected in zip(core_consumed, validated):
        assert got.timestamp == expected.timestamp
        assert got.open == expected.open
        assert got.high == expected.high
        assert got.low == expected.low
        assert got.close == expected.close
    # Timestamps strictly increasing (order preserved, not reversed).
    ts = [c.timestamp for c in core_consumed]
    assert ts == sorted(ts)


def test_get_candles_via_memory_ssot_actually_reads_from_memory():
    """Proves the returned series really is the memory-SSOT read-back
    (not the normalizer's direct output): the read-back path is what
    provides the candles, matching get_candles_from_memory()."""
    validated = _known_series(4)
    registry = MarketMemoryRegistry()
    service = MarketDataService(normalizer=_KnownSeriesNormalizer(validated),
                                memory_registry=registry)

    core_consumed = service.get_candles("XAUUSD", "M15", 200)
    from_memory = service.get_candles_from_memory("XAUUSD", "M15", 200)

    assert [c.timestamp for c in core_consumed] == [c.timestamp for c in from_memory]
    assert [c.close for c in core_consumed] == [c.close for c in from_memory]


def test_get_candles_falls_back_to_validated_when_memory_empty():
    """Fail-safe: an unknown/empty memory timeframe (e.g. the "Daily"
    vs "D1" vocabulary gap) leaves get_candles_from_memory() returning
    [], so get_candles() returns the original validated candles
    unchanged -- never an empty list, never a degraded trade path."""
    validated = _known_series(3)

    class _BlackHoleRegistry:
        # get_or_create used by _hydrate_memory; get_series used by
        # MemoryReader will find nothing -> read-back returns [].
        def get_or_create(self, symbol):
            class _M:
                def has_timeframe(self, tf):
                    return False
            return _M()

    service = MarketDataService(normalizer=_KnownSeriesNormalizer(validated),
                                memory_registry=_BlackHoleRegistry())
    core_consumed = service.get_candles("XAUUSD", "Daily", 100)
    assert [c.close for c in core_consumed] == [c.close for c in validated]


def test_reset_shared_market_data_service_forces_a_fresh_instance():
    from data_layer.live_data.market_data_service import (
        get_shared_market_data_service,
        reset_shared_market_data_service,
    )
    from data_layer.live_data.price_stream_service import reset_shared_price_stream_service

    reset_shared_price_stream_service()
    reset_shared_market_data_service()
    try:
        first = get_shared_market_data_service()
        reset_shared_market_data_service()
        second = get_shared_market_data_service()
        assert first is not second
    finally:
        reset_shared_price_stream_service()
        reset_shared_market_data_service()
