"""Tests for SnapshotLifecycle (module 9, amendments 2, 3, 5)."""

import pytest

from data_layer.snapshots.lifecycle import (
    SnapshotLifecycle, SnapshotLockedError, SnapshotNotFoundError,
)
from data_layer.snapshots.catalog import SnapshotCatalog
from data_layer.snapshots.snapshot_state import SnapshotState, VerifyState

from _sfakes import ts, memory_with, new_backend


def _lifecycle():
    backend = new_backend()
    return SnapshotLifecycle(backend, SnapshotCatalog(backend)), backend


def test_create_registers_and_stores():
    lc, backend = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    assert entry.state is SnapshotState.CREATED
    assert entry.verify_state is VerifyState.UNVERIFIED
    assert lc.load_blob(entry.snapshot_id) is not None
    assert entry.size_bytes > 0


def test_verify_ok_transitions_to_verified():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    vs = lc.verify(entry.snapshot_id)
    assert vs is VerifyState.VERIFIED
    assert lc._catalog.get(entry.snapshot_id).state is SnapshotState.VERIFIED


def test_verify_corrupt_blob_marks_corrupted():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.store_blob(entry.snapshot_id, b"not a real snapshot")
    vs = lc.verify(entry.snapshot_id)
    assert vs is VerifyState.FAILED
    assert lc._catalog.get(entry.snapshot_id).state is SnapshotState.CORRUPTED


def test_archive_requires_verified_or_created():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.archive(entry.snapshot_id)
    assert lc._catalog.get(entry.snapshot_id).state is SnapshotState.ARCHIVED


def test_delete_removes_blob_and_entry():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.delete(entry.snapshot_id)
    assert lc._catalog.get(entry.snapshot_id) is None
    assert lc.load_blob(entry.snapshot_id) is None


def test_lock_blocks_archive_and_delete():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.lock(entry.snapshot_id)
    with pytest.raises(SnapshotLockedError):
        lc.archive(entry.snapshot_id)
    with pytest.raises(SnapshotLockedError):
        lc.delete(entry.snapshot_id)
    lc.unlock(entry.snapshot_id)
    lc.archive(entry.snapshot_id)          # now allowed
    assert lc._catalog.get(entry.snapshot_id).state is SnapshotState.ARCHIVED


def test_unlock_never_negative():
    lc, _ = _lifecycle()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.unlock(entry.snapshot_id)
    assert lc._catalog.get(entry.snapshot_id).locks == 0


def test_operations_on_missing_raise():
    lc, _ = _lifecycle()
    with pytest.raises(SnapshotNotFoundError):
        lc.verify("nope")
    with pytest.raises(SnapshotNotFoundError):
        lc.archive("nope")


def test_create_rollback_on_register_failure():
    lc, backend = _lifecycle()

    def boom(entry):
        raise RuntimeError("register failed")

    lc._catalog.register = boom          # force REGISTER to fail
    with pytest.raises(RuntimeError):
        lc.create("XAUUSD", memory_with(), now=ts(0))
    # blob must have been rolled back -- storage holds no orphan blob
    assert [k for k in backend.list_keys("blob/")] == []
