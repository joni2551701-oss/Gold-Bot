# IMPLEMENTATION.md -- data_layer/market_memory

## `candle_record.py`

CandleRecord -- the extended in-memory candle model (DD-027).

Classes: `CandleStatus`, `CandleSource`, `MemoryMode`, `CandleRecord`

## `data_cache.py`

Classes: `SmartDataCache`

## `market_memory.py`

MarketMemory -- one asset's multi-timeframe memory (DD-030 non-singleton,

Classes: `MarketMemory`

## `market_memory_registry.py`

MarketMemoryRegistry -- asset -> MarketMemory (DD-030).

Classes: `DuplicateAssetError`, `UnknownAssetError`, `MarketMemoryRegistry`

Top-level functions: `build_default_registry()`

## `timeframe_memory.py`

TimeframeMemory -- one timeframe's independent, thread-safe candle store

Classes: `TimeframeMemory`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
