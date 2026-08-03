# CONTRACTS.md -- data_layer/data_validation/data_quality

## Input

See `README.md` Public API (the `data_quality.py` function signatures).

## Output

Immutable result object (see Public API). Never raises into callers on
ordinary bad data -- degrades to an invalid/empty result.

## Events

None.

## Public API

- `assess_data_quality() -> DataQualityResult`
- `DataQualityResult (frozen dataclass: valid, score, issues)`
- `INTERVAL_DELTAS, INVALID_OHLC_PENALTY, DUPLICATE_CANDLE_PENALTY, MISSING_CANDLE_PENALTY, TIMEFRAME_MISMATCH_PENALTY (constants)`

## Internal API

See `MODULE_MAP.md`.

## Ownership

Canonical module `data_layer/data_validation/data_quality` (Data Layer / Data_Validation).

## Dependencies

Reads `data_layer.providers.twelve_data_client.Candle`. Forbidden: Context, Strategy, Signal, AI, Decision, Risk.

## Runtime Rules

Read-only validation. Never generates signals, never trades, never uses AI.

---
*Generated 2026-08-03 under GEL-001 (Development v1). Import path preserved.*
