# IMPLEMENTATION.md — data_layer/historical_data/historical_bootstrap

## `historical_bootstrap.py`

Public surface:

- `annotations`
- `datetime`
- `timedelta`
- `timezone`
- `Optional`
- `List`
- `Dict`
- `Mapping`
- `setup_logger`
- `CandleClock`
- `TIMEFRAME_ORDER`
- `Candle`
- `MarketMemory`
- `CandleSource`
- `BootstrapState`
- `BootstrapStrategy`
- `BootstrapProgress`
- `BootstrapMetrics`
- `HistoricalProvider`
- `BootstrapCache`
- `GapRecovery`
- `BootstrapEventHook`
- `logger`
- `HistoricalBootstrap`

## Design Notes

Converted from a flat `historical_bootstrap.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `historical_bootstrap.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
