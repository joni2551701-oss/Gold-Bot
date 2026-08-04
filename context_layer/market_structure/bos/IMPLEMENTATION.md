# IMPLEMENTATION.md — context_layer/market_structure/bos

## `bos.py`

Public surface:

- `dataclass`
- `Enum`
- `List`
- `Sequence`
- `datetime`
- `Candle`
- `StructurePoint`
- `StructureType`
- `setup_logger`
- `logger`
- `BosDirection`
- `BosEvent`
- `detect_bos`

## Design Notes

Converted from a flat `bos.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `bos.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
