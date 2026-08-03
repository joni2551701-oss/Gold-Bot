"""Tests for SnapshotCleanup (module 9)."""

from data_layer.snapshots.catalog import SnapshotCatalog
from data_layer.snapshots.lifecycle import SnapshotLifecycle
from data_layer.snapshots.policy import SnapshotPolicy
from data_layer.snapshots.cleanup import SnapshotCleanup
from data_layer.snapshots.snapshot_state import SnapshotState

from _sfakes import ts, memory_with, new_backend


def _fixture(policy):
    backend = new_backend()
    catalog = SnapshotCatalog(backend)
    lifecycle = SnapshotLifecycle(backend, catalog)
    cleanup = SnapshotCleanup(catalog, lifecycle, policy)
    return catalog, lifecycle, cleanup


def test_cleanup_archives_by_default():
    policy = SnapshotPolicy(max_per_asset=1, archive_instead_of_delete=True)
    catalog, lc, cleanup = _fixture(policy)
    a = lc.create("XAUUSD", memory_with(), now=ts(1))
    b = lc.create("XAUUSD", memory_with(m1=6), now=ts(2))
    affected = cleanup.run(ts(10))
    assert a.snapshot_id in affected
    assert catalog.get(a.snapshot_id).state is SnapshotState.ARCHIVED
    # newest kept, unaffected
    assert b.snapshot_id not in affected


def test_cleanup_deletes_when_configured():
    policy = SnapshotPolicy(max_per_asset=1, archive_instead_of_delete=False)
    catalog, lc, cleanup = _fixture(policy)
    a = lc.create("XAUUSD", memory_with(), now=ts(1))
    lc.create("XAUUSD", memory_with(m1=6), now=ts(2))
    affected = cleanup.run(ts(10))
    assert a.snapshot_id in affected
    assert catalog.get(a.snapshot_id) is None


def test_cleanup_skips_locked():
    policy = SnapshotPolicy(max_per_asset=0, archive_instead_of_delete=False)
    catalog, lc, cleanup = _fixture(policy)
    a = lc.create("XAUUSD", memory_with(), now=ts(1))
    lc.lock(a.snapshot_id)
    affected = cleanup.run(ts(10))
    # locked entry is protected by the policy -> never selected
    assert a.snapshot_id not in affected
    assert catalog.get(a.snapshot_id) is not None
