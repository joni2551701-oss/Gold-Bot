# data_layer/data_validation/historical_validator

**Module** (HistoricalValidator) -- GoldBot Engineering Law GEL-001: one module = one package.

## Purpose

Validates a completed historical candle series (coverage, ordering, intraday gaps) against the expected timeframe cadence and returns an immutable ValidationReport. Reuses DataQuality's INTERVAL_DELTAS. Never generates signals, trades, or uses AI.

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this package.

## Dependencies

Reads: `data_layer.data_validation.data_quality.INTERVAL_DELTAS`. Cross-layer dependency direction is downstream-only
(Data Layer internal / providers), matching Layer_Contracts.md. No import
from Context, Strategy, Signal, AI, Decision, or Risk.

## Public API

- `validate_historical_candles() -> ValidationReport`
- `ValidationReport (frozen dataclass)`

Import (stable, GEL-001 package form):

    from data_layer.data_validation.historical_validator import validate_historical_candles

## Consumers

backtesting_layer.statistics.dataset_report, tests/data/test_historical_validator

---
*Canonical module package created 2026-08-03 under GoldBot Engineering Law
GEL-001 (Development v1). Implementation moved intact from the former flat
`historicalvalidator.py`; public import path preserved via this package's
`__init__` re-export. No behaviour changed.*
