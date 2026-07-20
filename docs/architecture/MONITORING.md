# GoldBot — Core Owner Monitoring (Alpha)

Governed by `docs/constitution/CONSTITUTION.md`. This document describes
`monitoring/`'s Owner-only observation layer, built in the "GoldBot Core
Owner Monitoring Alpha" phase (a V1 pre-production observation phase,
not part of the `66.x` AI Trading Intelligence sub-sequence). Full
Foundation Reuse Audit: `docs/PHASE_CORE_MONITORING_AUDIT.md`. Full
freeze: `docs/PHASE_CORE_MONITORING_FREEZE.md`.

## Why this phase exists

GoldBot has not shipped V1 yet. The current goal is observing real
behavior, finding bugs, and collecting data — not serving public
users. This phase adds an Owner-only monitoring layer that watches
GoldBot Core without ever participating in it.

```
GoldBot Core
      |
      v
Monitoring Layer
      |
      v
Owner Telegram Panel
```

## What is monitored

| Area | Model | Module | Command |
|------|-------|--------|---------|
| System health | `monitoring.models.SystemHealth` | `monitoring/system_monitor.py` | `/owner_status` |
| Full diagnostics | (reuses `AdminService` + provider registry) | `telegram/owner/system_commands.py` (existing, now wired) | `/health` |
| Market data | `monitoring.models.MarketHealth` | `monitoring/market_monitor.py` | `/market` |
| Signal activity | `monitoring.models.SignalHealth` | `monitoring/signal_monitor.py` | `/signals` |
| Errors | `monitoring.models.ErrorEvent` | `monitoring/error_monitor.py` | `/errors` |
| Decision pipeline trace | `monitoring.models.DecisionPipelineEntry` | `monitoring/decision_logger.py` | `/pipeline` |
| Daily digest | (composes the above) | `telegram/owner/monitoring_commands.py` | `/report` |

## What is *not* monitored (or not yet)

- **`SignalHealth.none_count`** is only ever non-zero for rows the
  Trading Core itself persisted with a non-BUY/SELL `direction`
  (REJECT/NO_TRADE candidates, when `persist_signals=True`). This
  module has no hook into `core/pipeline.py` to count evaluation
  cycles that produced *no* candidate at all — adding one would
  require modifying `core/pipeline.py`, forbidden this phase (Strict
  Rule).
- **`MarketHealth.last_price`/`.last_update`** are `Optional`,
  populated only when a caller supplies them — `data/providers/` has
  no "last candle received" or price-freshness concept anywhere today
  (confirmed by the audit). Never fabricated.
- **`SystemHealth.last_scan`** is populated only via
  `monitoring.system_monitor.record_scan()`, a passive sink. Nothing
  currently calls it (no `core/pipeline.py` hook this phase) — it
  reads "N/A" until a future, separately-approved integration calls it.

## Why `/status` is not the command name

The brief's own worked example names the System Health command
`/status`. `/status` is already a live, public, USER-level command
(`telegram/handlers.py`'s `status_handler`, "GoldBot is running.",
registered in `telegram.commands.COMMANDS`). Command names are never
renamed or reused (Article 9). The Owner-only richer version is named
`/owner_status` instead — see `telegram/handlers.py`'s
`owner_status_handler` docstring for the same note in code.

## Architecture

```
monitoring/
  models.py            SystemHealth/MarketHealth/SignalHealth/ErrorEvent/
                        ErrorSeverity/DecisionPipelineEntry -- primitive-only
  system_monitor.py     SystemMonitor -- in-memory uptime/last_scan/last_error,
                         composes AdminService + provider registry health
  market_monitor.py     get_market_health() -- composes monitoring.provider_health
  signal_monitor.py      (extended) get_signal_health() -- aggregates
                          SignalRepository.get_signals_today()
  decision_logger.py     DecisionLogger -- persists a primitive per-criterion
                          trace via MonitoringRepository
  error_monitor.py       ErrorMonitor -- persists ErrorEvent via
                          MonitoringRepository, updates SystemMonitor.last_error

database/
  monitoring_models.py    ErrorEventEntry / DecisionPipelineEntryRow
  monitoring_repository.py MonitoringRepository -- append-only, two tables
                            (monitoring_error_events, monitoring_decision_pipeline)

telegram/owner/
  monitoring_commands.py  get_status_report()/get_health_report()/
                          get_market_report()/get_signals_report()/
                          get_errors_report()/get_pipeline_report()/
                          get_daily_report()
```

`SystemHealth`/`MarketHealth`/`SignalHealth` are **computed live, on
demand** — no new table for any of the three (matching the existing
`AdminService.get_system_status()`/`telegram.owner.system_commands.get_system_health()`/
`monitoring.performance.PerformanceTracker.calculate()` precedent).
Only `ErrorEvent` and `DecisionPipelineEntry` are persisted, because
both need to survive a process restart (an error history, and the
future `66.5`/`66.6` Performance/Strategy Intelligence datasource).

## Dependency rules

Monitoring never imports `decision/`, `risk/`, or `execution/`
(enforced by `tests/monitoring/test_monitoring_isolation.py`, AST-based).
`monitoring/decision_logger.py` additionally never imports
`signals/`/`context/` — it accepts primitive `criteria_met`/
`criteria_total`/`decision`/`reason` values only, the same
"primitive contract, no upstream object import" discipline this
codebase's `ai/*/models.py` Foundation contracts already established.
Monitoring never mutates Trading Core state — every function here
either reads an already-existing source or writes to its own two new
tables.

## Security

Gated by the existing, live mechanism: `telegram.permissions.is_owner()`
(env var `TELEGRAM_OWNER_ID`, singular) + `telegram.command_router`'s
rank-based gate + `telegram.commands.OWNER_COMMANDS` registration —
the same mechanism every other Owner-only command (`/owner`, `/doctor`,
`/runtime`, etc.) already uses. No new `access_control.py` was
created; `telegram/owner/security.py`'s own `OwnerRole`/`require_role()`
foundation (a separate, four-tier hierarchy, not enforced anywhere)
was reviewed but is out of scope — this phase's own brief says "Hozir:
faqat OWNER ishlaydi" (only OWNER works for now), which the live gate
already satisfies exactly.

## Future extension

- `SignalHealth.none_count`, `MarketHealth.last_price`/`.last_update`,
  and `SystemHealth.last_scan` all need a future, separately-approved
  `core/pipeline.py` hook to become real — not built this phase.
- `monitoring.decision_logger.DecisionLogger` is this phase's own
  named datasource for `66.5` (Performance Intelligence) and `66.6`
  (Strategy Intelligence) — a future AI phase reads from
  `MonitoringRepository.get_recent_decision_entries()`, type-only,
  the same "read type-only, never import the class" pattern the AI
  Layer's own `ai/coaching/journal_adapter.py` (Phase 66.4) already
  established for a comparable boundary.
- `telegram/owner/security.py`'s dormant `OwnerRole` (OWNER/
  SUPER_ADMIN/ADMIN/VIEWER) remains available for a future phase that
  needs finer-grained Owner-panel roles.

## Related documents

- `docs/PHASE_CORE_MONITORING_AUDIT.md` — TASK 0's Foundation Reuse
  Audit.
- `docs/PHASE_CORE_MONITORING_FREEZE.md` — this phase's own freeze.
- `docs/owner/OWNER_PANEL.md` — the wider Owner Telegram panel this
  phase's commands are added to.
