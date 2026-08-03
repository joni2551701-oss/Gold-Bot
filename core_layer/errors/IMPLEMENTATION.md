# IMPLEMENTATION.md -- core_layer/errors

## `base.py`

Core Errors — GoldBotError base (Phase A18).

Classes: `GoldBotError`

## `codes.py`

Core Errors — standard error code registry (Phase A18).

Top-level functions: `is_valid_code_format()`, `is_known_code()`

## `exceptions.py`

Core Errors — the nine GoldBotError subclasses (Phase A18).

Classes: `ConfigurationError`, `ValidationError`, `DataError`, `ExternalAPIError`, `DatabaseError`, `PermissionError`, `StrategyError`, `DecisionError`, `ExecutionError`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
