# CHANGELOG.md — data_layer/live_data/market_data_service

## v1.1.0 — 2026-08-04 (GFL-001 FLOW-004, Market Engine Flow)

### Added
- `MarketDataService.get_candles_from_memory()` -- reads a closed-candle
  series back OUT of Market Memory via the canonical `MemoryReader`
  facade, shaped exactly like `get_candles()`'s own return value.
- `get_shared_market_data_service()` / `reset_shared_market_data_service()`
  -- process-wide singleton sharing the same `MarketMemoryRegistry` as
  `data_layer.live_data.price_stream_service.get_shared_price_stream_service()`.

### Changed
- None (existing `get_candles()`/`get_snapshot()`/`get_historical_candles()`
  untouched, no signature changes).

### Fixed
- None.

## v1.0.0 — 2026-08-04

GEL-001 (Strict) canonical package form.

### Added
- Package `__init__.py` re-exporting the public surface (import-path stable).
- GEL-001 standard doc set.

### Changed
- Converted from flat `market_data_service.py` to package `market_data_service/` (GEL-001 Strict). No behavioural change; implementation moved intact.

### Fixed / Removed / Deprecated
- None.
