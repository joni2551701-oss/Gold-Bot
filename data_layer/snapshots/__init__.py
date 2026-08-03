"""
data_layer.snapshots -- GoldBot v1.1 Market Data Foundation: Snapshot
Infrastructure (Phase 1 module 9). The snapshot *management* layer:
a metadata-only catalog + manifest, a query registry, a transactional
lifecycle (create/verify/archive/delete) with locking and a state
machine, retention policy + cleanup, portable import/export with a
compatibility gate, metrics, and a SnapshotManager facade that emits
SNAPSHOT.* events.

Module 6 creates & stores snapshots; module 9 manages them -- this layer
reuses module-6 serialization (MemoryCodec), storage (StorageBackend) and
integrity (check_series) rather than re-implementing them. Foundation
only: not wired into core/pipeline.py (Trading Safety). Never imports from
telegram/, ai/, decision/, risk/, strategies/, signals/, context/, or
database/.
"""

from data_layer.snapshots.snapshot_state import (
    SnapshotState, VerifyState, SnapshotStateError,
    can_transition, assert_transition, CORE_VERSION,
)
from data_layer.snapshots.catalog import (
    SnapshotManifest, CatalogEntry, SnapshotCatalog, utcnow,
)
from data_layer.snapshots.registry import SnapshotRegistry
from data_layer.snapshots.policy import SnapshotPolicy
from data_layer.snapshots.metrics import SnapshotMetrics
from data_layer.snapshots.lifecycle import (
    SnapshotLifecycle, SnapshotLockedError, SnapshotNotFoundError,
)
from data_layer.snapshots.cleanup import SnapshotCleanup
from data_layer.snapshots.snapshot_io import (
    SnapshotIO, SnapshotIncompatibleError, SnapshotImportError,
    ENVELOPE_FORMAT_VERSION,
)
from data_layer.snapshots.manager import SnapshotManager

__all__ = [
    "SnapshotState", "VerifyState", "SnapshotStateError",
    "can_transition", "assert_transition", "CORE_VERSION",
    "SnapshotManifest", "CatalogEntry", "SnapshotCatalog", "utcnow",
    "SnapshotRegistry",
    "SnapshotPolicy",
    "SnapshotMetrics",
    "SnapshotLifecycle", "SnapshotLockedError", "SnapshotNotFoundError",
    "SnapshotCleanup",
    "SnapshotIO", "SnapshotIncompatibleError", "SnapshotImportError",
    "ENVELOPE_FORMAT_VERSION",
    "SnapshotManager",
]
