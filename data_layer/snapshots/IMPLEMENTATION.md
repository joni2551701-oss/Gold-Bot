# IMPLEMENTATION.md -- data_layer/snapshots

## `catalog.py`

Snapshot catalog + manifest (v1.1 Phase 1, module 9).

Classes: `SnapshotManifest`, `CatalogEntry`, `SnapshotCatalog`

Top-level functions: `utcnow()`

## `cleanup.py`

SnapshotCleanup -- applies a SnapshotPolicy to remove/rotate snapshots

Classes: `SnapshotCleanup`

## `lifecycle.py`

SnapshotLifecycle -- create / verify / archive / delete (v1.1 Phase 1,

Classes: `SnapshotLockedError`, `SnapshotNotFoundError`, `SnapshotLifecycle`

## `manager.py`

SnapshotManager -- the facade that composes the module-9 snapshot

Classes: `SnapshotManager`

## `metrics.py`

SnapshotMetrics -- infrastructure metrics (module 9).

Classes: `SnapshotMetrics`

## `policy.py`

SnapshotPolicy -- retention / rotation / expiration rules (v1.1 Phase 1,

Classes: `SnapshotPolicy`

## `registry.py`

SnapshotRegistry -- the query API over the catalog (v1.1 Phase 1,

Classes: `SnapshotRegistry`

## `snapshot_io.py`

SnapshotIO -- portable export / import of a snapshot (v1.1 Phase 1,

Classes: `SnapshotIncompatibleError`, `SnapshotImportError`, `SnapshotIO`

## `snapshot_state.py`

Snapshot state machine (v1.1 Phase 1, module 9; amendment 3).

Classes: `VerifyState`, `SnapshotState`, `SnapshotStateError`

Top-level functions: `can_transition()`, `assert_transition()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
