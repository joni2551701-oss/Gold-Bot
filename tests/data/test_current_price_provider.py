"""
Tests for data/current_price_provider.py (TASK-CORE-004 Phase 1).

Covers the read-only, no-fetch reading of the production SmartDataCache
and the CurrentPriceProvider abstraction (fail-safe, symbol normalized,
swappable backend).
"""

from datetime import datetime, timedelta, timezone

from data.twelve_data_client import Candle
from data.current_price_provider import (
    CurrentPrice,
    CurrentPriceProvider,
    SmartCacheLastPriceSource,
)

BASE = datetime(2026, 1, 1, 14, 52, 8, tzinfo=timezone.utc)


def _candle(close, ts):
    return Candle(timestamp=ts, open=close, high=close + 1, low=close - 1, close=close)


class _FakeCache:
    """Mimics SmartDataCache: a `.cache` dict; get_cached_snapshot raises
    if called (so tests prove the read path never fetches)."""
    def __init__(self, cache):
        self.cache = cache
    def get_cached_snapshot(self, *a, **k):
        raise AssertionError("get_cached_snapshot must NOT be called (no fetch on read)")


# ---------------- SmartCacheLastPriceSource ----------------

def test_reads_freshest_candle_across_intervals_no_fetch():
    cache = _FakeCache({
        "XAUUSD": {
            "M15": {"data": [_candle(3360.0, BASE), _candle(3368.42, BASE + timedelta(minutes=15))]},
            "H1":  {"data": [_candle(3350.0, BASE - timedelta(hours=1))]},
        }
    })
    src = SmartCacheLastPriceSource(cache=cache)
    cp = src.get_current_price("XAUUSD")
    assert isinstance(cp, CurrentPrice)
    assert cp.asset == "XAUUSD"
    assert cp.price == 3368.42  # freshest timestamp wins
    assert cp.timestamp == BASE + timedelta(minutes=15)


def test_empty_cache_returns_none():
    assert SmartCacheLastPriceSource(cache=_FakeCache({})).get_current_price("XAUUSD") is None


def test_symbol_absent_returns_none():
    cache = _FakeCache({"XAUUSD": {"M15": {"data": [_candle(1.0, BASE)]}}})
    assert SmartCacheLastPriceSource(cache=cache).get_current_price("BTCUSDT") is None


def test_interval_with_no_data_is_skipped():
    cache = _FakeCache({"XAUUSD": {"M15": {"data": []}, "H1": {"data": [_candle(9.0, BASE)]}}})
    cp = SmartCacheLastPriceSource(cache=cache).get_current_price("XAUUSD")
    assert cp is not None and cp.price == 9.0


def test_source_never_raises_on_broken_cache():
    class _Broken:
        @property
        def cache(self):
            raise RuntimeError("boom")
    assert SmartCacheLastPriceSource(cache=_Broken()).get_current_price("XAUUSD") is None


# ---------------- CurrentPriceProvider ----------------

class _FakeSource:
    def __init__(self, result):
        self._r = result
        self.calls = []
    def get_current_price(self, symbol):
        self.calls.append(symbol)
        return self._r


def test_provider_delegates_and_normalizes_symbol():
    cp = CurrentPrice(asset="XAUUSD", price=3368.42, timestamp=BASE)
    src = _FakeSource(cp)
    provider = CurrentPriceProvider(source=src)
    assert provider.get_current_price(" xauusd ") is cp
    assert src.calls == ["XAUUSD"]  # trimmed + upper-cased


def test_provider_failsafe_on_raising_source():
    class _Boom:
        def get_current_price(self, symbol):
            raise RuntimeError("kaboom")
    assert CurrentPriceProvider(source=_Boom()).get_current_price("XAUUSD") is None


def test_provider_returns_none_when_source_has_no_price():
    assert CurrentPriceProvider(source=_FakeSource(None)).get_current_price("XAUUSD") is None
