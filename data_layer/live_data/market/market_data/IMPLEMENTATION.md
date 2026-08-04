# IMPLEMENTATION.md — data_layer/live_data/market/market_data

## `market_data.py`

Public surface:

- `dataclass`
- `field`
- `datetime`
- `timezone`
- `List`
- `Optional`
- `Candle`
- `MarketPrice`
- `LiquidityState`
- `MarketStructureView`
- `RegimeState`
- `SessionState`
- `TrendState`
- `VolatilityLevel`
- `MarketData`
- `MarketStateSnapshot`
- `MarketSnapshot`

## Design Notes

Converted from a flat `market_data.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `market_data.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
