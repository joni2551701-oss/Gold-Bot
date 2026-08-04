# IMPLEMENTATION.md — data_layer/snapshots/manager

## `manager.py`

Public surface:

- `annotations`
- `itertools`
- `datetime`
- `Dict`
- `List`
- `Optional`
- `CandleClock`
- `MarketMemory`
- `MemoryCodec`
- `StorageBackend`
- `EventBus`
- `Event`
- `EventType`
- `SnapshotCatalog`
- `CatalogEntry`
- `utcnow`
- `SnapshotRegistry`
- `SnapshotLifecycle`
- `SnapshotPolicy`
- `SnapshotCleanup`
- `SnapshotIO`
- `SnapshotMetrics`
- `VerifyState`
- `SnapshotManager`

## Design Notes

Converted from a flat `manager.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `manager.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
