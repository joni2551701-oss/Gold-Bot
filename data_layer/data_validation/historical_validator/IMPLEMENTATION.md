# IMPLEMENTATION.md -- data_layer/data_validation/historical_validator

## `historical_validator.py`

Validates a completed historical candle series (coverage, ordering, intraday gaps) against the expected timeframe cadence and returns an immutable ValidationReport. Reuses DataQuality's INTERVAL_DELTAS. Never generates signals, trades, or uses AI.

Public surface:

- `validate_historical_candles() -> ValidationReport`
- `ValidationReport (frozen dataclass)`

## Design Notes

Pure, deterministic validation over an in-memory candle sequence. No I/O,
no network, no shared mutable state. Constants are module-level (named,
never inlined). This module was converted from a flat `historicalvalidator.py`
into a canonical package under GEL-001 with zero behavioural change; the
public import path is preserved by the package `__init__` re-export.

---
*Generated 2026-08-03 under GEL-001 (Development v1).*
