"""
Unit tests for data/memory/market_memory.py (MarketMemory Core).

Covers per-asset timeframe ownership, LIVE/REPLAY mode (DD-033),
independent timeframes, and health aggregation.
"""

import pytest

from data.memory.market_memory import MarketMemory
from data.memory.candle_record import MemoryMode


def _mem():
    return MarketMemory("XAUUSD", {"M1": 100, "M15": 50, "H4": 20})


def test_requires_asset_and_timeframes():
    with pytest.raises(ValueError):
        MarketMemory("", {"M1": 10})
    with pytest.raises(ValueError):
        MarketMemory("XAUUSD", {})


def test_timeframes_listed():
    m = _mem()
    assert set(m.timeframes()) == {"M1", "M15", "H4"}
    assert m.has_timeframe("M1")
    assert not m.has_timeframe("D1")


def test_unknown_timeframe_raises():
    m = _mem()
    with pytest.raises(KeyError):
        m.timeframe("D1")


def test_timeframes_are_independent():
    m = _mem()
    m.timeframe("M1").open_candle(__import__("datetime").datetime(
        2026, 7, 24, tzinfo=__import__("datetime").timezone.utc), 100.0)
    # M1 has a forming candle; M15 does not
    assert m.timeframe("M1").get_forming() is not None
    assert m.timeframe("M15").get_forming() is None


def test_mode_default_live_and_switch():
    m = _mem()
    assert m.mode is MemoryMode.LIVE
    m.set_mode(MemoryMode.REPLAY)
    assert m.mode is MemoryMode.REPLAY


def test_set_mode_type_checked():
    m = _mem()
    with pytest.raises(TypeError):
        m.set_mode("replay")


def test_health_aggregates_all_timeframes():
    m = _mem()
    h = m.health()
    assert h["asset"] == "XAUUSD"
    assert h["mode"] == "live"
    assert set(h["timeframes"]) == {"M1", "M15", "H4"}
    assert h["timeframes"]["M1"]["capacity"] == 100
