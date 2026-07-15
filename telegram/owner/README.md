# telegram/owner/

## Purpose
Phase 59.3 foundation (TASK 5: Owner Command Foundation). Real,
tested, standalone service-shaped functions for the five owner-only
commands `docs/OWNER_COMMANDS.md` already specifies as a contract
(`/provider`, `/providers`, `/provider_status`, `/enable_provider`,
`/disable_provider`) plus `/system_health`/`/features`.

**Not wired into the live bot.** These functions are NOT registered
into `telegram/commands.py`'s `OWNER_COMMANDS`/`ADMIN_COMMANDS` dicts,
and NOT called from `telegram/command_router.py` or
`telegram/handlers.py`. The running Telegram bot's actual command
surface is completely unaffected by this package existing — a future,
separately-approved phase would add the actual command registration,
permission wiring (via the pre-existing `telegram/permissions.py`/
`telegram/command_router.py` pattern), and a handler that calls these
functions and sends the result.

## Modules

### `provider_commands.py`
`list_providers()`, `get_data_status()` — real, working, backed by
`data/providers/registry.py`/`monitoring/provider_health.py`.
`enable_provider()`/`disable_provider()` — honestly **not** working
toggles: `config.Config.ENABLE_MT5`/`ENABLE_TWELVEDATA` are read once
at `config.py` import time from `os.getenv()`, so there is no runtime
mechanism to flip them yet. Both return `success=False` with a clear
reason rather than silently no-op'ing or lying about success.

### `system_commands.py`
`get_system_health()` — combines the pre-existing
`telegram.admin_service.AdminService.get_system_status()` (reused, not
duplicated) with the new per-provider health report. Distinct from the
existing, already-live `/system` command (still just `AdminService`'s
simpler view) — a superset, not a replacement.
`count_online_providers()` — a small convenience count.

### `feature_commands.py`
`list_features()` — the first place `configuration/feature_flags.py`'s
`FeatureFlags` (Phase A13) and `config.py`'s `ENABLE_MT5`/
`ENABLE_TWELVEDATA` (Phase 59.1) are read together. Reports only —
changes neither flag system.

### `report_commands.py` (Phase 59.4, TASK 5)
`format_daily_stats(signals, performances)` — the future `/stats`
command's payload (Signals/Approved/TP/SL/Expired/Cancelled/Best
Strategy), reusing `analytics/strategy_report.py`'s
`build_strategy_report()` rather than reimplementing the counting.
`pick_best_strategy(reports, minimum_signals=1)` — highest `win_rate`,
ties broken by more `total_signals`. Both take already-computed data
as input (`List[SignalSchema]`/`List[SignalPerformance]`) — nothing in
this codebase persists a day's worth of these anywhere yet (see
`docs/PHASE59_VALIDATION.md`'s "Known gaps"), so a real `/stats`
command needs that data source wired up first, a separate future step.

### `validation_commands.py` (Phase 59 Real Market Validation
Foundation, TASK 8)
`get_validation_status()` — reports `config.Config.VALIDATION_MODE`'s
current value (Phase 59 Real Market Validation Foundation, TASK 1).
`get_today_signals(signals)` — total/BUY/SELL counts; `signals` must
already be filtered to "today" by the caller, same posture as
`report_commands.format_daily_stats()`. `get_validation_report(signals,
performances, period_start, period_end)` — wraps
`analytics.validation_report.build_validation_report()`/
`format_validation_report()` (same phase, TASK 5) in a
`ProviderCommandResult`, unmodified otherwise.

