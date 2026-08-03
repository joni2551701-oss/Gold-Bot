# Phase B.0 — GoldBot Core Owner Monitoring Alpha Foundation — Freeze

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes Phase B.0, a follow-up Worker Brief
that arrived under the same title as the already-shipped "GoldBot Core
Owner Monitoring Alpha" phase (commit `71f4073`). It records what was
actually built, what was deliberately not duplicated, and the
Constitution/Dependency compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE_B0_AUDIT.md`) found that ~90% of this
brief's own scope already existed, live-wired, tested (126+ tests at
the time), and frozen: `monitoring/system_monitor.py`,
`market_monitor.py`, `signal_monitor.py`, `error_monitor.py`,
`decision_logger.py`, two database tables, and seven Owner Telegram
commands already registered in `OWNER_COMMANDS`
(`owner_status`/`health`/`market`/`signals`/`errors`/`pipeline`/`report`).
Building this brief's own literal TASK 1 (`monitoring/owner/` as a new
subpackage with its own `system_monitor.py`/`market_monitor.py`/etc.)
would have created two competing implementations of the identical
mission and direct command-name collisions. The Director confirmed
(via `AskUserQuestion`) the recommended path: extend the existing
`monitoring/` package in place with only the genuine gaps, no new
subpackage.

## Built this phase

- `monitoring/models.py` (extended) — `HealthStatus` (OK/WARNING/
  CRITICAL), `ResourceSnapshot`, `PerformanceCounters`; `DecisionPipelineEntry`
  gained an additive `stage_durations_ms: Sequence[Tuple[str, float]] = ()`
  field.
- `monitoring/resource_monitor.py` (new) — `get_resource_snapshot()` /
  `record_process_start()`. CPU time and max RSS via stdlib `resource`
  (POSIX-only, `None` when unavailable, never fabricated); thread
  count via `threading.active_count()`; restart count persisted via
  `MonitoringRepository` (the one fact that cannot be tracked
  in-memory, since a restart is a new process by definition); uptime
  relayed from the already-existing `SystemMonitor.uptime_seconds()`
  (never a second uptime tracker). "Loop" and "Latency" from the
  brief's own TASK 2 list are deliberately not duplicated —
  represented by the already-existing `record_scan()`/`last_scan`
  mechanism and `monitoring/provider_health.py`'s own latency field,
  respectively.
- `monitoring/health_monitor.py` (new) — `classify_health()`, a pure,
  deterministic classifier over already-known `SystemHealth` fields
  and optional error counts. No scoring, no weighting, no fabrication.
- `monitoring/performance_collector.py` (new) — `PerformanceCollector`:
  `record_signal()`/`record_decision()`/`record_trade()`/
  `record_reject()`/`record_error()`/`record_reconnect()`/`get_counts()`.
  In-memory only, "Hozircha faqat yig'adi. Hisoblamaydi" (for now,
  only collects, never computes) — distinct from the already-existing
  `monitoring/performance.py`'s `PerformanceTracker`, which computes
  win-rate/strategy stats from closed trades.
- `monitoring/access.py` (new) — `is_owner_monitoring_enabled()`,
  gating only this phase's own new surface (not the seven pre-existing
  live commands, which stay gated by the existing
  `telegram.permissions`/`telegram.command_router` mechanism alone).
- `monitoring/decision_logger.py` (extended) — `log_entry()` and
  `get_recent_entries()` both now accept/relay `stage_durations_ms`
  (caller-supplied only; this module never measures a stage's
  duration itself).
- `database/monitoring_models.py` (extended) — `DecisionPipelineEntryRow`
  gained `stage_durations_ms`; new `ProcessStartEntry` +
  `create_process_start_entry()`.
- `database/monitoring_repository.py` (extended) — `record_decision_entry()`/
  `get_recent_decision_entries()` persist/restore `stage_durations_ms`
  (comma-joined `stage:ms` string, mirroring `criteria_met`'s own
  convention); new `record_process_start()`/`get_restart_count()`.
- `database/models.py` (extended) — `init_monitoring_schema()` gained
  a new `monitoring_process_starts` table and a guarded
  `ALTER TABLE ... ADD COLUMN stage_durations_ms` migration (mirrors
  the codebase's own established `_migrate_signals_table()` pattern).
- `configuration/feature_flags.py` (extended) — `enable_owner_monitoring: bool = False`.
- `telegram/owner/monitoring_commands.py` (extended) — new
  `get_performance_report()` (the `/performance` command, Owner-gated
  additionally by `enable_owner_monitoring`); `get_status_report()`
  appends an "Overall health" line and a "Resources:" line when the
  flag is on, never removing or altering its existing lines.
- `telegram/handlers.py` + `telegram/commands.py` (extended) — new
  `performance_handler()`, new `performance` entry in `OWNER_COMMANDS`.
- `main.py` (extended) — one line, `record_process_start()`, called
  once at `GoldBot.__init__()` (never raises, defensive).
- `tests/monitoring/` (10 new files) + one new
  `tests/telegram/owner/` file — **152 new tests**, exceeding the
  brief's own 150-test minimum, including AST-based isolation and
  compatibility suites.
- Documentation: `docs/PHASE_B0_AUDIT.md`, `docs/PHASE_B0_FREEZE.md`
  (new); `docs/architecture/MONITORING.md` (extended in place);
  `docs/ai/AI_ARCHITECTURE.md`, `docs/ai/AI_INTELLIGENCE_PIPELINE.md`
  (both gained a short cross-reference bullet only — this phase is
  explicitly not part of the `66.x` AI Trading Intelligence
  sub-sequence, confirmed by zero `ai.*` imports anywhere in
  `monitoring/`).

## Not Built this phase

- No new `monitoring/owner/` subpackage — see Audit Summary above.
- No duplicate `system_monitor.py`/`market_monitor.py`/
  `signal_monitor.py`/`error_monitor.py`/decision-pipeline logger.
- No `OWNER_IDS` (plural) — the existing singular
  `Secrets.TELEGRAM_OWNER_ID` gate already satisfies Rule 4's intent;
  a second, parallel owner-identity mechanism would create two
  competing sources for the same bot.
- No renamed/reused command names — `/status`, `/health`, `/market`,
  `/signals`, `/errors`, `/decision` (served by the existing
  `/pipeline`), and `/runtime` (a different, pre-existing AI Runtime
  concern) all stay exactly as they already were.
- No Trade Lifecycle monitor — `execution/` remains intentionally
  inert (no MT5 order calls exist yet, per `CLAUDE.md`'s Trading
  Safety section), so there is no live trade state to observe.
- No `trade_monitor.py`/`trade_manager.py` — neither exists anywhere
  in the repository (confirmed via the audit); Rule 1 names them
  defensively, not as files to create.
- No change to `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, `context/` (Rule 1).
- No BUY/SELL/SL/TP/Lot/Risk/Decision mutation of any kind anywhere in
  this phase's own code (Rule 2) — confirmed by
  `tests/monitoring/test_phase_b0_compatibility.py`.

