"""
REAL-DATA-008 -- unit tests for
data_layer/live_data/twelve_data_price_source.py::TwelveDataPriceSource.

Exercises the adapter via an injected fake client (no network / no key):
capabilities, connect/disconnect status, and that read() returns a
StreamEvent carrying the REAL current price (from client.get_price, NOT a
candle close) with a fresh observation timestamp and source=STREAM.
"""

from datetime import datetime, timezone

from data_layer.live_data.twelve_data_price_source import TwelveDataPriceSource
from data_layer.live_data.stream_event import ProviderStatus
from data_layer.market_memory.candle_record import CandleSource


class _FakeClient:
    def __init__(self, price=None):
        self.price = price
        self.calls = []

    def get_price(self, symbol):
        self.calls.append(symbol)
        return self.price


def test_capabilities_declared_polling_not_streaming():
    p = TwelveDataPriceSource("XAUUSD", client=_FakeClient())
    caps = p.capabilities
    assert caps.supports_polling is True
    assert caps.supports_streaming is False


def test_connect_disconnect_status():
    p = TwelveDataPriceSource("XAUUSD", client=_FakeClient())
    assert p.status() is ProviderStatus.DOWN
    p.connect()
    assert p.status() is ProviderStatus.UP
    p.disconnect()
    assert p.status() is ProviderStatus.DOWN


def test_read_returns_current_price_event_with_observation_timestamp():
    fc = _FakeClient(price=2412.5)
    p = TwelveDataPriceSource("XAUUSD", client=fc)
    p.connect()
    before = datetime.now(timezone.utc)
    events = p.read()
    after = datetime.now(timezone.utc)

    assert len(events) == 1
    ev = events[0]
    assert ev.price == 2412.5            # real current price, not candle close
    assert ev.asset == "XAUUSD"
    assert ev.source is CandleSource.STREAM
    assert ev.timestamp.tzinfo is not None
    assert before <= ev.timestamp <= after   # fresh observation timestamp
    assert fc.calls == ["XAUUSD"]        # source reads via client.get_price


def test_read_empty_when_no_price():
    p = TwelveDataPriceSource("XAUUSD", client=_FakeClient(price=None))
    p.connect()
    assert p.read() == []


def test_read_does_not_dedupe_repeated_price():
    """A repeated identical current price is a valid tick (unchanged value
    is fine) -- each read is one fresh observation, never de-duplicated."""
    fc = _FakeClient(price=2400.0)
    p = TwelveDataPriceSource("XAUUSD", client=fc)
    p.connect()
    first = p.read()
    second = p.read()
    assert len(first) == 1
    assert len(second) == 1
    assert first[0].price == second[0].price == 2400.0
