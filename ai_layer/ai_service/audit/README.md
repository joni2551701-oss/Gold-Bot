# ai_layer / ai_service / audit

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `provider_stats.py` -- AI Layer — Provider Stats (Phase 61.0: AI Infrastructure Foundation,
- `request_log.py` -- AI Layer — AI Request Log (Phase 61.0: AI Infrastructure Foundation,
- `response_log.py` -- AI Layer — AI Response Log (Phase 61.0: AI Infrastructure Foundation,
- `trace.py` -- AI Layer — Runtime Trace (Phase 61.3: AI Intelligence Layer, TASK 8).
- `usage_accounting.py` -- AI Layer — AI Usage Accounting (Phase 61.4: AI Product & Control

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `provider_stats.py`: class `ProviderStats`
- `provider_stats.py`: class `DailyUsage`
- `provider_stats.py`: class `RuntimeMetrics`
- `provider_stats.py`: class `RuntimeMetricsCollector`
- `provider_stats.py`: function `compute_provider_stats()`
- `provider_stats.py`: function `rank_providers()`
- `provider_stats.py`: function `compute_requests_per_minute()`
- `provider_stats.py`: function `compute_daily_usage()`
- `provider_stats.py`: function `evaluate_cost_protection()`
- `request_log.py`: class `AIRequestLogEntry`
- `request_log.py`: class `RequestLog`
- `response_log.py`: class `AIResponseLogEntry`
- `response_log.py`: class `ResponseLog`
- `trace.py`: class `RuntimeTrace`
- `trace.py`: function `trace_request()`
- `usage_accounting.py`: class `UserUsageStats`
- `usage_accounting.py`: function `compute_user_usage()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
