"""Unit tests for data/stream/price_stream_service.py (TASK-DATA-001)."""

from data.events.event_bus import EventBus
from data.events.event_model import EventType
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