### `dataset_commands.py` (Phase 59.5: Historical Data Collection &
Validation Foundation, TASK 7)
`get_dataset_status(symbol, timeframe)` — every stored candle for that
key across all providers, summarized via
`analytics.dataset_report.build_dataset_report()`/`format_dataset_report()`
(same phase, TASK 5). `get_history_status(symbol, timeframe)` — a
lighter-weight candle count + oldest/newest timestamp view.
`get_sync_status(provider, symbol, timeframe)` — the current
incremental-sync watermark, via `SyncStateRepository` (same phase,
TASK 2). `get_provider_compare(symbol, timeframe, provider_a,
provider_b)` — a summary of
`data.provider_comparison.compare_providers()` (same phase, TASK 6)
run against each provider's own stored candles. Unlike
`report_commands.py`/`validation_commands.py`, these four call the
real `RawCandleRepository`/`SyncStateRepository` directly rather than
taking caller-supplied data — `raw_candles`/`sync_state` are real,
persisted tables (Phase 59.3/Phase 59.5), the same "query the real
backing store" posture `provider_commands.py`'s
`list_providers()`/`get_data_status()` already uses.

### `owner_roles.py` (Phase 59.6: Audit & Observability Foundation,
TASK 3)
`OwnerRole` (`OWNER`/`SUPER_ADMIN`/`ADMIN`/`VIEWER`) +
`resolve_owner_role(telegram_id, admin_repository=None)`. A separate,
finer-grained, **not-yet-wired** hierarchy for a future Owner
Dashboard — never imports or modifies `telegram.permissions.PermissionLevel`
(the live enum gating real commands today via
`telegram/command_router.py`). See `docs/OWNER_PERMISSIONS.md` for the
full contrast between the two.

### `status_commands.py` (Phase 59.8: Owner Control Center)
`get_system_status()` — the future `/system_status` command's payload
(`System`/`Pipeline`/`Database`/`Provider`/`Mode`/`Last Signal`),
composing `telegram.admin_service.AdminService.get_system_status()`,
`data.providers.registry.build_default_registry()`,
`config.Config.MARKET_DATA_PROVIDER`/`VALIDATION_MODE`,
`core.system_state.SystemState` (used only as a display label — no
`SystemState` instance is held or mutated anywhere), and
`database.signal_repository.SignalRepository.get_latest_signal()`. No
new health-check logic — every sub-check is an already-existing,
already-tested call.

