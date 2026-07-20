# GoldBot Core Owner Snapshot Reporter v1.1 — Freeze

Governed by `docs/constitution/CONSTITUTION.md` Article 12
(Architecture Evolution Law). Closes "GoldBot Core Owner Snapshot
Reporter v1.1 — Operational Intelligence Upgrade", building on the
Alpha phase frozen by `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md`.

## Audit Summary

TASK 0's audit (`docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`) classified
every requested field as **Real** (a live, wired, persisted source
exists), **Proxy** (a real source exists but measures something
adjacent to the brief's worked example), or **Unavailable** (no source
exists; not fabricated). Key findings that shaped this phase:

- The `signals` table (via `SignalRepository.get_signals_today()`,
  already reused by the Alpha phase) is the real, wired per-decision
  record — `main.py` runs `TradingPipeline(..., persist_signals=True)`,
  persisting one row per candidate regardless of approval. This is the
  single source for Pipeline Activity, Signal Intelligence, and
  Decision Engine Snapshot — the brief's own three separate sections
  read the same underlying data.
- `monitoring.decision_logger.DecisionLogger` (the brief's own named
  "monitoring decision pipeline" source) has zero production callers
  anywhere in the codebase — it will read 0 today.
  `db_pipeline_events_total`/`pipeline_runs_today` are documented as
  reading this honestly, not silently.
- `ai/audit/request_log.py`/`response_log.py` are in-memory only,
  never persisted — AI Layer Monitoring is always `NO_DATA`/`0` by
  design, exactly the brief's own anticipated fallback.
- No numeric risk score is persisted anywhere (only a `PASSED`/
  `BLOCKED` string) — "Average Risk Score" became **Risk Pass Rate**,
  a real percentage, not an invented score.
- No pipeline run duration is persisted anywhere — the formatter shows
  `Duration: N/A`, never a fabricated value.

No Director Decision pause was required — every source was confirmed
by reading the actual code, and every gap resolved via honest
reporting rather than fabrication (this session's established
convention).

## Built this phase

- `monitoring/snapshot_models.py` (extended) — 26 new additive
  `OwnerSnapshot` fields covering TASK 1-8, all with defaults.
