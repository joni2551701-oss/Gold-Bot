# IMPLEMENTATION.md -- data_layer/historical_data

## `bootstrap_events.py`

BootstrapEventHook -- lifecycle events emitted by the Historical Bootstrap

Classes: `BootstrapEventHook`

## `bootstrap_metrics.py`

BootstrapMetrics -- per-asset bootstrap metrics (DD-057).

Classes: `BootstrapMetrics`

## `bootstrap_progress.py`

BootstrapProgress -- observable bootstrap progress (DD-054).

Classes: `BootstrapProgress`

## `bootstrap_state.py`

Bootstrap state and strategy enums (v1.1 Phase 1, module 5).

Classes: `BootstrapState`, `BootstrapStrategy`

## `gap_recovery.py`

GapRecovery -- detect and fill missing candle windows in memory

Classes: `GapRecovery`

## `historical_bootstrap.py`

HistoricalBootstrap -- the per-asset bootstrap orchestrator (v1.1 Phase 1,

Classes: `HistoricalBootstrap`

## `historical_data_collector.py`

Data Layer — Historical Data Collector (Phase 59.5: Historical Data

Classes: `CollectionResult`

Top-level functions: `collect_historical_candles()`, `sync_historical_candles()`

## `historical_provider.py`

HistoricalProvider -- vendor-agnostic historical data interface (mirrors

Classes: `HistoricalProvider`, `BootstrapCache`, `InMemoryBootstrapCache`

## `twelve_data_historical_provider.py`

TwelveDataHistoricalProvider -- a HistoricalProvider adapter over the

Classes: `TwelveDataHistoricalProvider`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
