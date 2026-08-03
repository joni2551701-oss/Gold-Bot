"""Unit tests for data_layer/live_data/price_cache.py (TASK-DATA-001)."""

from datetime import datetime, timezone

from data_layer.live_data.price_cache import PriceCache
from data_layer.live_data.price_tick import PriceTick


def _tick(symbol="XAUUSD", price=2400.0, provider="twelvedata"):
    return PriceTick(symbol=symbol, price=price,
                      timestamp=datetime(2026, 7, 24, 13, tzinfo=timezone.utc),
                      provider=provider)


def test_get_missing_symbol_returns_none():
    cache = PriceCache()
    assert cache.get("XAUUSD") is None


def test_update_then_get_returns_latest():
    cache = PriceCache()
    cache.update(_tick(price=2400.0))
    cache.update(_tick(price=2401.5))
    tick = cache.get("XAUUSD")
    assert tick.price == 2401.5


def test_per_symbol_isolation():
    cache = PriceCache()
    cache.update(_tick(symbol="XAUUSD", price=2400.0))
    cache.update(_tick(symbol="BTCUSDT", price=65000.0, provider="bitget"))
    assert cache.get("XAUUSD").price == 2400.0
    assert cache.get("BTCUSDT").price == 65000.0
    assert set(cache.symbols()) == {"XAUUSD", "BTCUSDT"}
