"""Tests for SnapshotPolicy selection (module 9)."""

from datetime import timedelta

from data_layer.snapshots.catalog import CatalogEntry
from data_layer.snapshots.policy import SnapshotPolicy

from _sfakes import ts


def _entry(sid, i=0, asset="XAUUSD", label="snapshot", locks=0):
    return CatalogEntry(
        snapshot_id=sid, asset=asset, label=label, created_at=ts(i),
        size_bytes=1, metadata_hash="h", schema_version=1, locks=locks)


def test_max_age_selects_old():
    policy = SnapshotPolicy(max_age=timedelta(minutes=10))
    entries = [_entry("old", i=0), _entry("new", i=100)]
    now = ts(100)
    removable = policy.select_removable(entries, now)
    assert [e.snapshot_id for e in removable] == ["old"]


def test_max_per_asset_keeps_newest():
    policy = SnapshotPolicy(max_per_asset=1)
    entries = [_entry("a", i=1), _entry("b", i=2), _entry("c", i=3)]
    removable = policy.select_removable(entries, ts(10))
    # keeps newest (c); a and b removable
    assert {e.snapshot_id for e in removable} == {"a", "b"}


def test_locked_never_selected():
    policy = SnapshotPolicy(max_per_asset=0)
    entries = [_entry("locked", i=1, locks=1), _entry("free", i=2)]
    removable = policy.select_removable(entries, ts(10))
    assert {e.snapshot_id for e in removable} == {"free"}


def test_protected_label_never_selected():
    policy = SnapshotPolicy(max_per_asset=0)
    entries = [_entry("keep", i=1, label="recovery"), _entry("drop", i=2)]
    removable = policy.select_removable(entries, ts(10))
    assert {e.snapshot_id for e in removable} == {"drop"}


def test_defaults_are_conservative():
    policy = SnapshotPolicy()
    entries = [_entry("a", i=1), _entry("b", i=2)]
    assert policy.select_removable(entries, ts(10)) == []
