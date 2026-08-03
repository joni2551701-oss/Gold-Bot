"""Tests for the SnapshotManager facade (module 9, amendment 6)."""

import pytest

from data_layer.event_system.event_bus import EventBus
from data_layer.event_system.event_model import EventType
from data_layer.snapshots.manager import SnapshotManager
from data_layer.snapshots.policy import SnapshotPolicy
from data_layer.snapshots.lifecycle import SnapshotLockedError
from data_layer.snapshots.snapshot_state import SnapshotState, VerifyState

from _sfakes import ts, memory_with, new_backend


def _manager_with_bus(policy=None):
    bus = EventBus()
    events = []
    bus.subscribe("SNAPSHOT", events.append)
    mgr = SnapshotManager(new_backend(), bus=bus, policy=policy)
    return mgr, events


def _types(events):
    return [e.type for e in events]


def test_create_emits_created_event():
    mgr, events = _manager_with_bus()
    entry = mgr.create("XAUUSD", memory_with(), now=ts(0))
    assert EventType.SNAPSHOT_CREATED in _types(events)
    assert mgr.get(entry.snapshot_id) is not None


def test_verify_emits_verified():
    mgr, events = _manager_with_bus()
    entry = mgr.create("XAUUSD", memory_with(), now=ts(0))
    vs = mgr.verify(entry.snapshot_id, now=ts(1))
    assert vs is VerifyState.VERIFIED
    assert EventType.SNAPSHOT_VERIFIED in _types(events)


def test_archive_and_delete_emit_events():
    mgr, events = _manager_with_bus()
    a = mgr.create("XAUUSD", memory_with(), now=ts(0))
    mgr.archive(a.snapshot_id, now=ts(1))
    assert mgr.get(a.snapshot_id).state is SnapshotState.ARCHIVED
    mgr.delete(a.snapshot_id, now=ts(2))
    assert mgr.get(a.snapshot_id) is None
    assert EventType.SNAPSHOT_ARCHIVED in _types(events)
    assert EventType.SNAPSHOT_DELETED in _types(events)


def test_lock_blocks_delete_via_manager():
    mgr, _ = _manager_with_bus()
    a = mgr.create("XAUUSD", memory_with(), now=ts(0))
    mgr.lock(a.snapshot_id)
    with pytest.raises(SnapshotLockedError):
        mgr.delete(a.snapshot_id)
    mgr.unlock(a.snapshot_id)
    mgr.delete(a.snapshot_id)
    assert mgr.get(a.snapshot_id) is None


def test_export_import_roundtrip_emits_events():
    mgr, events = _manager_with_bus()
    a = mgr.create("XAUUSD", memory_with(), now=ts(0))
    mgr.verify(a.snapshot_id, now=ts(1))
    envelope = mgr.export(a.snapshot_id, now=ts(2))
    assert EventType.SNAPSHOT_EXPORTED in _types(events)

    mgr2, events2 = _manager_with_bus()
    imported = mgr2.import_(envelope, now=ts(3))
    assert imported.state is SnapshotState.IMPORTED
    assert EventType.SNAPSHOT_IMPORTED in _types(events2)


def test_cleanup_emits_cleanup_event():
    policy = SnapshotPolicy(max_per_asset=1)
    mgr, events = _manager_with_bus(policy=policy)
    mgr.create("XAUUSD", memory_with(), now=ts(1))
    mgr.create("XAUUSD", memory_with(m1=6), now=ts(2))
    affected = mgr.cleanup(now=ts(10))
    assert affected
    assert EventType.SNAPSHOT_CLEANUP in _types(events)


def test_metrics_reports_counts():
    mgr, _ = _manager_with_bus()
    mgr.create("XAUUSD", memory_with(), now=ts(0))
    mgr.create("EURUSD", memory_with(asset="EURUSD"), now=ts(1))
    m = mgr.metrics()
    assert m["count"] == 2
    assert m["per_asset"] == {"XAUUSD": 1, "EURUSD": 1}


def test_manager_works_without_bus():
    mgr = SnapshotManager(new_backend())        # no bus
    entry = mgr.create("XAUUSD", memory_with(), now=ts(0))
    assert mgr.verify(entry.snapshot_id) is VerifyState.VERIFIED
    assert mgr.latest("XAUUSD").snapshot_id == entry.snapshot_id
