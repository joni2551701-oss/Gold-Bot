"""
Integration test: PriceStream -> CandleBuilder -> MarketMemory
(v1.1 Phase 1, module 4 wired to modules 1-3).

Verifies the stream feeds real StreamEvents through the real CandleBuilder
into real MarketMemory, single-writer, with candles readable via
MemoryReader.
"""

from data_layer.live_data.price_stream import PriceStream, AlwaysOpenCalendar
from data_layer.live_data.stream_event import StreamState, AssetClass
from data_layer.live_data.candle_builder import CandleBuilder
from data_layer.market_memory.market_memory_registry import MarketMemoryRegistry
from data_layer.market_memory.memory_reader import MemoryReader
from _fakes import FakeProvider, event, ts


def test_stream_builds_candles_into_memory():
    reg = MarketMemoryRegistry()
    memory = reg.register("XAUUSD", {"M1": 100})
    builder = CandleBuilder("XAUUSD", memory)     # real sink
    reader = MemoryReader(reg)

    provider = FakeProvider()
    stream = PriceStream("XAUUSD", provider, builder,
                         calendar=AlwaysOpenCalendar(),
                         asset_class=AssetClass.CRYPTO)

    stream.tick(ts(0))                             # CONNECTING
    assert stream.tick(ts(1)) is StreamState.STREAMING

    # two ticks in the same M1 window (13:00:00 and 13:00:30)
    provider.batches.append([event(price=100.0, i=0),
                             event(price=105.0, i=30)])
    stream.tick(ts(31))

    forming = reader.get_forming("XAUUSD", "M1")
    assert forming is not None
    assert forming.open == 100.0
    assert forming.high == 105.0
    assert forming.close == 105.0
    assert builder.stats()["processed"] == 2
