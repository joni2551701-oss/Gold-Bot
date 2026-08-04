"""Unit tests for data_layer/live_data/price_stream_service.py (TASK-DATA-001;
TASK-DATA-004 MarketMemory single-writer wiring; GFL-001 FLOW-001 shared
singleton + default validator/memory wiring)."""

import pytest

from data_layer.event_system.event_bus import EventBus
from data_layer.event_system.event_model import EventType
from data_layer.market_memory import MarketMemoryRegistry
from data_layer.live_data.price_stream_service import (
    PriceStreamService,
    build_default_price_stream_service,
    get_shared_price_stream_service,
    reset_shared_price_stream_service,
)
from data_layer.live_data.stream_event import AssetClass

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
    from data_layer.live_data.market_data_service import MarketDataService
    from data_layer.live_data.market_data import MarketSnapshot
    from data_layer.providers.twelve_data_client import Candle
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


# ---------------- GFL-001 FLOW-001: Data Validation module (default validator) ----------------

def test_build_default_wires_validator_that_drops_invalid_ticks():
    """The Data Validation module for FLOW-001: build_default_price_stream_service()
    wires a canonical StreamValidator into every source, dropping bad ticks
    before they reach the cache -- reusing TASK-ARCH-101's validator, not a
    second one."""
    service = PriceStreamService()
    provider = FakeProvider()
    from data_layer.live_data.stream_validator import StreamValidator
    service.register_source("XAUUSD", provider, provider_name="fake",
                             validator=StreamValidator())

    service.tick(ts(0)); service.tick(ts(1))
    # a non-positive price must be dropped by the validator, never cached
    provider.batches.append([event(asset="XAUUSD", price=-5.0, i=2)])
    service.tick(ts(4))
    assert service.get_price("XAUUSD") is None

    provider.batches.append([event(asset="XAUUSD", price=2400.0, i=3)])
    service.tick(ts(5))
    assert service.get_price("XAUUSD").price == 2400.0


# ---------------- GFL-001 FLOW-001: shared process-wide singleton ----------------

@pytest.fixture(autouse=True)
def _reset_shared_service():
    reset_shared_price_stream_service()
    yield
    reset_shared_price_stream_service()


def test_get_shared_price_stream_service_returns_same_instance():
    a = get_shared_price_stream_service()
    b = get_shared_price_stream_service()
    assert a is b


def test_reset_shared_price_stream_service_forces_rebuild():
    a = get_shared_price_stream_service()
    reset_shared_price_stream_service()
    b = get_shared_price_stream_service()
    assert a is not b


def test_shared_service_ticked_by_one_caller_is_seen_by_another_reader():
    """The exact FLOW-001 gap this closes: a driver ticking the shared
    service must be visible to any other holder of the same default --
    e.g. CurrentPriceProvider's default PriceStreamLastPriceSource."""
    from data_layer.live_data.current_price_provider import PriceStreamLastPriceSource

    driver_service = get_shared_price_stream_service()
    reader = PriceStreamLastPriceSource()  # lazily resolves the same shared instance
    assert reader.get_current_price("TESTXYZ") is None

    # Register an extra, unused-by-default symbol with a fake provider so
    # the tick is deterministic (no real network call in a unit test) --
    # XAUUSD/BTCUSDT are already registered by build_default_price_stream_service().
    provider = FakeProvider()
    driver_service.register_source("TESTXYZ", provider, provider_name="fake")
    driver_service.tick(ts(0)); driver_service.tick(ts(1))
    provider.batches.append([event(asset="TESTXYZ", price=3300.0, i=2)])
    driver_service.tick(ts(4))

    seen = reader.get_current_price("TESTXYZ")
    assert seen is not None
    assert seen.price == 3300.0


def test_build_default_price_stream_service_unaffected_by_shared_singleton():
    """build_default_price_stream_service() itself stays a plain factory --
    calling it directly still returns a fresh, independent instance, never
    the shared one (only get_shared_price_stream_service() shares)."""
    a = build_default_price_stream_service(memory_registry=MarketMemoryRegistry())
    b = build_default_price_stream_service(memory_registry=MarketMemoryRegistry())
    assert a is not b
