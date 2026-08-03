# CONTRACTS.md -- platform_layer/telegram/owner

## Input

Not independently specified beyond the module's own code at rollout time -- see `README.md` Public API.

## Output

Not independently specified beyond the module's own code at rollout time -- see `README.md` Public API.

## Events

None documented at rollout time.

## Public API

See `README.md`.

## Internal API

See `MODULE_MAP.md`.

## Ownership

Module `platform_layer/telegram/owner`.

## Dependencies

Cross-layer imports found mechanically in this module's own `.py` files at rollout time:

- `ai_layer.ai_coordinator`
- `ai_layer.ai_engine`
- `ai_layer.ai_service`
- `ai_layer.knowledge_ai`
- `ai_layer.personal_ai`
- `backtesting_layer.backtest_engine`
- `backtesting_layer.backtest_report`
- `backtesting_layer.replay_controller`
- `backtesting_layer.replay_engine`
- `backtesting_layer.statistics`
- `context_layer.fundamental`
- `core_layer.configuration`
- `core_layer.emergency`
- `core_layer.health_monitor`
- `core_layer.logger`
- `core_layer.secrets`
- `core_layer.system_state`
- `data_layer.providers`
- `database_layer.audit_log`
- `database_layer.journal_repository`
- `database_layer.market_repository`
- `database_layer.trade_repository`
- `database_layer.user_repository`
- `decision_layer.decision_logger`
- `execution_layer.execution_engine`
- `media_layer.translation`
- `platform_layer.telegram`
- `signal_layer.signal_builder`

## Runtime Rules

None documented beyond what CLAUDE.md's Trading Safety section already states at the repository level.

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Dependencies list is mechanically derived from actual `import` statements, not asserted from design intent.*
