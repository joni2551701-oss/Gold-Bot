# IMPLEMENTATION.md -- data_layer/live_data

## `bitget_price_source.py`

BitgetPriceSource -- a PriceProvider adapter over the existing

Classes: `BitgetPriceSource`

## `candle_clock.py`

CandleClock -- pure, deterministic timeframe-boundary math (v1.1 Phase 1,

Classes: `CandleClock`

## `market_data.py`

Classes: `MarketSnapshot`, `MarketDataNormalizer`

## `market_data_service.py`

MarketDataService -- the Data Layer facade for candle-shaped market

Classes: `MarketDataService`

Top-level functions: `build_default_market_data_service()`

## `market_data_snapshot.py`

Data Layer — Market Data Snapshot foundation (Phase 59 Preparation,

Classes: `MarketDataSnapshot`

Top-level functions: `generate_market_snapshot_id()`, `compute_candles_reference()`, `capture_market_data_snapshot()`

## `price_cache.py`

PriceCache -- per-symbol latest `PriceTick` store (TASK-DATA-001, Price

Classes: `PriceCache`

## `price_stream.py`

PriceStream -- per-asset market lifecycle state machine that pulls from a

Classes: `MarketCalendar`, `AlwaysOpenCalendar`, `PriceStream`

## `price_tick.py`

PriceTick -- the unified, provider-agnostic price observation

Classes: `PriceTick`

## `provider.py`

PriceProvider -- the abstract, vendor-agnostic provider interface

Classes: `PriceProvider`

## `session_filter.py`

Top-level functions: `get_tashkent_time()`, `is_trading_time()`

## `stream_event.py`

Stream models -- StreamEvent and the state/status/capability value types

Classes: `StreamState`, `ProviderStatus`, `AssetClass`, `ProviderCapabilities`, `ProviderHealth`, `StreamEvent`

## `stream_manager.py`

StreamManager -- supervises one PriceStream per asset (v1.1 Phase 1,

Classes: `StreamManager`

## `twelve_data_provider.py`

TwelveDataProvider -- a PriceProvider adapter over the existing

Classes: `TwelveDataProvider`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
