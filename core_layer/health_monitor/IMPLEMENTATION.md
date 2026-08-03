# IMPLEMENTATION.md -- core_layer/health_monitor

## `access.py`

Monitoring Layer — Access Gate (Phase B.0 Rule 5: "Feature Flag

Top-level functions: `is_owner_monitoring_enabled()`

## `error_monitor.py`

Monitoring Layer — Error Monitor (GoldBot Core Owner Monitoring Alpha,

Classes: `ErrorMonitor`

## `health_monitor.py`

Monitoring Layer — Health Monitor (Phase B.0 TASK 6's own genuine gap,

Top-level functions: `classify_health()`

## `market_monitor.py`

Monitoring Layer — Market Data Monitor (GoldBot Core Owner Monitoring

Top-level functions: `get_market_health()`

## `models.py`

Monitoring Layer — Foundation Models (GoldBot Core Owner Monitoring

Classes: `SystemHealth`, `MarketHealth`, `SignalHealth`, `ErrorSeverity`, `ErrorEvent`, `DecisionPipelineEntry`, `HealthStatus`, `ResourceSnapshot`, `PerformanceCounters`

## `performance.py`

Classes: `PerformanceConfig`, `StrategyStats`, `ConfidenceBucketStats`, `PerformanceResult`, `PerformanceTracker`

## `performance_collector.py`

Monitoring Layer — Performance Collector (Phase B.0 TASK 7's own

Classes: `PerformanceCollector`

Top-level functions: `get_counts()`, `record_signal()`, `record_decision()`, `record_trade()`, `record_reject()`, `record_error()`, `record_reconnect()`

## `provider_health.py`

Monitoring Layer — Provider Health (Phase 59.2, TASK 6).

Classes: `ProviderHealthStatus`, `ProviderHealthReport`

Top-level functions: `check_provider_health()`, `check_registry_health()`

## `resource_monitor.py`

Monitoring Layer — Resource Monitor (Phase B.0 TASK 2's own genuine

Top-level functions: `record_process_start()`, `get_resource_snapshot()`

## `risk_monitor.py`

Monitoring Layer — Risk Monitor (Phase V1.0.1: Risk Management

Classes: `RiskCounts`, `RiskMonitor`

Top-level functions: `get_risk_counts()`

## `signal_monitor.py`

Classes: `MonitorConfig`, `MonitorResult`, `SignalMonitor`

Top-level functions: `get_signal_health()`

## `system_monitor.py`

Monitoring Layer — System Monitor (GoldBot Core Owner Monitoring

Classes: `SystemMonitor`

Top-level functions: `get_health()`, `record_scan()`, `record_error()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
