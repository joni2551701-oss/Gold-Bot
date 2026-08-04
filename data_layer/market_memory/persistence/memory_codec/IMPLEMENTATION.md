# IMPLEMENTATION.md — data_layer/market_memory/persistence/memory_codec

## `memory_codec.py`

Public surface:

- `annotations`
- `gzip`
- `hashlib`
- `json`
- `dataclass`
- `datetime`
- `timezone`
- `Dict`
- `List`
- `Tuple`
- `Candle`
- `MarketMemory`
- `SCHEMA_VERSION`
- `SnapshotMetadata`
- `MemoryCodec`

## Design Notes

Converted from a flat `memory_codec.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `memory_codec.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
