# data_layer / snapshots

**Module**

## Purpose

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

## Files

- `__init__.py` -- data_layer.snapshots -- GoldBot v1.1 Market Data Foundation: Snapshot
- `catalog.py` -- Snapshot catalog + manifest (v1.1 Phase 1, module 9).
- `cleanup.py` -- SnapshotCleanup -- applies a SnapshotPolicy to remove/rotate snapshots
- `lifecycle.py` -- SnapshotLifecycle -- create / verify / archive / delete (v1.1 Phase 1,
- `manager.py` -- SnapshotManager -- the facade that composes the module-9 snapshot
- `metrics.py` -- SnapshotMetrics -- infrastructure metrics (module 9).
- `policy.py` -- SnapshotPolicy -- retention / rotation / expiration rules (v1.1 Phase 1,
- `registry.py` -- SnapshotRegistry -- the query API over the catalog (v1.1 Phase 1,
- `snapshot_io.py` -- SnapshotIO -- portable export / import of a snapshot (v1.1 Phase 1,
- `snapshot_state.py` -- Snapshot state machine (v1.1 Phase 1, module 9; amendment 3).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `catalog.py`: class `SnapshotManifest`
- `catalog.py`: class `CatalogEntry`
- `catalog.py`: class `SnapshotCatalog`
- `catalog.py`: function `utcnow()`
- `cleanup.py`: class `SnapshotCleanup`
- `lifecycle.py`: class `SnapshotLockedError`
- `lifecycle.py`: class `SnapshotNotFoundError`
- `lifecycle.py`: class `SnapshotLifecycle`
- `manager.py`: class `SnapshotManager`
- `metrics.py`: class `SnapshotMetrics`
- `policy.py`: class `SnapshotPolicy`
- `registry.py`: class `SnapshotRegistry`
- `snapshot_io.py`: class `SnapshotIncompatibleError`
- `snapshot_io.py`: class `SnapshotImportError`
- `snapshot_io.py`: class `SnapshotIO`
- `snapshot_state.py`: class `VerifyState`
- `snapshot_state.py`: class `SnapshotState`
- `snapshot_state.py`: class `SnapshotStateError`
- `snapshot_state.py`: function `can_transition()`
- `snapshot_state.py`: function `assert_transition()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
