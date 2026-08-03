"""
Unit tests for data_layer/market_memory/market_memory_registry.py (MarketMemory Core).

Covers DD-030 multi-asset, non-singleton behavior: register/get/
duplicate/unknown, get_or_create, default timeframe set (all six ON per
DD-026), and the build_default_registry factory.
"""

import pytest

from data_layer.market_memory.market_memory_registry import (
    MarketMemoryRegistry,
    DuplicateAssetError,
    UnknownAssetError,
    DEFAULT_TIMEFRAME_CAPACITY,
    build_default_registry,
)
from data_layer.market_memory.candle_record import MemoryMode


def test_default_timeframes_are_all_six_on():
    # DD-026: M1..D1 all present by default.
    assert set(DEFAULT_TIMEFRAME_CAPACITY) == {"M1", "M5", "M15", "H1", "H4", "D1"}


def test_register_and_get():
    reg = MarketMemoryRegistry()
    mem = reg.register("XAUUSD")
    assert reg.get("XAUUSD") is mem
    assert reg.has("XAUUSD")
    assert set(mem.timeframes()) == set(DEFAULT_TIMEFRAME_CAPACITY)


def test_register_duplicate_raises():
    reg = MarketMemoryRegistry()
    reg.register("XAUUSD")
    with pytest.raises(DuplicateAssetError):
        reg.register("XAUUSD")


def test_get_unknown_raises():
    reg = MarketMemoryRegistry()
    with pytest.raises(UnknownAssetError):
        reg.get("BTCUSD")


def test_get_or_create_is_idempotent():
    reg = MarketMemoryRegistry()
    a = reg.get_or_create("BTCUSD")
    b = reg.get_or_create("BTCUSD")
    assert a is b


def test_multiple_assets_are_independent():
    reg = MarketMemoryRegistry()
    reg.register("XAUUSD")
    reg.register("BTCUSD")
    assert set(reg.assets()) == {"XAUUSD", "BTCUSD"}
    assert reg.get("XAUUSD") is not reg.get("BTCUSD")


def test_remove():
    reg = MarketMemoryRegistry()
    reg.register("XAUUSD")
    reg.remove("XAUUSD")
    assert not reg.has("XAUUSD")
    with pytest.raises(UnknownAssetError):
        reg.remove("XAUUSD")


def test_custom_capacities_and_mode():
    reg = MarketMemoryRegistry()
    mem = reg.register("XAUUSD", {"M1": 5}, mode=MemoryMode.REPLAY)
    assert mem.timeframes() == ["M1"]
    assert mem.mode is MemoryMode.REPLAY


def test_build_default_registry_factory():
    reg = build_default_registry(["XAUUSD", "BTCUSD"])
    assert set(reg.assets()) == {"XAUUSD", "BTCUSD"}
    # not a singleton: a second registry is independent
    other = build_default_registry([])
    assert other.assets() == []
