"""
Unit tests for data_layer/market_memory/persistence/persistent_store.py (DD-069 backends,
DD-071 safe restore, recover).
"""

from data_layer.market_memory.market_memory import MarketMemory
from data_layer.market_memory.candle_record import CandleSource
from data_layer.market_memory.persistence.persistent_store import (
    InMemoryStorageBackend, FileStorageBackend, PersistentMemoryStore,
)
from _pfakes import memory_with, candle, ts


def test_persist_restore_roundtrip_inmemory():
    backend = InMemoryStorageBackend()
    store = PersistentMemoryStore(backend)
    store.persist("XAUUSD", memory_with(m1=6), ts(10))
    # fresh empty memory -> restore
    target = MarketMemory("XAUUSD", {"M1": 100})
    result = store.restore("XAUUSD", target)
    assert result.ok
    assert result.restored_candles == 6
    assert target.timeframe("M1").closed_count() == 6


def test_file_backend_roundtrip(tmp_path):
    backend = FileStorageBackend(str(tmp_path))
    store = PersistentMemoryStore(backend)
    store.persist("XAUUSD", memory_with(m1=4), ts(10))
    target = MarketMemory("XAUUSD", {"M1": 100})
    assert store.restore("XAUUSD", target).ok
    assert target.timeframe("M1").closed_count() == 4


def test_safe_restore_aborts_on_integrity_failure():
    # Persist a memory with a GAP (missing candle) -> restore must abort.
    backend = InMemoryStorageBackend()
    store = PersistentMemoryStore(backend)
    gappy = MarketMemory("XAUUSD", {"M1": 100})
    gappy.timeframe("M1").hydrate([candle(0), candle(1), candle(4)],  # 2,3 missing
                                  source=CandleSource.BOOTSTRAP)
    store.persist("XAUUSD", gappy, ts(10))

    target = MarketMemory("XAUUSD", {"M1": 100})
    result = store.restore("XAUUSD", target)
    assert result.ok is False
    assert "integrity failed" in result.reason
    assert target.timeframe("M1").closed_count() == 0   # memory untouched (DD-071)
    assert store.metrics.restore_failures == 1


def test_restore_no_snapshot():
    store = PersistentMemoryStore(InMemoryStorageBackend())
    target = MarketMemory("XAUUSD", {"M1": 100})
    r = store.restore("XAUUSD", target)
    assert not r.ok and r.reason == "no snapshot"


def test_recover_falls_back_through_slots():
    backend = InMemoryStorageBackend()
    store = PersistentMemoryStore(backend)
    store.persist("XAUUSD", memory_with(m1=5), ts(10))   # seeds latest+recovery
    target = MarketMemory("XAUUSD", {"M1": 100})
    result = store.recover("XAUUSD", target)
    assert result.ok
    assert "recovered from" in result.reason
