"""GFL-001 FLOW-004 (Market Engine) -- end-to-end integration test.

Proves the full chain required by Director Order GFL-004:

    Provider -> Validation -> Market Memory -> Market Engine

`get_shared_price_stream_service()` (FLOW-001/003) is the Producer
side: it validates ticks (`StreamValidator`) and folds them into the
shared `MarketMemoryRegistry` via `CandleBuilder`. `MarketDataService
.get_candles_from_memory()` / `get_shared_market_data_service()`
(FLOW-004, Market Engine) is the read-out side: it reads the SAME
live registry through the canonical `MemoryReader` facade and returns
closed candles shaped exactly like `MarketDataService.get_candles()`'s
own return value (`data_layer.providers.twelve_data_client.Candle` --
timestamp/open/high/low/close only) -- ready for
`context.context_orchestrator.ContextEngine.build()`'s existing,
unmodified `candles` contract (not exercised here -- that call belongs
to FLOW-005, out of this Flow's scope).

M5 is used (not M1): `TwelveDataProvider` only accepts GoldBot's
supported intervals (M5/M15/H1/H4/Daily); M5 is Market Memory's
shortest timeframe that is also a real, supported provider interval.

The first two `tick()` calls with no queued batch are the same
warm-up FLOW-001/FLOW-003's E2E tests use: a freshly registered
`PriceStream` starts CONNECTING and only reaches STREAMING (where it
actually reads a provider batch) on a later tick.

Uses the same `_fakes.py` helpers as the FLOW-001/FLOW-003 E2E tests
(same-directory import, pytest's rootdir-relative collection).
"""

from data_layer.live_data.market_data_service import (
    get_shared_market_data_service,
    reset_shared_market_data_service,
)
from data_layer.live_data.price_stream_service import (
    get_shared_price_stream_service,
    reset_shared_price_stream_service,
)

from _fakes import FakeProvider, event, ts


def setup_function():
    reset_shared_price_stream_service()
    reset_shared_market_data_service()


def teardown_function():
    reset_shared_price_stream_service()
    reset_shared_market_data_service()


def test_flow_004_full_chain_reaches_market_engine_as_a_closed_candle():
    service = get_shared_price_stream_service()
    provider = FakeProvider()
    service.register_source("FLOWENGINE", provider, provider_name="fake")

    market_data = get_shared_market_data_service()
    # Genuinely empty before any tick -- no candle has ever formed.
    assert market_data.get_candles_from_memory("FLOWENGINE", "M5") == []

    # Warm-up: a freshly registered stream is CONNECTING, not yet
    # STREAMING -- these two ticks carry no batch and open nothing.
    service.tick(ts(0))
    service.tick(ts(1))

    # Now STREAMING: opens a forming M5 candle at the 13:00 window.
    provider.batches.append([event(asset="FLOWENGINE", price=2050.0, i=2)])
    service.tick(ts(4))

    # A tick >= 5 minutes later crosses the M5 window boundary ->
    # closes the 13:00 candle (close = 2050.0, the last price before
    # the crossing tick) and opens a new forming candle.
    provider.batches.append([event(asset="FLOWENGINE", price=2060.0, i=305)])
    service.tick(ts(310))

    candles = market_data.get_candles_from_memory("FLOWENGINE", "M5")
    assert len(candles) == 1
    assert candles[0].close == 2050.0
    assert candles[0].open == 2050.0

    # An asset nobody registered/ticked stays honestly empty.
    assert market_data.get_candles_from_memory("NEVERSEEN", "M5") == []


def test_flow_004_invalid_tick_never_reaches_market_engine_output():
    from data_layer.live_data.stream_validator import StreamValidator

    service = get_shared_price_stream_service()
    provider = FakeProvider()
    service.register_source("FLOWENGINEBAD", provider, provider_name="fake",
                             validator=StreamValidator())

    service.tick(ts(0))
    service.tick(ts(1))
    provider.batches.append([event(asset="FLOWENGINEBAD", price=-1.0, i=2)])
    service.tick(ts(4))

    market_data = get_shared_market_data_service()
    assert market_data.get_candles_from_memory("FLOWENGINEBAD", "M5") == []
