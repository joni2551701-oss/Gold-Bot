# IMPLEMENTATION.md — context_layer/context_engine/snapshot

## `snapshot.py`

Public surface:

- `json`
- `uuid`
- `asdict`
- `dataclass`
- `field`
- `datetime`
- `timezone`
- `List`
- `Optional`
- `ContextSnapshot`
- `most_recent_bias`
- `ALLOWED_REGIMES`
- `StructureInfo`
- `LiquidityInfo`
- `ZonesInfo`
- `SessionInfo`
- `SnapshotMetadata`
- `ContextSnapshotSchema`
- `generate_snapshot_id`
- `ValidationResult`
- `validate_snapshot`
- `from_context_snapshot`

## Design Notes

Converted from a flat `snapshot.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `snapshot.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
