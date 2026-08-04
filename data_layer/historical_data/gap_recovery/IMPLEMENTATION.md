# IMPLEMENTATION.md — data_layer/historical_data/gap_recovery

## `gap_recovery.py`

Public surface:

- `annotations`
- `datetime`
- `timedelta`
- `Optional`
- `setup_logger`
- `CandleClock`
- `MarketMemory`
- `CandleSource`
- `HistoricalProvider`
- `logger`
- `GapRecovery`

## Design Notes

Converted from a flat `gap_recovery.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `gap_recovery.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
