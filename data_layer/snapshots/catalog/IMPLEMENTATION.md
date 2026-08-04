# IMPLEMENTATION.md — data_layer/snapshots/catalog

## `catalog.py`

Public surface:

- `annotations`
- `json`
- `dataclass`
- `asdict`
- `datetime`
- `timezone`
- `Dict`
- `List`
- `Optional`
- `Tuple`
- `SnapshotState`
- `VerifyState`
- `CORE_VERSION`
- `SnapshotManifest`
- `CatalogEntry`
- `SnapshotCatalog`
- `utcnow`

## Design Notes

Converted from a flat `catalog.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `catalog.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