### `control_commands.py` (Phase 59.8: Owner Control Center)
`get_feature_states()`, `enable_feature()`, `disable_feature()` — thin
wrappers over `configuration/runtime_api.py` (Phase 59.7), reformatted
into this package's `ProviderCommandResult` shape and the `NAME
ON/OFF` text a future `/features` command needs. Deliberately named
`get_feature_states()`, not `list_features()` — `feature_commands.py`
(Phase 59.3) already has a `list_features()` reporting the older,
static `Config`/`FeatureFlags` view; this is the newer, Phase 59.7
*runtime* view, not a same-named competing implementation.

### `security.py` (Phase 59.8: Owner Control Center)
`require_role(telegram_id, minimum_role)` — ranks the caller's
`owner_roles.OwnerRole` against a minimum (`VIEWER` < `ADMIN` <
`SUPER_ADMIN` < `OWNER`), returning a `SecurityCheckResult`.
`log_owner_action()` — a convenience call-through to
`AuditLogRepository.log_action()`. Foundation only: no command in this
package calls `require_role()` to actually gate itself yet.

### `dashboard.py` (Phase 59.8: Owner Control Center)
`get_dashboard()` — the future `/dashboard` command's payload, one
consolidated overview composing `status_commands.get_system_status()`
+ `control_commands.get_feature_states()` (rendered as an "N/M ON"
count) + `provider_commands.list_providers()`. No new status/health/
provider logic — pure composition of this package's own existing
functions.

`report_commands.py` also gained `get_validation_summary(signals,
performances, period_start, period_end)` in this phase — the future
`/validation_report` command's payload (`Signals`/`Win`/`Loss`/
`Accuracy`/`Best Strategy`), reusing `build_strategy_report()`/
`pick_best_strategy()` (both already in this file) and
`analytics.strategy_report.compute_win_rate()` for `Accuracy` — the
same win-rate formula every other figure in this codebase already
uses.

### `emergency_commands.py` (Phase 59.9: Emergency Safety Layer
Foundation)
`kill_system()`, `pause_system()`, `maintenance_on()`,
`restore_system()`, `get_emergency_status()` — thin wrappers over
`core.emergency.emergency_manager.EmergencyManager`, reformatted into
this package's `ProviderCommandResult` shape. No new
state/persistence/audit logic — every transition is validated,
persisted, and audited entirely inside `core/emergency/`. See
`docs/EMERGENCY_SYSTEM.md` for the full state diagram and safety
rules. Not wired into the live bot, same as every module in this
package.

### `replay_commands.py` (Phase 60.1: Historical Replay Engine)
`replay_start()`, `replay_pause()`, `replay_stop()`, `replay_status()`
— thin wrappers over `backtesting.replay_controller.ReplayController`,
reformatted into this package's `ProviderCommandResult` shape (via
`backtesting.replay_models.format_replay_report()`). No new
session/engine logic — one module-level default `ReplayController`
holds every session in-memory for this process's lifetime. See
`docs/REPLAY_ENGINE.md` for the full architecture and state diagram.
Not wired into the live bot, same as every module in this package.

## Dependencies
`provider_commands.py` imports `data.providers.registry`,
`monitoring.provider_health`. `system_commands.py` additionally
imports `telegram.admin_service.AdminService` and
`provider_commands.ProviderCommandResult`. `feature_commands.py`
imports `config.Config`, `configuration.feature_flags.DEFAULT_FLAGS`,
and `provider_commands.ProviderCommandResult`. `report_commands.py`
imports `analytics.strategy_report`, `analytics.signal_performance`,
`signals.schema.SignalSchema`, and `provider_commands.ProviderCommandResult`.
`validation_commands.py` imports `analytics.validation_report`,
`analytics.signal_performance`, `config.Config`, `signals.schema.SignalSchema`,
and `provider_commands.ProviderCommandResult`. `dataset_commands.py`
imports `analytics.dataset_report`, `data.provider_comparison`,
`database.raw_candle_repository`, `database.sync_state_repository`,
and `provider_commands.ProviderCommandResult`. `owner_roles.py`
imports `telegram.permissions.is_owner` and, lazily (inside
`resolve_owner_role()`, not at module import time),
`database.admin_repository.AdminRepository`. `status_commands.py`
imports `config.Config`, `core.system_state.SystemState`,
`data.providers.registry`, `database.signal_repository.SignalRepository`,
`telegram.admin_service.AdminService`, and
`provider_commands.ProviderCommandResult`. `control_commands.py`
imports `configuration.runtime_api` and
`provider_commands.ProviderCommandResult` — the same one-directional
`telegram/` → `configuration/` dependency `runtime_api.py` itself
documents, never reversed. `security.py` imports
`database.audit_log_repository`/`audit_log_models` and
`owner_roles.OwnerRole`/`resolve_owner_role`. `dashboard.py` imports
only other modules within this package
(`control_commands`/`provider_commands`/`status_commands`).
`emergency_commands.py` imports `core.emergency.emergency_manager.EmergencyManager`,
`core.emergency.emergency_state.EmergencyStateRecord`, and
`provider_commands.ProviderCommandResult`. `replay_commands.py`
imports `backtesting.replay_controller.ReplayController`,
`backtesting.replay_models.ReplayConfig`/`format_replay_report()`, and
`provider_commands.ProviderCommandResult`.
None imports `telegram.handlers`, `telegram.command_router`, or
`telegram.commands` — this package is never itself imported by the
live routing surface.

## Future Roadmap
See `docs/OWNER_COMMANDS.md`'s own "Roadmap" section — command
registration, permission wiring, an actual handler, and a runtime
config-override mechanism (for `enable_provider()`/`disable_provider()`
to become real) all remain unimplemented.
