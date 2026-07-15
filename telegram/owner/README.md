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

## Dependencies
`provider_commands.py` imports `data.providers.registry`,
`monitoring.provider_health`. `system_commands.py` additionally
imports `telegram.admin_service.AdminService` and
`provider_commands.ProviderCommandResult`. `feature_commands.py`
imports `config.Config`, `configuration.feature_flags.DEFAULT_FLAGS`,
and `provider_commands.ProviderCommandResult`. None imports
`telegram.handlers`, `telegram.command_router`, or `telegram.commands`
— this package is never itself imported by the live routing surface.

## Future Roadmap
See `docs/OWNER_COMMANDS.md`'s own "Roadmap" section — command
registration, permission wiring, an actual handler, and a runtime
config-override mechanism (for `enable_provider()`/`disable_provider()`
to become real) all remain unimplemented.
