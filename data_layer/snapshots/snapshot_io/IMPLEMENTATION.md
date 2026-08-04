# IMPLEMENTATION.md — data_layer/snapshots/snapshot_io

## `snapshot_io.py`

Public surface:

- `annotations`
- `base64`
- `datetime`
- `Optional`
- `Tuple`
- `CandleClock`
- `MemoryCodec`
- `SCHEMA_VERSION`
- `check_series`
- `SnapshotCatalog`
- `CatalogEntry`
- `SnapshotManifest`
- `utcnow`
- `SnapshotState`
- `VerifyState`
- `CORE_VERSION`
- `can_transition`
- `SnapshotLifecycle`
- `SnapshotNotFoundError`
- `ENVELOPE_FORMAT_VERSION`
- `SnapshotIncompatibleError`
- `SnapshotImportError`
- `SnapshotIO`

## Design Notes

Converted from a flat `snapshot_io.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `snapshot_io.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
