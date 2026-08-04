# IMPLEMENTATION.md — data_layer/live_data/stream/price_stream

## `price_stream.py`

Public surface:

- `datetime`
- `List`
- `Optional`
- `CurrentPrice`
- `StreamEvent`
- `StreamMode`
- `resolve_mode`
- `RouteResult`
- `StreamRouter`
- `StreamState`
- `StreamSubscriber`
- `StreamValidator`
- `ValidationResult`
- `IngestResult`
- `PriceStream`

## Design Notes

Converted from a flat `price_stream.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `price_stream.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
