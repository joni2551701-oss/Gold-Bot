# Owner Commands — Contract (Phase 59.2, TASK 7; partially implemented Phase 59.3 TASK 5 / 59.4 TASK 5)

**Still not wired into the live bot.** Phase 59.2 kept this
documentation-only, per the Director's prior agreement ("Oldingi
kelishuv bo'yicha: Owner uchun alohida. Hozir faqat contract."). Phase
59.3 and 59.4 both asked for real code
(`telegram/owner/provider_commands.py`/`system_commands.py`/
`feature_commands.py`/`report_commands.py`) — those now exist as real,
tested, **standalone** functions (`list_providers()`,
`get_data_status()`, `get_system_health()`, `list_features()`,
`format_daily_stats()`, plus honestly-non-working
`enable_provider()`/`disable_provider()` stubs — see
`telegram/owner/README.md`), but are **not** registered into
`telegram/commands.py`'s `OWNER_COMMANDS`/`ADMIN_COMMANDS` dicts, and
**not** called from `telegram/command_router.py` or
`telegram/handlers.py`. The running bot's actual command surface is
unaffected. The contract below is now partially satisfied by real
code, not yet by a live command.

## Commands

```
/provider                → shows the current MARKET_DATA_PROVIDER and every registered provider's ProviderStatus
/providers                → lists every provider in the default registry (data/providers/registry.py's build_default_registry()), by name, with availability
/provider_status          → a full monitoring/provider_health.py report for every registered provider (status, latency, reason) -- the Telegram-facing view of check_registry_health()
/enable_provider <name>   → sets ENABLE_<NAME>=True (owner-only)
/disable_provider <name>  → sets ENABLE_<NAME>=False (owner-only)
/system_health             → telegram/owner/system_commands.py's get_system_health()
/features                  → telegram/owner/feature_commands.py's list_features()
/stats                     → telegram/owner/report_commands.py's format_daily_stats() (Phase 59.4) -- needs a real data source (today's SignalSchema/SignalPerformance records) wired up first; nothing persists these yet, see "Contract" below
```

`/provider <name>` (Phase 59.1's original two-argument form, e.g.
`/provider twelvedata`, `/provider mt5`) is superseded by the four
commands above, which separate "show me state" (`/provider`,
`/providers`, `/provider_status`) from "change state"
(`/enable_provider`/`/disable_provider`) — a clearer split than one
overloaded command, though nothing about routing/permissions differs
between the two shapes.

## Contract, for whoever implements this later

- **Owner-only**, every command. Must go through
  `telegram/*_service.py` → a repository, per this codebase's own
  handler/service/repository rule (`telegram/handlers.py` never calls
  `database/*` directly, stated in that file's own module docstring)
  — no new exception to that rule. `telegram/owner/` (Phase 59.3) is
  intentionally NOT itself a `*_service.py`-registered service yet —
  it holds the real logic, but the actual handler → permission check →
  send-result wiring is still the next step. The exact owner-role
  check (which repository, which column) is not audited in this phase
  — that audit belongs to whoever wires the command, at wiring time.
- **`/provider`/`/providers`** — `telegram/owner/provider_commands.py`'s
  `list_providers()` already calls `data/providers/registry.py`'s
  `build_default_registry()` and `ProviderRegistry.all_names()`/
  `available()` — done, just needs a handler to call it.
- **`/provider_status`** — `provider_commands.py`'s `get_data_status()`
  already calls `monitoring/provider_health.py`'s
  `check_registry_health()` — done, just needs a handler.
- **`/system_health`** — `telegram/owner/system_commands.py`'s
  `get_system_health()` already combines
  `telegram.admin_service.AdminService.get_system_status()` with
  `check_registry_health()` — done, just needs a handler.
- **`/features`** — `telegram/owner/feature_commands.py`'s
  `list_features()` already reads both
  `configuration/feature_flags.py`'s `FeatureFlags` and
  `config.py`'s `ENABLE_MT5`/`ENABLE_TWELVEDATA` — done, just needs a
  handler.
- **`/enable_provider`/`/disable_provider`** — `provider_commands.py`'s
  `enable_provider()`/`disable_provider()` exist but honestly return
  `success=False` today (see next bullet) — a future implementer
  building the runtime-override mechanism below would update these two
  functions themselves, not just add a handler on top.
- **`/stats`** (Phase 59.4) — `telegram/owner/report_commands.py`'s
  `format_daily_stats(signals, performances)` already does the
  Signals/Approved/TP/SL/Expired/Cancelled/Best-Strategy formatting,
  reusing `analytics/strategy_report.py` — but needs a real *data
  source* wired up first, not just a handler: nothing in this codebase
  persists a day's worth of `SignalSchema`/`SignalPerformance` records
  anywhere yet. A future implementer would need to decide where
  "today's signals" comes from (a new query over
  `database/raw_candle_repository.py`-adjacent persistence, or a fresh
  in-memory accumulator process-lifetime-scoped) before a handler can
  call this function meaningfully.
- **Does not change `MARKET_DATA_PROVIDER`/`ENABLE_*` at the process
  level** the way `config.py` reads them today: `os.getenv()` is read
  once, at `config.py` import time. A real implementation needs either
  a process restart, or a runtime-override mechanism (e.g. a
  `configuration/` — Phase A13 — settings override, or a small
  in-memory/database-backed override table) this phase does not
  design. Until that exists, `/enable_provider`/`/disable_provider`
  can only be a *contract*, not a working toggle — flagged explicitly
  so a future implementer doesn't assume `os.environ` mutation alone
  is sufficient (it would not affect a value `config.py` already read
  at import time).

## What Phase 59.3/59.4 do NOT do

- Does not register any command into `telegram/commands.py`'s
  `OWNER_COMMANDS`/`ADMIN_COMMANDS` dicts.
- Does not change `telegram/handlers.py`, `telegram/polling.py`,
  `telegram/command_router.py`, or any pre-existing
  `telegram/*_service.py` file.
- Does not implement a runtime config-override mechanism —
  `enable_provider()`/`disable_provider()` (`telegram/owner/provider_commands.py`)
  honestly report `success=False` rather than pretending to work.
- Does not persist a day's worth of signals/performance anywhere —
  `format_daily_stats()` (Phase 59.4) takes already-computed data as
  input; no accumulator or query exists yet.

## Roadmap

```
docs/OWNER_COMMANDS.md (Phase 59.2 -- contract)
        |
        v
telegram/owner/*.py (Phase 59.3 -- real logic, not wired)
        |
        v
A future, separately-approved phase:
  - telegram/commands.py: five new command entries
  - telegram/command_router.py: routing for the five new commands
  - telegram/handlers.py: five new owner-only handler functions calling telegram/owner/*.py
  - a runtime override mechanism for MARKET_DATA_PROVIDER/ENABLE_*
    (needed for enable_provider()/disable_provider() to become real)
```
