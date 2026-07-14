# Owner Commands — Contract (Phase 59.2, TASK 7)

**Not implemented in this phase.** No Telegram handler, service, or
repository exists for any command below — this document fixes the
contract in advance, per the Director's own prior agreement ("Oldingi
kelishuv bo'yicha: Owner uchun alohida. Hozir faqat contract."), the
same posture Phase 59.1's TASK 6 (Owner Mode) established. That
section, previously inside `docs/MARKET_PROVIDER.md`, now lives here
as the single source of truth — `docs/MARKET_PROVIDER.md` points to
this document instead of duplicating it.

## Commands

```
/provider                → shows the current MARKET_DATA_PROVIDER and every registered provider's ProviderStatus
/providers                → lists every provider in the default registry (data/providers/registry.py's build_default_registry()), by name, with availability
/provider_status          → a full monitoring/provider_health.py report for every registered provider (status, latency, reason) -- the Telegram-facing view of check_registry_health()
/enable_provider <name>   → sets ENABLE_<NAME>=True (owner-only)
/disable_provider <name>  → sets ENABLE_<NAME>=False (owner-only)
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
  — no new exception to that rule. The exact owner-role check (which
  repository, which column) is not audited in this phase — that audit
  belongs to whoever implements the command, at implementation time.
- **`/provider`/`/providers`** should call
  `data/providers/registry.py`'s `build_default_registry()` (or an
  injected registry) and `ProviderRegistry.all_names()`/`available()`
  — not reimplement provider enumeration.
- **`/provider_status`** should call
  `monitoring/provider_health.py`'s `check_registry_health()` and
  format its `List[ProviderHealthReport]` for Telegram — not
  reimplement latency measurement or status classification.
- **`/enable_provider`/`/disable_provider`** should validate the
  target name against `data/providers/get_provider()`'s own known
  provider set and surface its exact `ValueError` message back to the
  owner (e.g. "MARKET_DATA_PROVIDER=mt5 requires ENABLE_MT5=True") —
  not a new, separate validation.
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

## What this phase does NOT do

- Does not add any Telegram command, handler, service, or repository
  code.
- Does not change `telegram/handlers.py`, `telegram/polling.py`, or
  any `telegram/*_service.py` file.
- Does not implement a runtime config-override mechanism.

## Roadmap

```
docs/OWNER_COMMANDS.md (this document -- contract only)
        |
        v
A future, separately-approved phase:
  - telegram/provider_service.py (new)
  - telegram/handlers.py: five new owner-only command routes
  - a runtime override mechanism for MARKET_DATA_PROVIDER/ENABLE_*
```
