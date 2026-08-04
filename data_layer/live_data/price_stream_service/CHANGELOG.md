# CHANGELOG.md -- data_layer/live_data/price_stream_service

## v1.1.0 -- 2026-08-04 (GFL-001 FLOW-001, Current Price Flow)

### Added
- `get_shared_price_stream_service()` / `reset_shared_price_stream_service()`
  -- process darajasida yagona (shared) `PriceStreamService` instance.

### Changed
- `build_default_price_stream_service()` endi har bir `register_source()`
  chaqiruviga default `StreamValidator`ni ulaydi va default
  `MarketMemoryRegistry()` yaratadi (Consumer: Market Memory).

### Fixed
- `/price` buyrug'i doim bo'sh narx qaytarar edi, chunki hech kim
  `tick()`ni chaqirmagan va har bir o'quvchi o'z alohida instance'ini
  qurar edi -- endi umumiy instance orqali hal qilindi.

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
