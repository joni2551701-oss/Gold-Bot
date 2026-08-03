"""Tests for SnapshotRegistry query views (module 9)."""

from data_layer.snapshots.catalog import SnapshotCatalog, CatalogEntry
from data_layer.snapshots.registry import SnapshotRegistry

from _sfakes import ts


def _entry(sid, asset="XAUUSD", i=0, label="snapshot", tags=()):
    return CatalogEntry(
        snapshot_id=sid, asset=asset, label=label, created_at=ts(i),
        size_bytes=1, metadata_hash="h", schema_version=1, tags=tags)


def _registry(*entries):
    cat = SnapshotCatalog()
    for e in entries:
        cat.register(e)
    return SnapshotRegistry(cat)


def test_get_and_list_sorted_by_created():
    reg = _registry(_entry("b", i=2), _entry("a", i=1))
    assert reg.get("a").snapshot_id == "a"
    assert [e.snapshot_id for e in reg.list()] == ["a", "b"]


def test_list_by_asset():
    reg = _registry(_entry("a", "XAUUSD"), _entry("b", "EURUSD"))
    assert [e.snapshot_id for e in reg.list("EURUSD")] == ["b"]


def test_latest():
    reg = _registry(_entry("old", i=1), _entry("new", i=5))
    assert reg.latest("XAUUSD").snapshot_id == "new"
    assert reg.latest("MISSING") is None


def test_find_filters():
    reg = _registry(
        _entry("a", i=1, label="auto", tags=("x",)),
        _entry("b", i=2, label="manual", tags=("y",)),
        _entry("c", i=3, label="auto", tags=("x",)))
    assert {e.snapshot_id for e in reg.find(label="auto")} == {"a", "c"}
    assert {e.snapshot_id for e in reg.find(tag="y")} == {"b"}
    assert {e.snapshot_id for e in reg.find(since=ts(2))} == {"b", "c"}
    assert {e.snapshot_id for e in reg.find(until=ts(2))} == {"a", "b"}
