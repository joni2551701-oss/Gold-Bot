# IMPLEMENTATION.md — context_layer/context_engine/candle

## `candle.py`

Public surface:

- `IntEnum`
- `Candle`
- `CandleDirection`
- `direction`
- `is_bullish`
- `is_bearish`
- `is_doji`
- `body_size`
- `upper_wick`
- `lower_wick`
- `range_size`
- `body_ratio`

## Design Notes

Converted from a flat `candle.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `candle.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
