# IMPLEMENTATION.md -- data_layer/data_validation/data_quality

## `data_quality.py`

Assesses market-data integrity for a candle series: OHLC validity, duplicate candles, missing candles, and timeframe alignment. Returns an immutable DataQualityResult (valid flag + 0-100 score + issue list). Never generates signals, trades, or uses AI -- pure data validation.

Public surface:

- `assess_data_quality() -> DataQualityResult`
- `DataQualityResult (frozen dataclass: valid, score, issues)`
- `INTERVAL_DELTAS, INVALID_OHLC_PENALTY, DUPLICATE_CANDLE_PENALTY, MISSING_CANDLE_PENALTY, TIMEFRAME_MISMATCH_PENALTY (constants)`

## Design Notes

Pure, deterministic validation over an in-memory candle sequence. No I/O,
no network, no shared mutable state. Constants are module-level (named,
never inlined). This module was converted from a flat `dataquality.py`
into a canonical package under GEL-001 with zero behavioural change; the
public import path is preserved by the package `__init__` re-export.

---
*Generated 2026-08-03 under GEL-001 (Development v1).*
