"""data_layer/snapshots/snapshot_io -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `snapshot_io.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `snapshot_io.py`.
"""
from data_layer.snapshots.snapshot_io.snapshot_io import (
    annotations,
    base64,
    datetime,
    Optional,
    Tuple,
    CandleClock,
    MemoryCodec,
    SCHEMA_VERSION,
    check_series,
    SnapshotCatalog,
    CatalogEntry,
    SnapshotManifest,
    utcnow,
    SnapshotState,
    VerifyState,
    CORE_VERSION,
    can_transition,
    SnapshotLifecycle,
    SnapshotNotFoundError,
    ENVELOPE_FORMAT_VERSION,
    SnapshotIncompatibleError,
    SnapshotImportError,
    SnapshotIO,
)

__all__ = [
    "annotations",
    "base64",
    "datetime",
    "Optional",
    "Tuple",
    "CandleClock",
    "MemoryCodec",
    "SCHEMA_VERSION",
    "check_series",
    "SnapshotCatalog",
    "CatalogEntry",
    "SnapshotManifest",
    "utcnow",
    "SnapshotState",
    "VerifyState",
    "CORE_VERSION",
    "can_transition",
    "SnapshotLifecycle",
    "SnapshotNotFoundError",
    "ENVELOPE_FORMAT_VERSION",
    "SnapshotIncompatibleError",
    "SnapshotImportError",
    "SnapshotIO",
]
