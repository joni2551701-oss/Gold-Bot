# Phase B.0 — GoldBot Core Owner Monitoring Alpha Foundation — TASK 0 Audit

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law) and this repository's `CLAUDE.md` Module Reuse Principle.
Mandatory TASK 0 audit, run before any new code for this brief.
Scope per the brief's own list: `logs/`, `database/`, `telegram/`,
`monitoring/`, `analytics/`, `performance/`, `trade_monitor.py`,
`trade_manager.py`, `logger.py`, `feature_flags.py`.

## Headline finding — this phase already exists, under the same name

A prior phase titled **"GoldBot Core Owner Monitoring Alpha"** — the
exact title of this brief — was already built, tested, documented, and
frozen, one day before this brief was issued: commit `71f4073`
("GoldBot Core Owner Monitoring Alpha: system/market/signal/error/
decision-pipeline observation layer"). It is fully merged into the
branch this Worker is developing on and is **live-wired**, not just a
foundation:

- `core_layer/health_monitor/models.py` — `SystemHealth`, `MarketHealth`,
  `SignalHealth`, `ErrorSeverity`, `ErrorEvent`, `DecisionPipelineEntry`
  (primitive-only, no Trading Core object references).
- `core_layer/health_monitor/system_monitor.py` — `SystemMonitor` /
  `DEFAULT_MONITOR`: in-memory uptime tracking, `record_scan()`,
  `record_error()`, `get_health()` composing `AdminService` +
  `check_registry_health()`.
- `core_layer/health_monitor/market_monitor.py` — `get_market_health()`, composing
  `core_layer/health_monitor/provider_health.py`.
- `core_layer/health_monitor/signal_monitor.py` — extended with `get_signal_health()`
  (today's BUY/SELL/NONE counts + average confidence), aggregating
  `SignalRepository.get_signals_today()`. The pre-existing dead
  `SignalMonitor`/`MonitorConfig`/`MonitorResult` placeholder (a
  different, older, `monitor()`-returns-`Not implemented` stub) is left
  untouched alongside it.
- `decision_layer/decision_logger/decision_logger.py` — `DecisionLogger`: `log_entry()` /
  `get_recent_entries()`, a primitive per-criterion pass/fail trace
  (`criteria_met`, `criteria_total`, `decision`, `reason`), persisted.
- `core_layer/health_monitor/error_monitor.py` — `ErrorMonitor`: `capture()` /
  `get_recent_errors()` / `get_error_counts()`, persisted, and relays
  into `SystemMonitor.record_error()`.
- `database_layer/audit_log/monitoring_models.py` + `database_layer/audit_log/monitoring_repository.py`
  — two new append-only tables (`monitoring_error_events`,
  `monitoring_decision_pipeline`).
- `telegram/owner/monitoring_commands.py` — `get_status_report()`,
  `get_health_report()` (reuses `system_commands.get_system_health()`),
  `get_market_report()`, `get_signals_report()`, `get_errors_report()`,
  `get_pipeline_report()`, `get_daily_report()`.
- `telegram/handlers.py` + `telegram/commands.py` — **seven commands
  already registered in `OWNER_COMMANDS` and live-wired**: `owner_status`,
  `health`, `market`, `signals`, `errors`, `pipeline`, `report`.
- `tests/monitoring/` + `tests/telegram/owner/test_owner_commands.py` —
  126 tests at close (182 pass today in `tests/monitoring/` alone,
  including later additions from the Owner Snapshot Reporter work).
- `docs/PHASE_CORE_MONITORING_AUDIT.md`, `docs/PHASE_CORE_MONITORING_FREEZE.md`,
  `docs/architecture/MONITORING.md` — full documentation, already
  frozen.

This is not a partial foundation the way `ai/research/` was relative to
an empty `research/` directory (Phase 66.8). This is the same mission,
built end-to-end, already in production wiring.

## Command-name collision check (this brief's own TASK 9 list)

| Brief's TASK 9 command | Already exists? | Existing owner |
|---|---|---|
| `/health` | **Yes** | `telegram/owner/monitoring_commands.py::get_health_report()`, live |
| `/status` | **Partially** — `/status` (general, "Bot status") already exists as a *non-owner* command (`telegram/commands.py:37`); the owner-scoped equivalent is `/owner_status` | Collision: this brief's `/status` would need `owner_status`'s slot, not a bare `/status` |
| `/errors` | **Yes** | `get_errors_report()`, live |
| `/performance` | **No** | Genuine gap — `core_layer/health_monitor/performance.py`'s `PerformanceTracker` is a *different* concern (computed win-rate/strategy breakdown from closed trades), not a raw counter collector |
| `/market` | **Yes** | `get_market_report()`, live |
| `/signals` | **Yes** | `get_signals_report()`, live |
| `/decision` | **Served by `/pipeline`** | `get_pipeline_report()` already shows the decision pipeline trace under a different command name |
| `/runtime` | **Yes, but a different concern** | `telegram/owner/runtime_commands.py`'s `/runtime` (Phase 61.6/61.7) reports **AI Runtime lifecycle** (provider circuit breaker/health) — not system process uptime. Reusing this name for Phase B.0's own "runtime" (process uptime) would collide in meaning, not just in name. |

## Genuine gaps — what does not exist yet

Cross-referencing this brief's TASK 2–8 against the existing
`monitoring/` package line by line:

1. **System resource metrics (TASK 2)** — CPU, RAM, thread count,
   event-loop health, restart count, heartbeat. Confirmed via
   repo-wide grep: **no `psutil` import anywhere in the codebase**, and
   `core_layer/health_monitor/system_monitor.py` tracks only `uptime_seconds`/
   `database_status`/`data_connection`/`last_scan`/`last_error` — no
   CPU/RAM/thread/restart-count field exists. **Genuine gap.**
2. **OK / WARNING / CRITICAL health classification (TASK 6)** —
   `SystemHealth.status` is a free-text label (`"RUNNING"`), not a
   three-state severity classifier. No `HealthStatus` enum with this
   exact vocabulary exists anywhere. **Genuine gap.**
3. **Pure performance counter collection (TASK 7)** — the brief is
   explicit: "Hozircha faqat yig'adi. Hisoblamaskes ka hisoblamaydi"
   (for now, only collects, does not compute) — signal count, decision
   count, trade count, reject count, runtime, error count, reconnect
   count, as raw tallies. `core_layer/health_monitor/performance.py`'s
   `PerformanceTracker` computes win-rate/strategy stats from *closed
   trades* — a different, already-computing concern. No raw
   "count of decisions this session"/"count of reconnects" tally
   exists anywhere. **Genuine gap**, but narrow: a small, additive
   `PerformanceCollector` counter object.
4. **Per-pipeline-stage timing (TASK 5)** — the brief wants each stage
   of Context → Signal → AI → Decision → Risk → Execution to have its
   own recorded duration. `decision_layer/decision_logger/decision_logger.py` already
   records a per-criterion pass/fail trace and a final decision, but
   **not stage-by-stage timing**. `core/pipeline.py` (read-only, Rule
   1) already logs `stage=... duration=...s` lines per
   `docs/PHASE_CORE_MONITORING_AUDIT.md`'s own read of it, but nothing
   captures those durations into a structured, Owner-queryable record.
   **Genuine gap**, narrow: an additive stage-timing entry appended
   alongside the existing decision trace.
5. **`enable_owner_monitoring` feature flag (Rule 5)** — confirmed via
   grep: no such flag exists in `configuration/feature_flags.py` today.
   **Genuine gap.**
6. **`OWNER_IDS` (Rule 4)** — confirmed via grep: no `OWNER_IDS` exists
   anywhere. The only owner-identity source is the existing, singular
   `Secrets.TELEGRAM_OWNER_ID`, which the live `telegram.permissions`/
   `telegram.command_router` gate already enforces on every
   `OWNER_COMMANDS` entry (confirmed by the prior phase's own audit).
   Introducing a second, parallel `OWNER_IDS` (plural) mechanism would
   create two competing owner-identity sources for the same bot — the
   prior phase's freeze explicitly declined this for the same reason.
   **Not a gap to fill with new code**; the existing single-owner gate
   already satisfies Rule 4's intent (only OWNER can use these
   commands).
7. **`/performance` command** — no Owner command surfaces the TASK 7
   counters yet. **Genuine gap**, once TASK 7's counter itself exists.

## `trade_monitor.py` / `trade_manager.py` (Rule 1's own named files)

Neither file exists in the repository today (confirmed via `Glob`).
Rule 1 names them defensively as untouchable *if they existed*; since
they don't, there is nothing to avoid touching, and nothing to build
under those names either — `execution/` remains intentionally inert
(no MT5 order calls, per `CLAUDE.md`'s Trading Safety section), so a
real trade-lifecycle monitor has no live trade state to observe yet.
Trade Lifecycle from this brief's own OBJECTIVE list is therefore
**out of scope until `execution/` is wired**, consistent with
`docs/PHASE_CORE_MONITORING_FREEZE.md`'s own "Not Built this phase"
section for the prior phase.

## `logs/`, `analytics/`, `performance/` (top-level)

- `logs/` — does not exist as a top-level directory or package
  anywhere in the repository (confirmed via `Glob`/`ls`).
- `analytics/` — reviewed; computes `SignalPerformance`/execution/
  learning reports from closed data, a different concern from live
  Owner monitoring, consistent with every prior phase's own "reviewed,
  not reused" conclusion for this package.
- `performance/` (top-level) — does not exist; the only
  performance-named module is `core_layer/health_monitor/performance.py`
  (`PerformanceTracker`, reviewed above).

## Conclusion

Per Constitution Article 11 and `CLAUDE.md`'s Module Reuse Principle
("Reuse is the default outcome, not the exception... a new top-level
package is the highest-cost option and should be rare"): creating a
new `monitoring/owner/` subpackage that duplicates
`system_monitor.py`/`market_monitor.py`/`signal_monitor.py`/
`error_monitor.py`/a decision-pipeline logger — each already existing,
live, and tested under those near-identical names one directory level
up — would produce two competing implementations of the identical
mission inside the same `monitoring/` tree, with direct Owner-command
name collisions (`/health`, `/market`, `/signals`, `/errors`,
`/status`, `/runtime`).

**Recommendation carried into this phase's implementation:** extend
the existing `monitoring/` package and `telegram/owner/monitoring_commands.py`
in place with only the six genuine gaps identified above (system
resource metrics, OK/WARNING/CRITICAL classification, a pure
performance counter collector, per-stage pipeline timing, the
`enable_owner_monitoring` feature flag, and a new `/performance`
command) — no new `monitoring/owner/` subpackage, no duplicate
`system_monitor.py`/`market_monitor.py`/`signal_monitor.py`/
`error_monitor.py`. This is documented here per TASK 0's own "duplicate
qilma" (don't duplicate) instruction, and reported to the Director
before proceeding, since it changes this brief's own literal TASK 1
package-location instruction.

## Related documents

- `docs/PHASE_CORE_MONITORING_AUDIT.md` / `docs/PHASE_CORE_MONITORING_FREEZE.md`
  — the prior phase's own audit and freeze, covering the same mission.
- `docs/architecture/MONITORING.md` — the existing subsystem
  documentation this phase extends rather than replaces.
