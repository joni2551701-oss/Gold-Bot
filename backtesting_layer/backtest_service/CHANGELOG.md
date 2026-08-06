# CHANGELOG.md -- backtesting_layer/backtest_service

## v1.1.0 -- 2026-08-06 (FLOW-018 Production Wiring)

### Added
- `backtest_service.py`: real `BacktestService` (composition root) —
  `BacktestRequest` (Input Contract), `BacktestOutcome` (Output
  Contract), `parse_backtest_request()`, `run()` / `run_from_args()`,
  `get_backtest_service()`. Composes the existing, unmodified
  `BacktestEngine` + `format_backtest_report` + `ReplayConfig`; no new
  backtesting/trading logic. Tool-First: reads Historical Data from the
  DB via ReplayEngine, no external API. Live consumer: Telegram
  `/backtest` (`platform_layer/telegram/handlers.backtest_handler`).

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
