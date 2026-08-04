# IMPLEMENTATION.md — data_layer/live_data/price_stream

## `price_stream.py`

Public surface:

- `annotations`
- `datetime`
- `timedelta`
- `timezone`
- `Optional`
- `List`
- `Any`
- `Dict`
- `Protocol`
- `runtime_checkable`
- `setup_logger`
- `PriceProvider`
- `StreamEvent`
- `StreamState`
- `ProviderStatus`
- `AssetClass`
- `logger`
- `MarketCalendar`
- `AlwaysOpenCalendar`
- `PriceStream`

## Design Notes

Converted from a flat `price_stream.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `price_stream.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
