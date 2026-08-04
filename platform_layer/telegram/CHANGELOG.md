# CHANGELOG.md -- platform_layer/telegram

## v1.1.0 -- 2026-08-04 (GFL-001 FLOW-001, Current Price Flow)

### Added
- `_price_stream_tick_loop()` va `PRICE_STREAM_TICK_INTERVAL_SECONDS`
  (`polling.py`) -- `_heartbeat_loop()` bilan bir xil naqshda, Price
  Stream'ni `get_settings().stream.polling_interval` bo'yicha "tick"
  qiladi.

### Changed
- `run_polling()` endi ikkita fon vazifasini (heartbeat + price
  stream tick) parallel ishga tushiradi va yopilishda ikkalasini ham
  bekor qiladi.

### Fixed
- `/price` buyrug'i endi haqiqiy narxni qaytara oladi (avval doim
  bo'sh holat qaytarar edi -- Price Stream hech qachon "tick"
  qilinmasdi).

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
