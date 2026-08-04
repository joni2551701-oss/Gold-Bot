# IMPLEMENTATION.md — data_layer/live_data/market/market_manager

## `market_manager.py`

Public surface:

- `dataclass`
- `datetime`
- `List`
- `Optional`
- `Candle`
- `MarketPrice`
- `read_current_price`
- `LiquidityState`
- `MarketData`
- `MarketStateSnapshot`
- `MarketStructureView`
- `RegimeState`
- `SessionState`
- `TrendState`
- `VolatilityLevel`
- `MarketState`
- `MarketManager`

## Design Notes

Converted from a flat `market_manager.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `market_manager.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
