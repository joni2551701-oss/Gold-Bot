"""Tests for SnapshotMetrics (module 9)."""

from data.snapshots.catalog import CatalogEntry
from data.snapshots.metrics import SnapshotMetrics
from data.snapshots.snapshot_state import SnapshotState, VerifyState

from _sfakes import ts


def _entry(sid, asset="XAUUSD", i=0, size=10, state=SnapshotState.CREATED,
           verify=VerifyState.UNVERIFIED, locks=0):
    return CatalogEntry(
        snapshot_id=sid, asset=asset, label="s", created_at=ts(i),
        size_bytes=size, metadata_hash="h", schema_version=1,
        state=state, verify_state=verify, locks=locks)


def test_empty_metrics():
    m = SnapshotMetrics.snapshot([])
    assert m["count"] == 0
    assert m["total_size_bytes"] == 0
    assert m["last_created"] is None


def test_aggregate_metrics():
    entries = [
        _entry("a", "XAUUSD", i=1, size=10, verify=VerifyState.VERIFIED),
        _entry("b", "XAUUSD", i=2, size=20, verify=VerifyState.FAILED),
        _entry("c", "EURUSD", i=3, size=30, state=SnapshotState.ARCHIVED,
               locks=1),
    ]
    m = SnapshotMetrics.snapshot(entries)
    assert m["count"] == 3
    assert m["total_size_bytes"] == 60
    assert m["per_asset"] == {"XAUUSD": 2, "EURUSD": 1}
    assert m["verified"] == 1
    assert m["verify_failed"] == 1
    assert m["archived"] == 1
    assert m["in_use"] == 1
    assert m["last_created"] == ts(3).isoformat()
