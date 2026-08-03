# MODULE_MAP.md -- data_layer/snapshots

| File | Role |
|---|---|
| `__init__.py` | data_layer.snapshots -- GoldBot v1.1 Market Data Foundation: Snapshot |
| `catalog.py` | Snapshot catalog + manifest (v1.1 Phase 1, module 9). |
| `cleanup.py` | SnapshotCleanup -- applies a SnapshotPolicy to remove/rotate snapshots |
| `lifecycle.py` | SnapshotLifecycle -- create / verify / archive / delete (v1.1 Phase 1, |
| `manager.py` | SnapshotManager -- the facade that composes the module-9 snapshot |
| `metrics.py` | SnapshotMetrics -- infrastructure metrics (module 9). |
| `policy.py` | SnapshotPolicy -- retention / rotation / expiration rules (v1.1 Phase 1, |
| `registry.py` | SnapshotRegistry -- the query API over the catalog (v1.1 Phase 1, |
| `snapshot_io.py` | SnapshotIO -- portable export / import of a snapshot (v1.1 Phase 1, |
| `snapshot_state.py` | Snapshot state machine (v1.1 Phase 1, module 9; amendment 3). |

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Table is mechanically generated from each file's own first docstring line.*