- `monitoring/snapshot_collector.py` (extended) — `_decision_rows_today()`
  (one shared read of today's `signals` rows), `_pipeline_activity()`,
  `_decision_breakdown()`, `_last_signal_score()`, `_error_breakdown()`,
  `_pipeline_events_total()`, `next_check_time()`. All pure aggregation
  over already-existing sources, each independently defensive (never
  raises).
- `telegram/owner/snapshot_formatter.py` (rewritten) — the v1.1 emoji
  message layout (TASK 9), including every honest "N/A"/"No data
  collected yet" caveat.
- `monitoring/run_snapshot.py` (extended) — owner failure notification
  on collection/formatting failure (Audit & Hardening TASK 4,
  best-effort, never raises), self-timed `runtime_execution_seconds`/
  `runtime_next_check` wiring via `dataclasses.replace()`.
- `.github/workflows/owner_snapshot.yml` (extended) — `timeout-minutes: 5`
  (Audit & Hardening TASK 5).
- `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`, this freeze doc (new);
  `docs/OWNER_SNAPSHOT_REPORTER.md`, `docs/architecture/MONITORING.md`,
  `docs/DEPLOYMENT.md` extended.
- `tests/monitoring/test_snapshot_models.py`,
  `tests/monitoring/test_snapshot_collector.py`,
  `tests/monitoring/test_run_snapshot.py`,
  `tests/telegram/owner/test_snapshot_formatter.py`,
  `tests/workflows/test_owner_snapshot_workflow.py` (extended) — 60+
  new tests covering every new field/helper, missing-data/empty-
  database/error states, owner-only delivery (unchanged from Alpha),
  failure notification (including "never logs a secret" and "never
  raises when the notification itself fails"), and the workflow
  timeout.

## Not built this phase

- No `monitoring_history` table or any new persistence — TASK 7's own
  instruction ("hozircha yaratmaslik... faqat recommendation") is
  honored: see "Future recommendation" below.
- No change to `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, `context/` (Strict Rule).
- No wiring of `DecisionLogger` into `core/pipeline.py` — would touch
  Trading Core, explicitly out of scope; documented as the reason
  `pipeline_runs_today`/`db_pipeline_events_total` read as a proxy/zero
  today, not silently.
- No AI/LLM call of any kind (Strict Rule) — AI Layer Monitoring reads
  existing in-memory logs only, never queries a provider.
- No Telegram polling binding (Strict Rule).

## Future recommendation (TASK 7, not built)

A `monitoring_history` table (mirroring `monitoring_error_events`'/
`monitoring_decision_pipeline`'s own append-only shape in
`database/monitoring_repository.py`) would let a future phase persist
each `OwnerSnapshot` and answer "how has GoldBot Core trended over the
last N days" — not just "what does it look like right now". Two
prerequisites before that's worth building: (1) `DecisionLogger`
actually wired into `core/pipeline.py` (a separate, explicitly-approved
Trading Core change), since without it there's no real decision-level
history to persist beyond what `signals` already holds; (2) a
retention/pruning policy, since a 15-minute cadence accumulates ~35k
rows/year with no natural expiry today. Not started this phase.

## Constitution Compliance (checks run at close)

- **Isolation** — `monitoring/snapshot_*.py` and
  `telegram/owner/snapshot_*.py` import only `monitoring.*`,
  `database.signal_repository`, `database.monitoring_repository`,
  `telegram.bot`, `telegram.owner.snapshot_sender`, `core.secrets`,
  `core.logger`, `config`, and stdlib. No `decision`/`risk`/
  `execution`/`ai.*`/`signals`/`strategies` import anywhere.
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`: no changes in any of those directories this
  phase.
- **Article 9 (Version Compatibility)** — `OwnerSnapshot`/
  `collect_snapshot()`/`send_snapshot()`'s existing public shapes are
  unbroken; every new field has a default. `format_snapshot()`'s
  *output text* changed (the brief's own TASK 9 requirement), but its
  signature (`OwnerSnapshot -> str`) did not.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  every new field is computable from an already-imported function; no
  new repository method, no new monitoring submodule, no new Telegram
  client.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | — | — | `monitoring/`, `telegram/owner/` (both pre-existing) |
| Modules | — | `monitoring/snapshot_models.py`, `snapshot_collector.py`, `run_snapshot.py`, `telegram/owner/snapshot_formatter.py` (4) | `monitoring/error_monitor.py`, `database/signal_repository.py`, `database/monitoring_repository.py`, `config.Config` (all composed, not modified) |
| Fields | 26 new `OwnerSnapshot` fields | — | — |
| Functions | `_decision_rows_today()`, `_pipeline_activity()`, `_decision_breakdown()`, `_last_signal_score()`, `_error_breakdown()`, `_pipeline_events_total()`, `next_check_time()`, `_format_failure_message()`, `_notify_owner_of_failure()` (9) | `collect_snapshot()`, `format_snapshot()`, `run_snapshot_report()` | `get_signals_today()`, `get_latest_signal()`, `get_recent_errors()`, `get_recent_decision_entries()` |
| Workflows | — | `.github/workflows/owner_snapshot.yml` (`timeout-minutes: 5`) | — |
| Tests | — | 5 files, 60+ new tests | — |
| Docs | `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`, this freeze doc (2) | `docs/OWNER_SNAPSHOT_REPORTER.md`, `docs/architecture/MONITORING.md`, `docs/DEPLOYMENT.md` (3) | — |

Totals: **0 new top-level packages**, **0 new modules** (only
extensions to the 4 existing v1.0 files), **1 workflow extended**,
**26 new additive fields**, **9 new helper functions**, **0 breaking
changes to any pre-existing public method/field signature**, **60+ new
tests**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/ context/` returns no output.

## LOCK Policy (unchanged, reaffirmed)

`monitoring/snapshot_*` and `telegram/owner/snapshot_*`:

- **Permitted**: new snapshot fields, new report formats, new
  monitoring metrics feeding the collector.
- **Forbidden**: rename, move, breaking API, or any Core dependency
  added to these modules.

## Related documents

- `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md` — TASK 0's Foundation
  Reuse Audit.
- `docs/OWNER_SNAPSHOT_REPORTER.md` — the full subsystem
  documentation, updated for v1.1.
- `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md` — the Alpha phase this builds
  on.
- `docs/architecture/MONITORING.md` — the wider Core Owner Monitoring
  layer this phase's collector composes.
