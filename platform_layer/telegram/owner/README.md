# platform_layer / telegram / owner

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `ai_commands.py` -- Telegram Layer — Owner AI Commands (Phase 61.4: AI Product & Control
- `backtest_commands.py` -- Telegram Layer — Owner Backtest Commands (Phase 60.2: Backtesting
- `broadcast_commands.py` -- Telegram Layer — Owner Broadcast Commands (Phase 63.0: Senior Trading
- `control_commands.py` -- Telegram Layer — Owner Control Commands (Phase 59.8: Owner Control
- `dashboard.py` -- Telegram Layer — Owner Dashboard (Phase 59.8: Owner Control Center;
- `dataset_commands.py` -- Telegram Layer — Owner Dataset Commands (Phase 59.5: Historical Data
- `emergency_commands.py` -- Telegram Layer — Owner Emergency Commands (Phase 59.9: Emergency Safety
- `execution_commands.py` -- Telegram Layer — Owner Execution Commands (Phase 60.3: Execution
- `feature_commands.py` -- Telegram Layer — Owner Feature Commands (Phase 59.3, TASK 5). Same
- `fundamental_commands.py` -- Telegram Layer — Owner Fundamental Commands (Phase 60.5: Fundamental
- `learning_commands.py` -- Telegram Layer — Owner Learning Commands (Phase 60.6: Learning Loop
- `monitoring_commands.py` -- Telegram Layer — Owner Monitoring Commands (GoldBot Core Owner
- `owner_roles.py` -- Telegram Layer — Owner Permission System foundation (Phase 59.6: Audit
- `performance_commands.py` -- Telegram Layer — Owner Performance Commands (Phase 60.4: Performance
- `provider_commands.py` -- Telegram Layer — Owner Provider Commands (Phase 59.3, TASK 5: Owner
- `replay_commands.py` -- Telegram Layer — Owner Replay Commands (Phase 60.1: Historical Replay
- `report_commands.py` -- Telegram Layer — Owner Report Commands (Phase 59.4, TASK 5: Owner
- `runtime_commands.py` -- Telegram Layer — Owner Runtime Commands (Phase 61.6: AI Operations &
- `runtime_notifications.py` -- Telegram Layer — Owner Runtime Notifications (Phase 61.6: AI
- `security.py` -- Telegram Layer — Owner Control Center Security (Phase 59.8: Owner
- `status_commands.py` -- Telegram Layer — Owner Status Commands (Phase 59.8: Owner Control
- `system_commands.py` -- Telegram Layer — Owner System Commands (Phase 59.3, TASK 5). Same
- `validation_commands.py` -- Telegram Layer — Owner Validation Commands (Phase 59 Real Market

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `ai_commands.py`: class `AICommandResult`
- `ai_commands.py`: function `resolve_capability()`
- `ai_commands.py`: function `ai_runtime_online()`
- `ai_commands.py`: function `current_provider_for()`
- `ai_commands.py`: function `ai_status()`
- `ai_commands.py`: function `ai_provider()`
- `ai_commands.py`: function `ai_disable()`
- `ai_commands.py`: function `ai_enable()`
- `ai_commands.py`: function `ai_limit()`
- `ai_commands.py`: function `ai_cost()`
- `ai_commands.py`: function `ai_usage()`
- `ai_commands.py`: function `ai_health()`
- `ai_commands.py`: function `ai_explanation_status()`
- `backtest_commands.py`: function `backtest_run()`
- `broadcast_commands.py`: class `BroadcastCommandResult`
- `broadcast_commands.py`: function `broadcast_status()`
- `broadcast_commands.py`: function `broadcast_provider()`
- `broadcast_commands.py`: function `broadcast_enable()`
- `broadcast_commands.py`: function `broadcast_disable()`
- `control_commands.py`: function `get_feature_states()`
- `control_commands.py`: function `enable_feature()`
- `control_commands.py`: function `disable_feature()`
- `dashboard.py`: function `get_dashboard()`
- `dashboard.py`: function `get_owner_summary()`
- `dashboard.py`: function `get_doctor_report()`
- `dataset_commands.py`: function `get_dataset_status()`
- `dataset_commands.py`: function `get_history_status()`
- `dataset_commands.py`: function `get_sync_status()`
- `dataset_commands.py`: function `get_provider_compare()`
- `emergency_commands.py`: function `kill_system()`
- `emergency_commands.py`: function `pause_system()`
- `emergency_commands.py`: function `maintenance_on()`
- `emergency_commands.py`: function `restore_system()`
- `emergency_commands.py`: function `get_emergency_status()`
- `execution_commands.py`: function `execution_status()`
- `execution_commands.py`: function `slippage_status()`
- `execution_commands.py`: function `set_simulation_mode()`
- `feature_commands.py`: function `list_features()`
- `fundamental_commands.py`: function `get_macro_status()`
- `fundamental_commands.py`: function `get_fundamental_score_report()`
- `fundamental_commands.py`: function `get_fed_status()`
- `learning_commands.py`: function `get_learning_status()`
- `learning_commands.py`: function `get_patterns_report()`
- `learning_commands.py`: function `get_failures_report()`
- `learning_commands.py`: function `get_best_conditions_report()`
- `monitoring_commands.py`: function `get_status_report()`
- `monitoring_commands.py`: function `get_performance_report()`
- `monitoring_commands.py`: function `get_health_report()`
- `monitoring_commands.py`: function `get_market_report()`
- `monitoring_commands.py`: function `get_signals_report()`
- `monitoring_commands.py`: function `get_errors_report()`
- `monitoring_commands.py`: function `get_pipeline_report()`
- `monitoring_commands.py`: function `get_daily_report()`
- `owner_roles.py`: class `OwnerRole`
- `owner_roles.py`: function `resolve_owner_role()`
- `performance_commands.py`: function `get_performance_report()`
- `performance_commands.py`: function `get_equity_curve_report()`
- `performance_commands.py`: function `get_backtest_performance_report()`
- `provider_commands.py`: class `ProviderCommandResult`
- `provider_commands.py`: function `list_providers()`
- `provider_commands.py`: function `get_data_status()`
- `provider_commands.py`: function `enable_provider()`
- `provider_commands.py`: function `disable_provider()`
- `replay_commands.py`: function `replay_start()`
- `replay_commands.py`: function `replay_pause()`
- `replay_commands.py`: function `replay_stop()`
- `replay_commands.py`: function `replay_status()`
- `report_commands.py`: function `pick_best_strategy()`
- `report_commands.py`: function `format_daily_stats()`
- `report_commands.py`: function `get_validation_summary()`
- `runtime_commands.py`: class `RuntimeCommandResult`
- `runtime_commands.py`: function `runtime_status()`
- `runtime_commands.py`: function `runtime_events()`
- `runtime_commands.py`: function `runtime_metrics()`
- `runtime_commands.py`: function `runtime_full_status()`
- `runtime_commands.py`: function `runtime_check()`
- `runtime_commands.py`: function `runtime_restart()`
- `runtime_commands.py`: function `runtime_provider()`
- `runtime_notifications.py`: class `RuntimeAlert`
- `runtime_notifications.py`: class `RuntimeNotifier`
- `runtime_notifications.py`: function `evaluate_high_cost()`
- `runtime_notifications.py`: function `evaluate_cache_disabled()`
- `runtime_notifications.py`: function `deliver_alerts()`
- `security.py`: class `SecurityCheckResult`
- `security.py`: function `require_role()`
- `security.py`: function `log_owner_action()`
- `status_commands.py`: function `get_system_status()`
- `system_commands.py`: function `get_system_health()`
- `system_commands.py`: function `count_online_providers()`
- `validation_commands.py`: function `get_validation_status()`
- `validation_commands.py`: function `get_today_signals()`
- `validation_commands.py`: function `get_validation_report()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
