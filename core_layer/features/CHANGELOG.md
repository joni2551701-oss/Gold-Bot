# CHANGELOG.md -- core_layer/features

## v1.1.0 -- 2026-08-04 (GFL-001 FLOW-007, Indicator Engine, Director-approved)

### Added
- `core_layer/features/atr/` -- Wilder's Average True Range
  (`compute_atr(candles, period=14)`), computed from
  `ContextSnapshot.candles`. None when fewer than `period + 1` candles
  are available.

### Changed
- `feature_engine.compute_market_features()` -- `atr` is now
  `compute_atr(context.candles)` instead of always `None`. Still
  purely advisory: not passed into SignalEngine/AIAnalyzer/
  DecisionEngine/RiskManager.
- `feature_model.MarketFeatures.atr` docstring updated to describe
  the real computation instead of the former always-None hook.

### Fixed
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
