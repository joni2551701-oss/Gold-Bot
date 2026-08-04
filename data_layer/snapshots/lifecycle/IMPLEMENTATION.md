# IMPLEMENTATION.md — data_layer/snapshots/lifecycle

## `lifecycle.py`

Public surface:

- `annotations`
- `hashlib`
- `datetime`
- `Optional`
- `setup_logger`
- `MemoryCodec`
- `StorageBackend`
- `check_series`
- `CandleClock`
- `MarketMemory`
- `SnapshotCatalog`
- `CatalogEntry`
- `utcnow`
- `SnapshotState`
- `VerifyState`
- `assert_transition`
- `can_transition`
- `CORE_VERSION`
- `logger`
- `SnapshotLockedError`
- `SnapshotNotFoundError`
- `SnapshotLifecycle`

## Design Notes

Converted from a flat `lifecycle.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `lifecycle.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
