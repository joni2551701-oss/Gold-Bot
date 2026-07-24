"""
Unit tests for data/bootstrap/twelve_data_historical_provider.py (module 5).

Exercises the adapter via an injected fake client (no network): capability
declaration, fetch_recent, and fetch_range filtering.
"""

from datetime import datetime, timezone, timedelta

from data.twelve_data_client import Candle
from data.bootstrap.twelve_data_historical_provider import (
    TwelveDataHistoricalProvider,
)


class _FakeClient:
    def __init__(self, candles):
        self.candles = candles
        self.calls = 0

    def fetch_candles(self, symbol, interval, outputsize=50):
        self.calls += 1
        return self.candles[-outputsize:]


def _c(i):
    t = datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)
    return Candle(timestamp=t, open=i, high=i, low=i, close=i)


def _t(i):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)


def test_capabilities():
    p = TwelveDataHistoricalProvider(client=_FakeClient([]))
    assert p.capabilities.supports_historical is True


def test_fetch_recent_sorted():
    fc = _FakeClient([_c(2), _c(0), _c(1)])
    p = TwelveDataHistoricalProvider(client=fc)
    out = p.fetch_recent("XAUUSD", "M1", 3)
    assert [c.timestamp for c in out] == [_t(0), _t(1), _t(2)]


def test_fetch_range_filters_window():
    fc = _FakeClient([_c(0), _c(1), _c(2), _c(3), _c(4)])
    p = TwelveDataHistoricalProvider(client=fc)
    out = p.fetch_range("XAUUSD", "M1", _t(1), _t(3))
    assert [c.timestamp for c in out] == [_t(1), _t(2)]     # [1,3)
