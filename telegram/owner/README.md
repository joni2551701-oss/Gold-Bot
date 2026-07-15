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
and `provider_commands.ProviderCommandResult`.
None imports `telegram.handlers`, `telegram.command_router`, or
`telegram.commands` — this package is never itself imported by the
live routing surface.

## Future Roadmap
See `docs/OWNER_COMMANDS.md`'s own "Roadmap" section — command
registration, permission wiring, an actual handler, and a runtime
config-override mechanism (for `enable_provider()`/`disable_provider()`
to become real) all remain unimplemented.
