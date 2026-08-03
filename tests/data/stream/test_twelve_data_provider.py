"""
Unit tests for data_layer/live_data/twelve_data_provider.py (v1.1 Phase 1, module 4).

Exercises the adapter's conversion logic via an injected fake client (no
network / no API key): capabilities, connect/disconnect status, latest
candle -> StreamEvent, and de-duplication.
"""

from datetime import datetime, timezone, timedelta

from data_layer.providers.twelve_data_client import Candle
from data_layer.live_data.twelve_data_provider import TwelveDataProvider
from data_layer.live_data.stream_event import ProviderStatus
from data_layer.market_memory.candle_record import CandleSource


class _FakeClient:
    def __init__(self):
        self.candles = []

    def fetch_candles(self, symbol, interval, outputsize=1):
        return self.candles[-outputsize:]


def _c(i, close):
    ts = datetime(2026, 7, 24, 13, tzinfo=timezone.utc) + timedelta(minutes=i)
    return Candle(timestamp=ts, open=close, high=close, low=close, close=close)


def test_capabilities_declared():
    p = TwelveDataProvider("XAUUSD", client=_FakeClient())
    caps = p.capabilities
    assert caps.supports_polling is True
    assert caps.supports_historical is True
    assert caps.supports_streaming is False


def test_connect_disconnect_status():
    p = TwelveDataProvider("XAUUSD", client=_FakeClient())
    assert p.status() is ProviderStatus.DOWN
    p.connect()
    assert p.status() is ProviderStatus.UP
    p.disconnect()
    assert p.status() is ProviderStatus.DOWN


def test_read_converts_latest_candle_to_event():
    fc = _FakeClient()
    fc.candles = [_c(0, 100.0), _c(1, 101.0)]
    p = TwelveDataProvider("XAUUSD", client=fc)
    p.connect()
    events = p.read()
    assert len(events) == 1
    assert events[0].price == 101.0
    assert events[0].asset == "XAUUSD"
    assert events[0].source is CandleSource.STREAM


def test_read_deduplicates_same_candle():
    fc = _FakeClient()
    fc.candles = [_c(0, 100.0)]
    p = TwelveDataProvider("XAUUSD", client=fc)
    p.connect()
    assert len(p.read()) == 1
    assert p.read() == []               # same latest candle -> no new event
    fc.candles.append(_c(1, 102.0))
    assert len(p.read()) == 1           # newer candle -> emitted


def test_read_empty_when_no_candles():
    p = TwelveDataProvider("XAUUSD", client=_FakeClient())
    p.connect()
    assert p.read() == []
