"""Tests for SnapshotIO export/import (module 9, amendments 1, 4, 5)."""

import copy

import pytest

from data_layer.snapshots.catalog import SnapshotCatalog
from data_layer.snapshots.lifecycle import SnapshotLifecycle, SnapshotNotFoundError
from data_layer.snapshots.snapshot_io import (
    SnapshotIO, SnapshotIncompatibleError, SnapshotImportError,
    ENVELOPE_FORMAT_VERSION,
)
from data_layer.snapshots.snapshot_state import SnapshotState, VerifyState

from _sfakes import ts, memory_with, new_backend


def _io(backend=None):
    backend = backend or new_backend()
    catalog = SnapshotCatalog(backend)
    lifecycle = SnapshotLifecycle(backend, catalog)
    return SnapshotIO(lifecycle, catalog), lifecycle, catalog


def _valid_envelope():
    io, lc, _ = _io()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.verify(entry.snapshot_id)          # VERIFIED so EXPORTED marker is legal
    return io.export(entry.snapshot_id), entry


def test_export_envelope_shape():
    envelope, entry = _valid_envelope()
    assert envelope["format_version"] == ENVELOPE_FORMAT_VERSION
    assert envelope["manifest"]["snapshot_id"] == entry.snapshot_id
    assert isinstance(envelope["blob_b64"], str)


def test_export_marks_exported_when_legal():
    io, lc, catalog = _io()
    entry = lc.create("XAUUSD", memory_with(), now=ts(0))
    lc.verify(entry.snapshot_id)
    io.export(entry.snapshot_id)
    assert catalog.get(entry.snapshot_id).state is SnapshotState.EXPORTED


def test_export_missing_raises():
    io, _, _ = _io()
    with pytest.raises(SnapshotNotFoundError):
        io.export("nope")


def test_import_roundtrip_into_fresh_backend():
    envelope, entry = _valid_envelope()
    io2, _, catalog2 = _io()          # fresh, empty backend
    imported = io2.import_(envelope, now=ts(5))
    assert imported.snapshot_id == entry.snapshot_id
    assert imported.state is SnapshotState.IMPORTED
    assert imported.verify_state is VerifyState.VERIFIED
    assert catalog2.get(entry.snapshot_id) is not None


def test_import_rejects_bad_schema_version():
    envelope, _ = _valid_envelope()
    bad = copy.deepcopy(envelope)
    bad["manifest"]["schema_version"] = 999
    io2, _, _ = _io()
    with pytest.raises(SnapshotIncompatibleError):
        io2.import_(bad)


def test_import_rejects_incompatible_core_version():
    envelope, _ = _valid_envelope()
    bad = copy.deepcopy(envelope)
    bad["manifest"]["core_version"] = "2.0.0"
    io2, _, _ = _io()
    with pytest.raises(SnapshotIncompatibleError):
        io2.import_(bad)


def test_import_rejects_missing_asset():
    envelope, _ = _valid_envelope()
    bad = copy.deepcopy(envelope)
    bad["manifest"]["asset"] = ""
    io2, _, _ = _io()
    with pytest.raises(SnapshotIncompatibleError):
        io2.import_(bad)


def test_import_malformed_envelope_raises():
    io2, _, _ = _io()
    with pytest.raises(SnapshotImportError):
        io2.import_({"manifest": {"nope": 1}})


def test_import_rolls_back_blob_on_register_failure():
    envelope, entry = _valid_envelope()
    io2, lifecycle2, catalog2 = _io()

    def boom(e):
        raise RuntimeError("register failed")

    catalog2.register = boom
    with pytest.raises(RuntimeError):
        io2.import_(envelope)
    assert lifecycle2.load_blob(entry.snapshot_id) is None
