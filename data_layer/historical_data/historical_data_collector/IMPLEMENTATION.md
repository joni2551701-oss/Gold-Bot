# IMPLEMENTATION.md — data_layer/historical_data/historical_data_collector

## `historical_data_collector.py`

Public surface:

- `dataclass`
- `datetime`
- `timezone`
- `TYPE_CHECKING`
- `List`
- `Optional`
- `INTERVAL_DELTAS`
- `RawCandleRepository`
- `setup_logger`
- `logger`
- `MAX_FETCH_LIMIT`
- `CollectionResult`
- `collect_historical_candles`
- `sync_historical_candles`

## Design Notes

Converted from a flat `historical_data_collector.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `historical_data_collector.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
