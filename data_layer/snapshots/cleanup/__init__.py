"""data_layer/snapshots/cleanup -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `cleanup.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `cleanup.py`.
"""
from data_layer.snapshots.cleanup.cleanup import (
    annotations,
    datetime,
    List,
    SnapshotCatalog,
    SnapshotPolicy,
    SnapshotLifecycle,
    SnapshotLockedError,
    SnapshotCleanup,
)

__all__ = [
    "annotations",
    "datetime",
    "List",
    "SnapshotCatalog",
    "SnapshotPolicy",
    "SnapshotLifecycle",
    "SnapshotLockedError",
    "SnapshotCleanup",
]
