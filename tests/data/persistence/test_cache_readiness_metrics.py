"""
Unit tests for cache_policy.py, readiness.py, smart_cache_adapter.py,
persistence_metrics.py (module 6).
"""

from datetime import timedelta

from data_layer.market_memory.persistence.cache_policy import CachePolicy
from data_layer.market_memory.persistence.readiness import ReadinessService, Readiness
from data_layer.market_memory.persistence.smart_cache_adapter import SmartCacheAdapter
from data_layer.market_memory.persistence.persistence_metrics import PersistenceMetrics
from data_layer.historical_data.bootstrap_state import BootstrapState
from _pfakes import candle, ts


# -- CachePolicy --------------------------------------------------------
def test_cache_policy_freshness_by_candle_close():
    p = CachePolicy()
    written = ts(0)
    # M1 written at 13:00 stays fresh until the 13:01 candle closes (13:02)
    assert p.is_fresh("M1", written, ts(0)) is True
    assert p.is_fresh("M1", written, ts(5)) is False


def test_cache_policy_ttl():
    p = CachePolicy(ttl_seconds=30)
    written = ts(0)
    assert p.is_fresh("M1", written, written + timedelta(seconds=10)) is True
    assert p.is_fresh("M1", written, written + timedelta(seconds=60)) is False


def test_cache_policy_lru_eviction():
    p = CachePolicy(max_entries=2)
    access = {"a": ts(1), "b": ts(2), "c": ts(3)}
    assert p.evictions(access) == ["a"]        # oldest evicted


# -- SmartCacheAdapter --------------------------------------------------
def test_smart_cache_adapter_put_get_lasttime():
    a = SmartCacheAdapter()
    a.put("XAUUSD", "M1", [candle(0), candle(1)], ts(0))
    got = a.get("XAUUSD", "M1")
    assert [c.close for c in got] == [100.0, 100.0]
    assert a.last_time("XAUUSD", "M1") == ts(1)
    assert a.is_fresh("XAUUSD", "M1", ts(0)) is True
    assert a.is_fresh("XAUUSD", "M1", ts(10)) is False
    assert a.get("XAUUSD", "H4") is None


# -- ReadinessService (DD-065) ------------------------------------------
class _Progress:
    def __init__(self, status):
        self.status = status


class _FakeBootstrap:
    def __init__(self, ready, status):
        self.bootstrap_ready = ready
        self._status = status

    def progress(self):
        return _Progress(self._status)


def _svc(mapping):
    return ReadinessService(bootstrap_lookup=lambda a: mapping.get(a))


def test_readiness_states():
    svc = _svc({
        "R": _FakeBootstrap(True, BootstrapState.READY),
        "L": _FakeBootstrap(False, BootstrapState.LOADING),
        "F": _FakeBootstrap(False, BootstrapState.FAILED),
        "C": _FakeBootstrap(False, BootstrapState.CANCELLED),
    })
    assert svc.get_readiness("R") is Readiness.READY
    assert svc.get_readiness("L") is Readiness.BOOTSTRAPPING
    assert svc.get_readiness("F") is Readiness.FAILED
    assert svc.get_readiness("C") is Readiness.CANCELLED
    assert svc.get_readiness("unknown") is Readiness.BOOTSTRAPPING


def test_readiness_recovering_marker():
    svc = _svc({"X": _FakeBootstrap(True, BootstrapState.READY)})
    svc.mark_recovering("X")
    assert svc.get_readiness("X") is Readiness.RECOVERING
    svc.clear_recovering("X")
    assert svc.get_readiness("X") is Readiness.READY


# -- PersistenceMetrics -------------------------------------------------
def test_persistence_metrics():
    m = PersistenceMetrics()
    m.cache_hits = 3
    m.cache_misses = 1
    assert m.cache_hit_pct == 75.0
    assert m.as_dict()["cache_hit_pct"] == 75.0
