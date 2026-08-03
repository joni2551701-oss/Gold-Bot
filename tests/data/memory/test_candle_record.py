"""
Unit tests for data_layer/market_memory/candle_record.py (MarketMemory Core, module 1).

Covers the DD-027 extended candle model: identity, forming updates,
close immutability, copy-on-read isolation, and reuse interop with the
existing frozen data_layer.providers.twelve_data_client.Candle.
"""

from datetime import datetime, timezone

import pytest

from data_layer.providers.twelve_data_client import Candle
from data_layer.market_memory.candle_record import (
    CandleRecord,
    CandleStatus,
    CandleSource,
)


def _ts(hour=0, minute=0):
    return datetime(2026, 7, 24, hour, minute, tzinfo=timezone.utc)


def _forming(**kw):
    base = dict(
        timestamp=_ts(),
        open=100.0, high=100.0, low=100.0, close=100.0,
        timeframe="M1",
        candle_id="XAUUSD:M1:1",
        sequence_number=1,
    )
    base.update(kw)
    return CandleRecord(**base)


def test_make_candle_id_is_stable():
    ts = _ts(1, 30)
    a = CandleRecord.make_candle_id("XAUUSD", "M15", ts)
    b = CandleRecord.make_candle_id("XAUUSD", "M15", ts)
    assert a == b == f"XAUUSD:M15:{int(ts.timestamp())}"


def test_apply_price_updates_ohlc():
    rec = _forming()
    rec.apply_price(105.0)
    rec.apply_price(95.0)
    rec.apply_price(101.0)
    assert rec.open == 100.0          # open preserved
    assert rec.high == 105.0
    assert rec.low == 95.0
    assert rec.close == 101.0         # close = last price


def test_apply_price_accumulates_volume():
    rec = _forming(volume=None)
    rec.apply_price(101.0, volume=5.0)
    rec.apply_price(102.0, volume=3.0)
    assert rec.volume == 8.0


def test_close_then_apply_price_raises():
    rec = _forming()
    rec.close_candle()
    assert rec.status is CandleStatus.CLOSED
    with pytest.raises(ValueError):
        rec.apply_price(101.0)


def test_copy_is_isolated():
    rec = _forming(metadata={"k": [1, 2]})
    dup = rec.copy()
    dup.apply_price(200.0)
    dup.metadata["k"].append(3)
    # original untouched
    assert rec.close == 100.0
    assert rec.metadata["k"] == [1, 2]


def test_to_candle_reuses_frozen_candle():
    rec = _forming()
    rec.apply_price(110.0)
    candle = rec.to_candle()
    assert isinstance(candle, Candle)
    assert candle.close == 110.0
    assert candle.timestamp == rec.timestamp


def test_from_candle_roundtrip():
    c = Candle(timestamp=_ts(2), open=1.0, high=2.0, low=0.5, close=1.5)
    rec = CandleRecord.from_candle(
        c, asset="XAUUSD", timeframe="H1", sequence_number=7)
    assert rec.status is CandleStatus.CLOSED
    assert rec.source is CandleSource.BOOTSTRAP
    assert rec.close == 1.5
    assert rec.trading_day == c.timestamp.date()
    assert rec.candle_id == f"XAUUSD:H1:{int(c.timestamp.timestamp())}"
