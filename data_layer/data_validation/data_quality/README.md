# data_layer/data_validation/data_quality

**Module** (DataQuality) -- GoldBot Engineering Law GEL-001: one module = one package.

## Purpose

Assesses market-data integrity for a candle series: OHLC validity, duplicate candles, missing candles, and timeframe alignment. Returns an immutable DataQualityResult (valid flag + 0-100 score + issue list). Never generates signals, trades, or uses AI -- pure data validation.

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this package.

## Dependencies

Reads: `data_layer.providers.twelve_data_client.Candle`. Cross-layer dependency direction is downstream-only
(Data Layer internal / providers), matching Layer_Contracts.md. No import
from Context, Strategy, Signal, AI, Decision, or Risk.

## Public API

- `assess_data_quality() -> DataQualityResult`
- `DataQualityResult (frozen dataclass: valid, score, issues)`
- `INTERVAL_DELTAS, INVALID_OHLC_PENALTY, DUPLICATE_CANDLE_PENALTY, MISSING_CANDLE_PENALTY, TIMEFRAME_MISMATCH_PENALTY (constants)`

Import (stable, GEL-001 package form):

    from data_layer.data_validation.data_quality import assess_data_quality

## Consumers

core_layer.pipeline.pipeline, data_layer.live_data.stream_validator, data_layer.historical_data.historical_data_collector, backtesting_layer.statistics.gap_report

---
*Canonical module package created 2026-08-03 under GoldBot Engineering Law
GEL-001 (Development v1). Implementation moved intact from the former flat
`dataquality.py`; public import path preserved via this package's
`__init__` re-export. No behaviour changed.*
