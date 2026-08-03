"""
Unit tests for data_layer/market_memory/memory_reader.py (MarketMemory Core, module 2).

Covers the DD-031 read facade over a MarketMemoryRegistry: discovery,
candle reads (copy-on-read), revision/mode/health, read-only guarantee,
and the deferred subscribe/unsubscribe/snapshot surface.
"""

from datetime import datetime, timezone, timedelta

import pytest

from data_layer.market_memory.market_memory_registry import MarketMemoryRegistry
from data_layer.market_memory.memory_reader import MemoryReader
from data_layer.market_memory.candle_record import MemoryMode, CandleStatus


def _ts(i):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)


def _reader_with_data():
    reg = MarketMemoryRegistry()
    reg.register("XAUUSD", {"M1": 100, "H4": 50})
    reader = MemoryReader(reg)
    tfm = reg.get("XAUUSD").timeframe("M1")
    for i in range(3):
        tfm.open_candle(_ts(i), float(i))
        tfm.close_forming()
    tfm.open_candle(_ts(3), 3.0)   # leave one forming
    return reg, reader


def test_requires_registry():
    with pytest.raises(ValueError):
        MemoryReader(None)


def test_discovery():
    reg, reader = _reader_with_data()
    assert reader.assets() == ["XAUUSD"]
    assert set(reader.timeframes("XAUUSD")) == {"M1", "H4"}
    assert reader.mode("XAUUSD") is MemoryMode.LIVE


def test_get_last_candle_prefers_forming():
    reg, reader = _reader_with_data()
    last = reader.get_last_candle("XAUUSD", "M1")
    assert last.status is CandleStatus.FORMING
    assert last.open == 3.0


def test_get_last_closed_and_forming():
    reg, reader = _reader_with_data()
    assert reader.get_last_closed("XAUUSD", "M1").open == 2.0
    assert reader.get_forming("XAUUSD", "M1").open == 3.0
    # H4 has no data
    assert reader.get_last_closed("XAUUSD", "H4") is None
    assert reader.get_forming("XAUUSD", "H4") is None


def test_get_series_and_include_forming():
    reg, reader = _reader_with_data()
    closed = reader.get_series("XAUUSD", "M1")
    assert [c.open for c in closed] == [0.0, 1.0, 2.0]
    with_forming = reader.get_series("XAUUSD", "M1", include_forming=True)
    assert len(with_forming) == 4
    assert with_forming[-1].status is CandleStatus.FORMING
    assert reader.get_series("XAUUSD", "M1", n=1) == closed[-1:]


def test_revision_and_health():
    reg, reader = _reader_with_data()
    assert reader.revision("XAUUSD", "M1") > 0
    health = reader.health("XAUUSD")
    assert health["asset"] == "XAUUSD"
    assert set(health["timeframes"]) == {"M1", "H4"}


def test_copy_on_read_isolation_through_reader():
    reg, reader = _reader_with_data()
    snap = reader.get_forming("XAUUSD", "M1")
    snap.apply_price(999.0)
    assert reader.get_forming("XAUUSD", "M1").close == 3.0


def test_reader_is_read_only():
    # No write methods leak through the facade.
    reg, reader = _reader_with_data()
    for attr in ("open_candle", "update_forming", "close_forming",
                 "hydrate", "set_mode", "register"):
        assert not hasattr(reader, attr)


def test_unknown_asset_and_timeframe_raise():
    reg, reader = _reader_with_data()
    with pytest.raises(KeyError):
        reader.get_series("BTCUSD", "M1")
    with pytest.raises(KeyError):
        reader.get_series("XAUUSD", "D1")


def test_deferred_surface_raises_not_implemented():
    reg, reader = _reader_with_data()
    with pytest.raises(NotImplementedError):
        reader.subscribe("XAUUSD", "M1", lambda e: None)
    with pytest.raises(NotImplementedError):
        reader.unsubscribe(object())
    with pytest.raises(NotImplementedError):
        reader.snapshot("XAUUSD")
