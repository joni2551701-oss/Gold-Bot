# IMPLEMENTATION.md — data_layer/live_data/market_data

## `market_data.py`

Public surface:

- `List`
- `Dict`
- `dataclass`
- `field`
- `timedelta`
- `Config`
- `TwelveDataClient`
- `Candle`
- `classify_api_error`
- `setup_logger`
- `logger`
- `MarketSnapshot`
- `MarketDataNormalizer`

## Design Notes

Converted from a flat `market_data.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `market_data.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
