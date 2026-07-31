"""Unit tests for data/stream/price_stream_service.py (TASK-DATA-001;
TASK-DATA-004 MarketMemory single-writer wiring)."""

from data.events.event_bus import EventBus
from data.events.event_model import EventType
from data.memory import MarketMemoryRegistry
from data.stream.price_stream_service import PriceStreamService
from data.stream.stream_event import AssetClass

from _fakes import FakeProvider, event, ts


def test_get_price_none_before_any_tick():
    service = PriceStreamService()
    service.register_source("XAUUSD", FakeProvider(), provider_name="fake")
    assert service.get_price("XAUUSD") is None


def test_tick_updates_cache_with_unified_price_tick():
    service = PriceStreamService()
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata",
                             asset_class=AssetClass.METAL)

    service.tick(ts(0))   # INITIALIZING -> CONNECTING
    service.tick(ts(1))   # CONNECTING -> STREAMING (provider connects)
    provider.batches.append([event(asset="XAUUSD", price=2400.5, i=2)])
    service.tick(ts(4))

    tick = service.get_price("XAUUSD")
    assert tick is not None
    assert tick.symbol == "XAUUSD"
    assert tick.price == 2400.5
    assert tick.provider == "twelvedata"


def test_get_price_normalizes_symbol_case():
    service = PriceStreamService()
    provider = FakeProvider()
    service.register_source("BTCUSDT", provider, provider_name="bitget",
                             asset_class=AssetClass.CRYPTO)
    service.tick(ts(0)); service.tick(ts(1))
    provider.batches.append([event(asset="BTCUSDT", price=65000.0, i=2)])
    service.tick(ts(4))

    assert service.get_price("btcusdt").price == 65000.0


def test_publishes_price_updated_event():
    bus = EventBus()
    received = []
    bus.subscribe(EventType.PRICE_UPDATED, lambda e: received.append(e))

    service = PriceStreamService(event_bus=bus)
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata")
    service.tick(ts(0)); service.tick(ts(1))
    provider.batches.append([event(asset="XAUUSD", price=2400.0, i=2)])
    service.tick(ts(4))

    assert len(received) == 1
    assert received[0].type is EventType.PRICE_UPDATED
    assert received[0].payload.symbol == "XAUUSD"
    assert received[0].asset == "XAUUSD"


def test_two_independent_symbols_do_not_clobber_each_other():
    service = PriceStreamService()
    gold = FakeProvider()
    btc = FakeProvider()
    service.register_source("XAUUSD", gold, provider_name="twelvedata",
                             asset_class=AssetClass.METAL)
    service.register_source("BTCUSDT", btc, provider_name="bitget",
                             asset_class=AssetClass.CRYPTO)

    service.tick(ts(0)); service.tick(ts(1))
    gold.batches.append([event(asset="XAUUSD", price=2400.0, i=2)])
    btc.batches.append([event(asset="BTCUSDT", price=65000.0, i=2)])
    service.tick(ts(4))

    assert service.get_price("XAUUSD").price == 2400.0
    assert service.get_price("BTCUSDT").price == 65000.0


def test_health_and_shutdown_delegate_to_manager():
    service = PriceStreamService()
    service.register_source("XAUUSD", FakeProvider(), provider_name="fake")
    health = service.health()
    assert "XAUUSD" in health
    result = service.shutdown(ts(0))
    assert "XAUUSD" in result


# ---------------- TASK-DATA-004: MarketMemory single-writer wiring ----------------

def _drive_one_tick(service, provider, asset, price):
    service.tick(ts(0))   # INITIALIZING -> CONNECTING
    service.tick(ts(1))   # CONNECTING -> STREAMING
    provider.batches.append([event(asset=asset, price=price, i=2)])
    service.tick(ts(4))


def test_tick_folds_into_market_memory_via_candle_builder():
    registry = MarketMemoryRegistry()
    service = PriceStreamService(memory_registry=registry)
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata")

    _drive_one_tick(service, provider, "XAUUSD", 2400.5)

    # The tick both updated the PriceCache AND folded into MarketMemory.
    assert service.get_price("XAUUSD").price == 2400.5
    forming = registry.get("XAUUSD").timeframe("M1").get_forming()
    assert forming is not None
    assert forming.close == 2400.5


def test_price_cache_and_events_still_work_alongside_memory():
    bus = EventBus()
    received = []
    bus.subscribe(EventType.PRICE_UPDATED, lambda e: received.append(e))

    registry = MarketMemoryRegistry()
    service = PriceStreamService(event_bus=bus, memory_registry=registry)
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata")

    _drive_one_tick(service, provider, "XAUUSD", 2400.0)

    assert len(received) == 1                       # event still published
    assert service.get_price("XAUUSD").price == 2400.0  # cache still updated
    assert registry.get("XAUUSD").timeframe("M1").get_forming() is not None


def test_memory_write_is_fail_safe_for_cache_and_events():
    class _BrokenRegistry:
        def get_or_create(self, symbol):
            raise RuntimeError("boom")

    # A registry that fails at wire time degrades to no memory writer;
    # the stream still registers and the cache path still works.
    service = PriceStreamService(memory_registry=_BrokenRegistry())
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata")

    _drive_one_tick(service, provider, "XAUUSD", 2400.0)
    assert service.get_price("XAUUSD").price == 2400.0


def test_default_no_registry_constructs_no_memory():
    service = PriceStreamService()
    assert service._memory_registry is None
    provider = FakeProvider()
    service.register_source("XAUUSD", provider, provider_name="twelvedata")
    _drive_one_tick(service, provider, "XAUUSD", 2400.0)
    # Cache path unchanged, no memory involved.
    assert service.get_price("XAUUSD").price == 2400.0


def test_shared_registry_is_single_source_of_truth_for_both_services():
    """MarketDataService (hydrate) and PriceStreamService (tick) writing
    into ONE shared registry land in the same MarketMemory."""
    from data.market_data_service import MarketDataService
    from data.market_data import MarketSnapshot
    from data.twelve_data_client import Candle
    from datetime import datetime, timezone

    registry = MarketMemoryRegistry()

    class _N:
        def get_candles(self, symbol, interval, outputsize):
            return [Candle(timestamp=datetime(2026, 7, 24, 13, tzinfo=timezone.utc),
                           open=1, high=2, low=0.5, close=1.5)]
        def get_snapshot(self, symbol, intervals):
            return MarketSnapshot(symbol=symbol, candles={}, quality={})

    mds = MarketDataService(normalizer=_N(), memory_registry=registry)
    mds.get_candles("XAUUSD", "M15", 10)          # hydrates M15 closed history

    pss = PriceStreamService(memory_registry=registry)
    provider = FakeProvider()
    pss.register_source("XAUUSD", provider, provider_name="twelvedata")
    _drive_one_tick(pss, provider, "XAUUSD", 2400.5)   # folds live tick into M1

    mem = registry.get("XAUUSD")
    assert mem.timeframe("M15").closed_count() == 1      # from MarketDataService
    assert mem.timeframe("M1").get_forming().close == 2400.5  # from PriceStreamService
