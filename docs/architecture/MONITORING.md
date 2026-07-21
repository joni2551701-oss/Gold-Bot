# GoldBot — Core Owner Monitoring (Alpha)

Governed by `docs/constitution/CONSTITUTION.md`. This document describes
`monitoring/`'s Owner-only observation layer, built in the "GoldBot Core
Owner Monitoring Alpha" phase (a V1 pre-production observation phase,
not part of the `66.x` AI Trading Intelligence sub-sequence). Full
Foundation Reuse Audit: `docs/PHASE_CORE_MONITORING_AUDIT.md`. Full
freeze: `docs/PHASE_CORE_MONITORING_FREEZE.md`.

**Phase B.0 addendum**: a second, identically-named Worker Brief
("GoldBot Core Owner Monitoring Alpha Foundation") arrived after this
phase had already shipped. `docs/PHASE_B0_AUDIT.md` found ~90% overlap
with the content already documented on this page and extended the
existing modules in place rather than creating a duplicate
`monitoring/owner/` package — see `docs/PHASE_B0_FREEZE.md` for the six
genuine gaps that were filled (system resource metrics,
OK/WARNING/CRITICAL classification, a pure performance counter, per-
pipeline-stage timing, `enable_owner_monitoring`, and a `/performance`
command). This page's own "Architecture"/"What is monitored" sections
below are updated in place to reflect the current, combined state.

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
| Decision pipeline trace | `monitoring.models.DecisionPipelineEntry` (+ Phase B.0's own `stage_durations_ms`) | `monitoring/decision_logger.py` | `/pipeline` |
| Daily digest | (composes the above) | `telegram/owner/monitoring_commands.py` | `/report` |
| Resource metrics (CPU/RAM/threads/restarts/heartbeat) | `monitoring.models.ResourceSnapshot` | `monitoring/resource_monitor.py` (Phase B.0) | appended to `/owner_status` |
| Overall health classification (OK/WARNING/CRITICAL) | `monitoring.models.HealthStatus` | `monitoring/health_monitor.py` (Phase B.0) | appended to `/owner_status` |
| Performance counters (raw tallies, never computed) | `monitoring.models.PerformanceCounters` | `monitoring/performance_collector.py` (Phase B.0) | `/performance` |

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
                        ErrorSeverity/DecisionPipelineEntry/HealthStatus/
                        ResourceSnapshot/PerformanceCounters -- primitive-only
  system_monitor.py     SystemMonitor -- in-memory uptime/last_scan/last_error,
                         composes AdminService + provider registry health
  market_monitor.py     get_market_health() -- composes monitoring.provider_health
  signal_monitor.py      (extended) get_signal_health() -- aggregates
                          SignalRepository.get_signals_today()
  decision_logger.py     DecisionLogger -- persists a primitive per-criterion
                          trace (+ Phase B.0's own stage_durations_ms) via
                          MonitoringRepository
  error_monitor.py       ErrorMonitor -- persists ErrorEvent via
                          MonitoringRepository, updates SystemMonitor.last_error
  resource_monitor.py    (Phase B.0) get_resource_snapshot()/record_process_start()
                          -- CPU/RAM/thread/restart/heartbeat, stdlib only
  health_monitor.py      (Phase B.0) classify_health() -- pure OK/WARNING/CRITICAL
                          classifier over already-known SystemHealth/error counts
  performance_collector.py (Phase B.0) PerformanceCollector -- in-memory
                          raw counters (signal/decision/trade/reject/error/
                          reconnect), never computed
  access.py              (Phase B.0) is_owner_monitoring_enabled() -- gates
                          this phase's own new surface only

database/
  monitoring_models.py    ErrorEventEntry / DecisionPipelineEntryRow (+ Phase
                           B.0's own stage_durations_ms field) / ProcessStartEntry
  monitoring_repository.py MonitoringRepository -- append-only, three tables
                            (monitoring_error_events, monitoring_decision_pipeline,
                            monitoring_process_starts)

telegram/owner/
  monitoring_commands.py  get_status_report() (+ Phase B.0's own appended
                          resource/health lines when enable_owner_monitoring is
                          on)/get_health_report()/get_market_report()/
                          get_signals_report()/get_errors_report()/
                          get_pipeline_report()/get_daily_report()/
                          get_performance_report() (Phase B.0, new command)
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
either reads an already-existing source or writes to its own tables.
Phase B.0's own new files (`resource_monitor.py`, `health_monitor.py`,
`performance_collector.py`, `access.py`) are confirmed isolated the
same way by `tests/monitoring/test_phase_b0_isolation.py`; `access.py`
imports only `configuration.feature_flags`, `health_monitor.py` and
`performance_collector.py` import no database of any kind (in-memory/
pure-function only).

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

## Owner Snapshot Reporter (GitHub Actions Alpha, v1.1)

`monitoring/snapshot_collector.py` (GoldBot Core Owner Snapshot
Reporter Alpha) composes `get_health()`/`get_market_health()`/
`get_signal_health()`/`ErrorMonitor`/`SignalRepository.get_signals_today()`/
`MonitoringRepository` from this layer into a single `OwnerSnapshot`,
delivered to the Owner's Telegram every 15 minutes by
`.github/workflows/owner_snapshot.yml` (`timeout-minutes: 5`) — a
one-shot substitute for this phase's own live commands until
`telegram.polling` is deployed on a VPS. v1.1 (Operational
Intelligence Upgrade) extended the snapshot with Pipeline/Signal/
Decision/AI/Market/Error/Runtime/Database detail, all additively
sourced from data already read elsewhere in this file's own layer —
see `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md` for the full Real/Proxy/
Unavailable classification per field (e.g. `ai_status` is always
`NO_DATA`: `ai/audit/*.py` is in-memory only, invisible to a fresh
15-minute process). On a collection/formatting failure, the Owner also
receives a short "Snapshot Failed" Telegram message (best-effort,
never itself raises) instead of the failure only being visible in
GitHub Actions' own logs. See `docs/OWNER_SNAPSHOT_REPORTER.md` for
the full design and `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md`/
`docs/PHASE_OWNER_SNAPSHOT_V1_1_FREEZE.md`'s LOCK Policy for
`monitoring/snapshot_*`/`telegram/owner/snapshot_*`.

## Phase B.0 — genuine gaps only (no duplicate package)

`docs/PHASE_B0_AUDIT.md`'s own headline finding: the Phase B.0 brief
requested a new `monitoring/owner/` subpackage duplicating
`system_monitor.py`/`market_monitor.py`/`signal_monitor.py`/
`error_monitor.py`/a decision-pipeline logger under near-identical
names, plus seven Owner commands that collide with the seven already
live (`/health`, `/market`, `/signals`, `/errors`, `/status` vs.
`/owner_status`, `/decision` vs. `/pipeline`, `/runtime` — the last of
which already means "AI Runtime lifecycle," a different concern
entirely). Per the Module Reuse Principle, only six genuine gaps were
filled, all as additive extensions to the existing modules above:
system resource metrics (`resource_monitor.py`), OK/WARNING/CRITICAL
classification (`health_monitor.py`), a pure counter collector
(`performance_collector.py`), per-pipeline-stage timing
(`DecisionPipelineEntry.stage_durations_ms`), the
`enable_owner_monitoring` feature flag, and a new `/performance`
command. `OWNER_IDS` (Rule 4) was not implemented as a second,
competing owner-identity source — the existing singular
`Secrets.TELEGRAM_OWNER_ID` gate already satisfies "only OWNER can use
these commands." Full detail: `docs/PHASE_B0_AUDIT.md`,
`docs/PHASE_B0_FREEZE.md`.

## Related documents

- `docs/PHASE_CORE_MONITORING_AUDIT.md` — TASK 0's Foundation Reuse
  Audit.
- `docs/PHASE_CORE_MONITORING_FREEZE.md` — this phase's own freeze.
- `docs/PHASE_B0_AUDIT.md`, `docs/PHASE_B0_FREEZE.md` — the
  genuine-gaps-only extension phase, run after this page's own content
  had already shipped under an identically-named brief.
- `docs/owner/OWNER_PANEL.md` — the wider Owner Telegram panel this
  phase's commands are added to.
