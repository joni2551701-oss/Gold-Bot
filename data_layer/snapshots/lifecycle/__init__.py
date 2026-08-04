"""data_layer/snapshots/lifecycle -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `lifecycle.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `lifecycle.py`.
"""
from data_layer.snapshots.lifecycle.lifecycle import (
    annotations,
    hashlib,
    datetime,
    Optional,
    setup_logger,
    MemoryCodec,
    StorageBackend,
    check_series,
    CandleClock,
    MarketMemory,
    SnapshotCatalog,
    CatalogEntry,
    utcnow,
    SnapshotState,
    VerifyState,
    assert_transition,
    can_transition,
    CORE_VERSION,
    logger,
    SnapshotLockedError,
    SnapshotNotFoundError,
    SnapshotLifecycle,
)

__all__ = [
    "annotations",
    "hashlib",
    "datetime",
    "Optional",
    "setup_logger",
    "MemoryCodec",
    "StorageBackend",
    "check_series",
    "CandleClock",
    "MarketMemory",
    "SnapshotCatalog",
    "CatalogEntry",
    "utcnow",
    "SnapshotState",
    "VerifyState",
    "assert_transition",
    "can_transition",
    "CORE_VERSION",
    "logger",
    "SnapshotLockedError",
    "SnapshotNotFoundError",
    "SnapshotLifecycle",
]
