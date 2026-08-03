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

## Phase 59.8 update — Owner Control Center

Still not wired into the live bot — every rule above still holds. Five
new/extended commands' worth of payload now exist, per the Director's
own "Owner Control Center" brief:

```
/system_status     → telegram/owner/status_commands.py's get_system_status()
/features           → telegram/owner/control_commands.py's get_feature_states() -- NOTE: a different function from feature_commands.py's own list_features() (see below)
/dashboard          → telegram/owner/dashboard.py's get_dashboard() -- one consolidated overview
/validation_report  → telegram/owner/report_commands.py's get_validation_summary(signals, performances, period_start, period_end)
/feature enable|disable <name>  → telegram/owner/control_commands.py's enable_feature()/disable_feature()
```

**`/features` now has two different real implementations in this
package**, disclosed explicitly to avoid confusion:
`feature_commands.list_features()` (Phase 59.3) reports the *static*
`config.Config`/`configuration.feature_flags.FeatureFlags` view (what
each flag's process-start value is). `control_commands.get_feature_states()`
(Phase 59.8) reports the *runtime* view via
`configuration/runtime_feature_manager.py` (Phase 59.7) — what an
owner has actually toggled, validated/persisted/audited/snapshotted,
surviving a restart. A future wiring step must pick exactly one of
these two for the live `/features` command (the Director's own worked
example — `ENABLE_AI ON` / `ENABLE_MT5 OFF` — matches
`get_feature_states()`'s output shape, not `list_features()`'s).

**The `/enable_provider`/`/disable_provider` gap above is still not
closed** — `Config.ENABLE_MT5`/`ENABLE_TWELVEDATA` themselves remain
os.getenv-read-once constants; Phase 59.7's runtime override is a
*separate* tracked value (`configuration/runtime_feature_manager.py`'s
own `"ENABLE_MT5"` registry entry), not a mutation of `Config.ENABLE_MT5`
itself. `provider_commands.py`'s `enable_provider()`/`disable_provider()`
still honestly report `success=False`, unchanged by this phase. A
future implementer wiring live provider control would use
`control_commands.enable_feature("ENABLE_MT5")`/`disable_feature()`
(the real, working runtime toggle) rather than trying to make
`provider_commands.py`'s own stubs work.

**Owner Control Center's own foundation-only pieces**:
`telegram/owner/security.py`'s `require_role()` (ranks the Phase 59.6
`OwnerRole` hierarchy against a minimum) and `log_owner_action()` (a
convenience `AuditLogRepository.log_action()` call-through) exist but
are not called by any command in this package yet — the actual
per-command minimum-role gate is part of the same future wiring step
below.

## Phase 59.9 update — Emergency Safety Layer

Still not wired into the live bot — every rule above still holds. Five
new emergency commands' worth of payload now exist:

```
/panic (kill)       → telegram/owner/emergency_commands.py's kill_system()
/pause               → telegram/owner/emergency_commands.py's pause_system()
/maintenance on      → telegram/owner/emergency_commands.py's maintenance_on()
/restore             → telegram/owner/emergency_commands.py's restore_system()
/emergency_status     → telegram/owner/emergency_commands.py's get_emergency_status()
```

Each is a thin wrapper over `core_layer.emergency.emergency_manager.EmergencyManager`
(Phase 59.9) — every call is persisted (append-only history, never
overwritten) and audited (`KILL_ACTIVATED`/`PAUSE_ACTIVATED`/
`MAINTENANCE_ENABLED`/`SYSTEM_RESTORED`). See `docs/EMERGENCY_SYSTEM.md`
for the full state diagram, safety rules, and future wiring plan
(including how this would eventually gate `core/pipeline.py`/
`execution/` — not done in this phase).

## Roadmap

```
docs/OWNER_COMMANDS.md (Phase 59.2 -- contract)
        |
        v
telegram/owner/*.py (Phase 59.3-59.8 -- real logic, not wired)
        |
        v
A future, separately-approved phase:
  - telegram/commands.py: new command entries (including the five above)
  - telegram/command_router.py: routing for the new commands, using
    telegram/owner/security.py's require_role() for the per-command
    minimum-OwnerRole gate
  - telegram/handlers.py: new owner-only handler functions calling
    telegram/owner/*.py, each logging via security.py's log_owner_action()
  - a decision on /features: get_feature_states() (runtime) vs
    list_features() (static) -- not both, to avoid two different
    answers to the same command
  - a runtime override mechanism for MARKET_DATA_PROVIDER/ENABLE_* at
    the config.Config level itself (still needed for
    enable_provider()/disable_provider() specifically to become real;
    Phase 59.7's runtime registry is a parallel tracked value, not a
    fix for this specific gap)
```