## Constitution Compliance (checks run at close)

- **Article 3-equivalent isolation** — AST sweep for `decision`/`risk`/
  `execution`/`strategies`/`signals`/`ai.` imports across the four new
  Phase B.0 files: zero matches
  (`tests/monitoring/test_phase_b0_isolation.py`). Confined-import
  checks confirm `access.py` imports only `configuration.feature_flags`;
  `health_monitor.py`/`performance_collector.py` import no database of
  any kind.
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`: no changes in any of those directories this
  phase.
- **Article 9 (Version Compatibility)** — `DecisionPipelineEntry` and
  `DecisionPipelineEntryRow` both gain one new, additive, defaulted
  field (`stage_durations_ms`); `FeatureFlags` gains one new field
  (`enable_owner_monitoring`); `get_status_report()`'s pre-existing
  output lines are never altered, only appended to when the flag is
  on. No existing public method/field signature changed.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed the
  overwhelming majority of this brief's own scope already existed;
  only six genuine, narrow gaps were filled, each as an additive
  extension. See `docs/PHASE_B0_AUDIT.md`.

## Dependency Compliance

`monitoring/access.py` imports only `configuration.feature_flags`.
`monitoring/health_monitor.py` imports only `monitoring.models` and
stdlib `typing`. `monitoring/performance_collector.py` imports only
`monitoring.models` and stdlib `time`. `monitoring/resource_monitor.py`
imports `monitoring.models`, `monitoring.system_monitor`,
`database.monitoring_repository`, `core_layer.logger.logger`, and stdlib
(`threading`, `datetime`, `typing`, `resource`) — never `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `ai.*`. Nothing in
this phase imports `context/` or `core.pipeline` directly.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | — (no new top-level or sub-package) | — | `monitoring/`, `database/`, `telegram/owner/`, `configuration/` (all pre-existing) |
| Modules | `resource_monitor.py`, `health_monitor.py`, `performance_collector.py`, `access.py` (4) | `models.py`, `decision_logger.py`, `monitoring_models.py`, `monitoring_repository.py`, `database/models.py`, `feature_flags.py`, `monitoring_commands.py`, `telegram/handlers.py`, `telegram/commands.py`, `main.py` (10) | `system_monitor.py`, `market_monitor.py`, `signal_monitor.py`, `error_monitor.py` (read/composed, not modified) |
| Classes | `PerformanceCollector` (1) | `DecisionPipelineEntry`, `DecisionPipelineEntryRow`, `MonitoringRepository`, `FeatureFlags` (+1 field each) | `SystemMonitor` (composed via `DEFAULT_MONITOR.uptime_seconds()`) |
| Models | `HealthStatus`, `ResourceSnapshot`, `PerformanceCounters`, `ProcessStartEntry` (4) | `DecisionPipelineEntry.stage_durations_ms`, `DecisionPipelineEntryRow.stage_durations_ms` | `SystemHealth`, `MarketHealth`, `SignalHealth`, `ErrorEvent` |
| Functions | `get_resource_snapshot()`, `record_process_start()`, `classify_health()`, `is_owner_monitoring_enabled()`, `get_performance_report()`, `performance_handler()`, `record_process_start()` (in `resource_monitor.py`), `record_signal/decision/trade/reject/error/reconnect()` module functions (~13) | `log_entry()`, `get_recent_entries()`, `record_decision_entry()`, `get_recent_decision_entries()`, `init_monitoring_schema()`, `get_status_report()` | — |
| Secrets | — | — | `Secrets.TELEGRAM_OWNER_ID` (unchanged) |
| Tests | 10 new files, 152 new tests | `test_monitoring_models.py` (1 test widened), `test_feature_flags.py` (1 test renamed + widened) | — |
| Docs | `docs/PHASE_B0_AUDIT.md`, `docs/PHASE_B0_FREEZE.md` (2) | `docs/architecture/MONITORING.md`, `docs/ai/AI_ARCHITECTURE.md`, `docs/ai/AI_INTELLIGENCE_PIPELINE.md`, `docs/roadmap/VERSIONS.md`, `docs/roadmap/AI_EVOLUTION.md` (5) | — |

Totals: **0 new packages or subpackages**, **10 pre-existing files
extended in place** (all additive), **1 new class**, **1 new database
table + 1 guarded column migration**, **0 changes to any pre-existing
public method/field signature**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/ context/` returns no output.

## Next phase recommendation

Continue Track B: 3-5 weeks of real Owner monitoring on live/paper
market data, collecting bugs, errors, and performance data via this
now-extended `monitoring/` layer, ahead of V1 Final Audit, Beta Test,
and VPS Production. Not decided here — requires its own dedicated
Worker Brief per this session's Director Policy.

## Related documents

- `docs/PHASE_B0_AUDIT.md` — TASK 0's Foundation Reuse Audit, the
  headline finding that most of this brief's scope already existed.
- `docs/architecture/MONITORING.md` — the full, current subsystem
  documentation, updated in place to reflect this phase's additions.
- `docs/PHASE_CORE_MONITORING_AUDIT.md` / `docs/PHASE_CORE_MONITORING_FREEZE.md`
  — the prior phase this one extends.
- `docs/constitution/CONSTITUTION.md` Article 11 — the Foundation
  Reuse Law this phase's entire audit was designed to satisfy.
