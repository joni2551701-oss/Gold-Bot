"""Unit tests for data/persistence/snapshot_store.py (DD-067/068/070)."""

from data.persistence.persistent_store import InMemoryStorageBackend
from data.persistence.snapshot_store import SnapshotStore
from _pfakes import memory_with, ts


def test_save_and_load_latest():
    store = SnapshotStore(InMemoryStorageBackend())
    meta = store.save("XAUUSD", memory_with(m1=5), ts(10))
    assert meta.candle_count == 5
    decoded = store.load_decoded("XAUUSD", "latest")
    assert decoded is not None
    _, tfs = decoded
    assert len(tfs["M1"]) == 5


def test_retention_latest_previous_recovery():
    backend = InMemoryStorageBackend()
    store = SnapshotStore(backend)
    store.save("XAUUSD", memory_with(m1=3), ts(1))    # latest + recovery seeded
    store.save("XAUUSD", memory_with(m1=5), ts(2))    # previous <- old latest
    slots = store.available_slots("XAUUSD")
    assert set(slots) == {"latest", "previous", "recovery"}
    # latest has 5, previous has 3
    _, latest = store.load_decoded("XAUUSD", "latest")
    _, previous = store.load_decoded("XAUUSD", "previous")
    assert len(latest["M1"]) == 5
    assert len(previous["M1"]) == 3


def test_atomic_write_leaves_no_temp_key():
    backend = InMemoryStorageBackend()
    store = SnapshotStore(backend)
    store.save("XAUUSD", memory_with(m1=4), ts(1))
    assert not backend.exists("XAUUSD/tmp")     # committed, temp cleaned up


def test_promote_recovery():
    backend = InMemoryStorageBackend()
    store = SnapshotStore(backend)
    store.save("XAUUSD", memory_with(m1=3), ts(1))
    store.save("XAUUSD", memory_with(m1=7), ts(2))
    assert store.promote_recovery("XAUUSD") is True
    _, recovery = store.load_decoded("XAUUSD", "recovery")
    assert len(recovery["M1"]) == 7             # recovery now = current latest
