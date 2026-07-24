"""Tests for the snapshot catalog + manifest (module 9, amendments 1, 3)."""

from data.snapshots.catalog import (
    SnapshotCatalog, CatalogEntry, SnapshotManifest,
)
from data.snapshots.snapshot_state import SnapshotState, VerifyState

from _sfakes import ts, new_backend


def _entry(sid="s1", asset="XAUUSD", label="snapshot"):
    return CatalogEntry(
        snapshot_id=sid, asset=asset, label=label, created_at=ts(0),
        size_bytes=10, metadata_hash="h", schema_version=1)


def test_register_get_all_by_asset():
    cat = SnapshotCatalog()
    cat.register(_entry("a", "XAUUSD"))
    cat.register(_entry("b", "EURUSD"))
    assert cat.get("a").asset == "XAUUSD"
    assert len(cat.all()) == 2
    assert [e.snapshot_id for e in cat.by_asset("EURUSD")] == ["b"]


def test_update_and_remove():
    cat = SnapshotCatalog()
    e = _entry("a")
    cat.register(e)
    e.state = SnapshotState.VERIFIED
    cat.update(e)
    assert cat.get("a").state is SnapshotState.VERIFIED
    cat.remove("a")
    assert cat.get("a") is None


def test_manifest_fields():
    e = _entry("a", "XAUUSD")
    m = e.manifest()
    assert isinstance(m, SnapshotManifest)
    assert m.snapshot_id == "a"
    assert m.asset == "XAUUSD"
    assert m.core_version == e.core_version


def test_manifest_roundtrip():
    m = _entry().manifest()
    assert SnapshotManifest.from_dict(m.as_dict()) == m


def test_catalog_entry_roundtrip():
    e = _entry("a")
    e.locks = 2
    e.verify_state = VerifyState.VERIFIED
    e.tags = ("x", "y")
    back = CatalogEntry.from_dict(e.as_dict())
    assert back == e
    assert back.in_use is True


def test_in_use_property():
    e = _entry()
    assert e.in_use is False
    e.locks = 1
    assert e.in_use is True


def test_catalog_persists_across_instances():
    backend = new_backend()
    cat = SnapshotCatalog(backend)
    cat.register(_entry("a"))
    reloaded = SnapshotCatalog(backend)
    assert reloaded.get("a") is not None
    assert reloaded.get("a").snapshot_id == "a"
