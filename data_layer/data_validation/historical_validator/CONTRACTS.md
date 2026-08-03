# CONTRACTS.md -- data_layer/data_validation/historical_validator

## Input

See `README.md` Public API (the `historical_validator.py` function signatures).

## Output

Immutable result object (see Public API). Never raises into callers on
ordinary bad data -- degrades to an invalid/empty result.

## Events

None.

## Public API

- `validate_historical_candles() -> ValidationReport`
- `ValidationReport (frozen dataclass)`

## Internal API

See `MODULE_MAP.md`.

## Ownership

Canonical module `data_layer/data_validation/historical_validator` (Data Layer / Data_Validation).

## Dependencies

Reads `data_layer.data_validation.data_quality.INTERVAL_DELTAS`. Forbidden: Context, Strategy, Signal, AI, Decision, Risk.

## Runtime Rules

Read-only validation. Never generates signals, never trades, never uses AI.

---
*Generated 2026-08-03 under GEL-001 (Development v1). Import path preserved.*
