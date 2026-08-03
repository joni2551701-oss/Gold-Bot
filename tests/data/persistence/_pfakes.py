"""Shared helpers for Persistent Memory Layer tests (module 6)."""

from datetime import datetime, timezone, timedelta

from data_layer.providers.twelve_data_client import Candle
from data_layer.market_memory.market_memory import MarketMemory
from data_layer.market_memory.candle_record import CandleSource


def ts(i, tf_minutes=1):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(
        minutes=i * tf_minutes)


def candle(i, close=100.0, tf_minutes=1):
    t = ts(i, tf_minutes)
    return Candle(timestamp=t, open=close, high=close, low=close, close=close)


def memory_with(asset="XAUUSD", caps=None, m1=5):
    """A MarketMemory hydrated with `m1` contiguous M1 candles."""
    mem = MarketMemory(asset, caps or {"M1": 100})
    mem.timeframe("M1").hydrate([candle(i) for i in range(m1)],
                                source=CandleSource.BOOTSTRAP)
    return mem
