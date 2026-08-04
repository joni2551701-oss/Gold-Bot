# CHANGELOG.md -- data_layer/live_data/current_price_provider

## v1.1.0 -- 2026-08-04 (GFL-001 FLOW-001, Current Price Flow)

### Changed
- `PriceStreamLastPriceSource`'ning default backend'i endi
  `get_shared_price_stream_service()` orqali umumiy (shared)
  `PriceStreamService`'ga ulanadi (avval har chaqiruvda alohida,
  hech qachon "tick" qilinmagan instance qurar edi). Public API
  o'zgarmadi.

### Fixed
- `/price` uchun default o'quvchi endi haqiqiy, "tick" qilingan
  narxni ko'ra oladi.

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
