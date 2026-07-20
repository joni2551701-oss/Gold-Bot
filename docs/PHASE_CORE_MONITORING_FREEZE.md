# GoldBot Core Owner Monitoring Alpha — Freeze

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes "GoldBot Core Owner Monitoring
Alpha" — a V1 pre-production observation phase, separate from the
`66.x` AI Trading Intelligence sub-sequence. It records what was
actually built, what remains explicitly out of scope, and the
Constitution/Dependency compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE_CORE_MONITORING_AUDIT.md`) reviewed
`monitoring/`, `telegram/owner/` (five named files in full), `core/`,
`database/`, and `signals/`/`context/`. Found and reused two real,
dormant functions outright (`telegram/owner/system_commands.py`'s
`get_system_health()` for `/health`; the live
`telegram.permissions`/`telegram.command_router` gate for security);
extended two existing files in place (`monitoring/signal_monitor.py`'s
dead placeholder, `database/signal_repository.py` with one new read
method); confirmed a genuine gap for `ErrorEvent`/`DecisionPipelineEntry`
persistence (nothing like it existed anywhere). No Director Decision
pause was required.

## Built this phase

- `monitoring/models.py` (new) — `SystemHealth`, `MarketHealth`,
  `SignalHealth`, `ErrorSeverity`, `ErrorEvent`, `DecisionPipelineEntry`
  — primitive-only.
- `monitoring/system_monitor.py` (new) — `SystemMonitor`: in-memory
  `uptime_seconds()`/`record_scan()`/`record_error()`, `get_health()`
  composing `AdminService().get_system_status()` +
  `monitoring.provider_health.check_registry_health()`. Module-level
  `DEFAULT_MONITOR` shared across a running process.
- `monitoring/market_monitor.py` (new) — `get_market_health()`,
  composing `monitoring.provider_health.check_provider_health()`;
  `last_price`/`last_update` are caller-supplied `Optional`s, never
  fabricated.
- `monitoring/signal_monitor.py` (extended) — new `get_signal_health()`
  aggregating `SignalRepository.get_signals_today()` by
  `direction`/`confidence_score`; the pre-existing dead `SignalMonitor`/
  `MonitorConfig`/`MonitorResult` placeholder is untouched.
- `monitoring/decision_logger.py` (new) — `DecisionLogger`:
  `log_entry()`/`get_recent_entries()`, primitive `criteria_met`/
  `criteria_total`/`decision`/`reason` only — never imports
  `signals.signal_quality.SignalQualityResult` directly.
- `monitoring/error_monitor.py` (new) — `ErrorMonitor`:
  `capture()`/`get_recent_errors()`/`get_error_counts()`; `capture()`
  also relays into `SystemMonitor.record_error()`.
- `database/monitoring_models.py` + `database/monitoring_repository.py`
  (new) — `ErrorEventEntry`/`DecisionPipelineEntryRow` +
  `MonitoringRepository`, two new append-only tables
  (`monitoring_error_events`, `monitoring_decision_pipeline`).
  `database/models.py` gained `init_monitoring_schema()`.
- `database/signal_repository.py` (extended) — new
  `get_signals_today()` read method (all of today's signals, any
  status; mirrors the existing `count_signals_today()`/
  `get_closed_signals_today()` pattern).
- `telegram/owner/monitoring_commands.py` (new) — `get_status_report()`,
  `get_health_report()` (reuses `system_commands.get_system_health()`),
  `get_market_report()`, `get_signals_report()`, `get_errors_report()`,
  `get_pipeline_report()`, `get_daily_report()`.
- `telegram/handlers.py` (extended) — seven new handler functions
  (`owner_status_handler`, `health_handler`, `market_handler`,
  `signals_handler`, `errors_handler`, `pipeline_handler`,
  `report_handler`), live-wired.
- `telegram/commands.py` (extended) — seven new `OWNER_COMMANDS`
  entries: `owner_status`, `health`, `market`, `signals`, `errors`,
  `pipeline`, `report`. None dual-listed in `ADMIN_COMMANDS` — Owner
  only, per the brief's own "Hozir: faqat OWNER ishlaydi."
- `docs/architecture/MONITORING.md`, `docs/PHASE_CORE_MONITORING_AUDIT.md`,
  `docs/PHASE_CORE_MONITORING_FREEZE.md` (new documentation).
- `tests/monitoring/` (7 new files) + `tests/telegram/owner/test_owner_commands.py`
  — 126 new tests, exceeding the brief's own 100-test minimum.

## Not Built this phase

- No new `telegram/access_control.py` — the existing, live
  `telegram.permissions`/`telegram.command_router` gate already
  satisfies TASK 8 exactly (see the audit's own "Security" section).
- No `OWNER_IDS` (plural) — the existing `Secrets.TELEGRAM_OWNER_ID`
  (singular) is the only owner-identity source in this codebase; not
  changed.
- No persisted health snapshots — `SystemHealth`/`MarketHealth`/
  `SignalHealth` are computed live on every call, matching the
  established house convention (see the audit's own TASK 9
  conclusion).
- No `core/pipeline.py` change of any kind — `SignalHealth.none_count`,
  `MarketHealth.last_price`/`.last_update`, and `SystemHealth.last_scan`
  all remain honest `None`/`0` until a future, separately-approved
  phase adds a real hook (documented in `docs/architecture/MONITORING.md`'s
  own "Future extension" section).
- No signal generation, no trade decision, no risk computation of any
  kind — every module here is read-only observation or append-only
  logging.
- No change to `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/` (Strict Rule).

## Constitution Compliance (checks run at close)

- **Article 3-equivalent isolation** — AST sweep for `decision`/`risk`/
  `execution` imports across `monitoring/**/*.py` and
  `telegram/owner/monitoring_commands.py`: zero matches
  (`tests/monitoring/test_monitoring_isolation.py`). Additional
  belt-and-suspenders check confirms `monitoring/decision_logger.py`
  never imports `signals`/`context`.
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`: no changes in any of those directories this phase.
- **Article 9 (Version Compatibility)** — `monitoring/signal_monitor.py`'s
  pre-existing `SignalMonitor`/`MonitorConfig`/`MonitorResult`
  placeholder is untouched (confirmed zero callers, but left in place
  rather than removed, per Article 9 discipline even for dead code
  without explicit deletion authorization); `database/signal_repository.py`
  gains one new, additive read method; `database/models.py` gains one
  new, additive schema function. No existing public method/field
  signature changed anywhere.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  `telegram/owner/system_commands.py`'s `get_system_health()` and
  `monitoring/provider_health.py`'s health-check functions both
  already existed and are reused outright; the two genuine gaps
  (`ErrorEvent`/`DecisionPipelineEntry` persistence) were added only
  after confirming nothing comparable existed anywhere. See
  `docs/PHASE_CORE_MONITORING_AUDIT.md`.

