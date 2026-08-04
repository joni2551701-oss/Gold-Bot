# CHANGELOG.md -- data_layer/market_memory

## v1.1.0 -- 2026-08-04 (GFL-001 FLOW-003, Market Memory Flow)

### Added
- None (Consumer contract -- `MemoryReader`, `MarketManager` -- was
  already fully built and tested; the production gap closed was in
  `data_layer/live_data/price_stream_service` -- see that module's
  CHANGELOG).

### Changed
- None.

### Fixed
- Confirmed and end-to-end tested: the Producer (Data Validation via
  `CandleBuilder`) -> Market Memory -> Consumer (`MemoryReader` /
  `MarketManager`) chain now has a genuine, sanctioned read path
  (`PriceStreamService.memory_registry`) proven by a live-tick E2E
  test -- previously the Consumer facade was built but never reachable
  from a real registry outside tests.

### Removed
- None.

### Deprecated
- None.

## v1.0.0 -- 2026-08-03

### Added
- Initial Engineering Standard (Director Order No. 012/013).

### Changed
- None.

### Fixed
- None.

### Removed
- None.

### Deprecated
- None.
