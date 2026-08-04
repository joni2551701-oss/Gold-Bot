# IMPLEMENTATION.md — data_layer/market_memory/data_cache

## `data_cache.py`

Public surface:

- `os`
- `json`
- `List`
- `Dict`
- `Any`
- `datetime`
- `timezone`
- `timedelta`
- `MarketDataNormalizer`
- `MarketSnapshot`
- `Candle`
- `setup_logger`
- `Config`
- `logger`
- `SmartDataCache`

## Design Notes

Converted from a flat `data_cache.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `data_cache.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