## Dependency Compliance

`monitoring/models.py` imports only `dataclasses`/`enum`/`typing`.
`monitoring/decision_logger.py` imports only `database.monitoring_repository`,
`monitoring.models`, `core.logger`, and stdlib — never `signals`/
`context` (confirmed by
`test_decision_logger_never_imports_signals_or_context()`).
`database/monitoring_repository.py` imports only `database.*`,
`core.logger`, and stdlib (confirmed by
`test_monitoring_repository_module_confined_to_database_and_stdlib()`).
No file in `monitoring/` imports `ai.*` (confirmed by
`test_monitoring_never_imports_ai_package()`).

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | — (no new top-level package) | — | `monitoring/`, `telegram/owner/`, `database/` (all pre-existing) |
| Modules | `monitoring/models.py`, `system_monitor.py`, `market_monitor.py`, `decision_logger.py`, `error_monitor.py`, `database/monitoring_models.py`, `monitoring_repository.py`, `telegram/owner/monitoring_commands.py` (8) | `monitoring/signal_monitor.py`, `database/signal_repository.py`, `database/models.py`, `telegram/commands.py`, `telegram/handlers.py` (5) | `telegram/owner/system_commands.py` (`get_system_health()`), `monitoring/provider_health.py`, `telegram/admin_service.py` (`AdminService`), `telegram.permissions`/`telegram.command_router` (all read/composed, not modified) |
| Classes | `SystemMonitor`, `DecisionLogger`, `ErrorMonitor`, `MonitoringRepository` (4) | — | `AdminService`, `ProviderRegistry` (composed, not modified) |
| Models | `SystemHealth`, `MarketHealth`, `SignalHealth`, `ErrorSeverity`, `ErrorEvent`, `DecisionPipelineEntry`, `ErrorEventEntry`, `DecisionPipelineEntryRow` (8) | — | `ProviderHealthReport`, `ProviderHealthStatus`, `SystemStatus` |
| Functions | `get_health()`, `record_scan()`, `record_error()`, `get_market_health()`, `get_signal_health()`, `log_entry()`, `get_recent_entries()`, `capture()`, `get_recent_errors()`, `get_error_counts()`, 7 command functions, `init_monitoring_schema()`, `get_signals_today()` (~20) | — | `check_registry_health()`, `check_provider_health()`, `AdminService.get_system_status()` |
| Secrets | — | — | `Secrets.TELEGRAM_OWNER_ID` (unchanged) |
| Tests | 8 new files, 126 new tests | — | — |
| Docs | `docs/PHASE_CORE_MONITORING_AUDIT.md`, `docs/PHASE_CORE_MONITORING_FREEZE.md`, `docs/architecture/MONITORING.md` (3) | — | — |

Totals: **0 new top-level packages** (this phase lives entirely inside
already-existing `monitoring/`, `database/`, `telegram/owner/`), **5
pre-existing files extended in place** (all additive), **4 new
classes**, **2 new database tables**, **0 changes to any pre-existing
public method/field signature**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/` returns no output.

## Next phase recommendation

Per the Director's own stated order: 3–5 weeks of real Owner
monitoring, collecting bugs and data, then AI `66.5` (Performance
Intelligence Foundation) continues, reading from
`monitoring.decision_logger.DecisionLogger`'s own accumulated dataset.
Not decided here — requires its own dedicated Worker Brief per this
session's Director Policy.

## Related documents

- `docs/PHASE_CORE_MONITORING_AUDIT.md` — TASK 0's Foundation Reuse
  Audit.
- `docs/architecture/MONITORING.md` — the full subsystem documentation.
- `docs/owner/OWNER_PANEL.md` — the wider Owner Telegram panel this
  phase's commands are added to.
- `docs/constitution/CONSTITUTION.md` Article 11 — the Foundation
  Reuse Law this phase's entire audit was designed to satisfy.
