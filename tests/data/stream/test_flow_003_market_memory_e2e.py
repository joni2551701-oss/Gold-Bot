"""GFL-001 FLOW-003 (Market Memory) -- end-to-end integration test.

Exercises the full documented chain in one test:

    Provider Factory (a PriceProvider)
      -> Price Stream (PriceStreamService.tick(), via the shared,
         process-wide singleton)
      -> Data Validation (StreamValidator, wired by default)
      -> Market Memory (MarketMemoryRegistry, fed via the single-writer
         CandleBuilder; reached through the public
         PriceStreamService.memory_registry accessor -- GFL-001
         FLOW-003's Consumer read seam, not a private-attribute
         reach-in)
      -> Consumer (data_layer.market_memory.MemoryReader, the
         canonical read facade "every future client reads market data
         through"; and data_layer.live_data.market.market_manager
         .MarketManager, the facade layer for future chart/ai/
         platform/telegram/monitoring consumers)

A bad/invalid tick is also driven through the same chain to confirm
Data Validation drops it before it ever reaches Market Memory or a
Consumer.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from data_layer.live_data.price_stream_service import (
    get_shared_price_stream_service,
    reset_shared_price_stream_service,
)
from data_layer.market_memory import MemoryReader
from data_layer.live_data.market.market_manager import MarketManager

from _fakes import FakeProvider, event, ts

_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def setup_function():
    reset_shared_price_stream_service()


def teardown_function():
    reset_shared_price_stream_service()


def test_flow_003_full_chain_reaches_a_real_consumer():
    # Producer: a fresh symbol driven by a fake provider (no network).
    service = get_shared_price_stream_service()
    provider = FakeProvider()
    service.register_source("FLOWMEM", provider, provider_name="fake")

    # Consumer (MemoryReader): registering the source eagerly creates
    # the asset's MarketMemory (so a CandleBuilder has somewhere to
    # write), but genuinely no candle data exists before any tick.
    reader = MemoryReader(service.memory_registry)
    assert "FLOWMEM" in reader.assets()
    assert reader.get_forming("FLOWMEM", "M1") is None

    # Price Stream + Data Validation: advance to STREAMING, then push a
    # valid tick through the default-wired StreamValidator.
    service.tick(ts(0))   # INITIALIZING -> CONNECTING
    service.tick(ts(1))   # CONNECTING -> STREAMING
    provider.batches.append([event(asset="FLOWMEM", price=2044.75, i=2)])
    service.tick(ts(4))

    # Output: Market Memory now holds the validated tick as an M1
    # forming candle, read through the canonical Consumer contract.
    forming = reader.get_forming("FLOWMEM", "M1")
    assert forming is not None
    assert forming.close == 2044.75

    # Consumer (MarketManager): the facade layer for chart/ai/platform/
    # telegram/monitoring projects a MarketData carrying that same
    # price, reading Market Memory through MemoryReader -- not a
    # second, parallel data path.
    schema = SimpleNamespace(symbol="FLOWMEM", timeframe="M1", regime="TRENDING")
    data = MarketManager().build_market_data(schema, memory_reader=reader, now=_WEEKDAY)
    assert data.price == 2044.75


def test_flow_003_invalid_tick_never_reaches_market_memory_or_consumer():
    """A non-positive price must never reach Market Memory or a
    Consumer -- StreamValidator (Data Validation) drops it first."""
    from data_layer.live_data.stream_validator import StreamValidator

    service = get_shared_price_stream_service()
    provider = FakeProvider()
    service.register_source("FLOWMEMBAD", provider, provider_name="fake",
                             validator=StreamValidator())
    reader = MemoryReader(service.memory_registry)

    service.tick(ts(0)); service.tick(ts(1))
    provider.batches.append([event(asset="FLOWMEMBAD", price=-1.0, i=2)])
    service.tick(ts(4))

    assert reader.get_forming("FLOWMEMBAD", "M1") is None

    schema = SimpleNamespace(symbol="FLOWMEMBAD", timeframe="M1", regime="RANGE")
    data = MarketManager().build_market_data(schema, memory_reader=reader, now=_WEEKDAY)
    assert data.current_price is None
