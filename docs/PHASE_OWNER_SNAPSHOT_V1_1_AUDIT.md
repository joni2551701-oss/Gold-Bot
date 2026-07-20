# GoldBot Core Owner Snapshot Reporter v1.1 — Foundation Reuse Audit

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law) and the "GoldBot Core Owner Snapshot Reporter v1.1
Enhancement" Worker Brief's own TASK 0. Audits `monitoring/`,
`database/`, `telegram/owner/`, `telegram/bot.py`,
`monitoring/run_snapshot.py`, `snapshot_collector.py`,
`snapshot_formatter.py`, `ai/audit/`, and `core/pipeline.py` to
determine, per brief TASK, what data honestly exists, what is already
persisted, and what would need a new adapter — before writing any
v1.1 code. No Trading Core file (`core/`, `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`) is modified by this audit or
by anything it recommends.

## Method

Read every candidate data source directly (not assumed from prior
phase docs), traced each one back to its actual production caller
(`main.py`, `core/pipeline.py`), and classified each v1.1 TASK's
requested field as **Real** (a live, wired, persisted source exists),
**Proxy** (a real source exists but measures something adjacent to
what the brief's worked example shows), or **Unavailable** (no source
exists anywhere in the codebase; will not be fabricated per
`CLAUDE.md`'s "no unnecessary refactor" / this session's own
established field-honesty discipline — see
`docs/OWNER_SNAPSHOT_REPORTER.md`'s `telegram_status`/`uptime_info`
precedent).

## Per-TASK findings

### TASK 1 — Pipeline Activity Monitoring

**Proxy.** No pipeline-run counter or duration exists anywhere.
`core/pipeline.py`'s `TradingPipeline.run()` computes
`total_duration = time.perf_counter() - pipeline_start` and logs it
(`pipeline_finished duration=...`), but only to `core.logger` — never
persisted, never readable by a separate one-shot process in a later
GitHub Actions run. `monitoring.decision_logger.DecisionLogger` (the
brief's own named "monitoring decision pipeline" source) is a real,
persisted table (`monitoring_decision_pipeline`) but has **zero
production callers** — `grep -rn "DecisionLogger\|log_entry("` across
the repository finds only `monitoring/decision_logger.py` itself and
its own tests. `core/pipeline.py` never constructs or calls it. This
table will read empty in production today.

The only real, wired per-cycle record is the `signals` table itself:
`main.py`'s `TradingPipeline(..., persist_signals=True)` (confirmed by
reading `main.py` directly) makes `core/pipeline.py` persist one
`SignalRecord` row for **every** candidate the pipeline evaluates that
reaches the database stage — "Signal records are always built for
every candidate regardless of approval... only written to the
database if `persist_signals=True`" (`core/pipeline.py`'s own
docstring, lines 184-191).

**v1.1 design decision**: `pipeline_runs_today`/`pipeline_last_at`/
`pipeline_status` are sourced from `SignalRepository.get_signals_today()`
(already used elsewhere in this package) as a proxy for "pipeline
reached the persistence stage today" — **not** a literal GitHub
Actions execution count (a `main.py` run that aborts before the
database stage, e.g. on a `PipelineGuard` block, leaves no trace
here). `pipeline_last_status` is derived only from whether any row
exists today, never from a real per-run exit code (none is persisted).
`Last Duration` is **not implemented** — no honest source exists; a
future phase could add one only by hooking `core/pipeline.py` itself
(a Trading Core change, explicitly out of scope, same class of gap as
`docs/architecture/MONITORING.md`'s already-documented
`SystemHealth.last_scan`/`SignalHealth.none_count` limitations).

### TASK 2 — Signal Intelligence Summary

**Real.** `database/signal_repository.py`'s `get_signals_today()`
(existing, reused by `monitoring/signal_monitor.py` already) returns
every today's row with `ai_decision` (`APPROVE`/`REJECT`/`NO_TRADE`,
from `decision.models.DecisionAction`, confirmed via
`database/signal_record.py`), `strategy_name`/`strategy`
(`FVG_STRATEGY`/`AMD_STRATEGY`/`LIQUIDITY_SWEEP_STRATEGY`, confirmed
via `strategies/*.py`), and `confidence_score` (0.0-1.0 scale,
confirmed via `decision/decision_engine.py`'s own comment "0.0-1.0
scale as every other confidence field in this codebase"). Approved/
Rejected counts and the strategy breakdown are all directly computable
from this one already-fetched row set — no new adapter needed. Score
display multiplies `confidence_score` by 100 (unit conversion of real
data, not fabrication) to match the brief's own "Score: 82" example.

### TASK 3 — Decision Engine Snapshot

**Real** for Total/Approved/Rejected/Average Confidence (same
`signals` table rows as TASK 2 — this v1.1 layer does not maintain two
independent decision datasets, since only one exists). **Proxy** for
"Average Risk Score": no numeric risk score is persisted anywhere —
`risk_status` on the `signals` table is a string (`PASSED`/`BLOCKED`,
from `RiskResult.approved`, confirmed via `database/signal_record.py`),
not a score. Inventing a numeric percentage would be fabrication
(forbidden). v1.1 instead reports **Risk Pass Rate** — the real,
honestly-computable percentage of today's decisions with
`risk_status == "PASSED"` — as the closest honest analog, clearly
labeled as a pass rate, not a "score". The brief's own worked example
(TASK 9) shows different Signal-section vs Decision-section
approve/reject numbers (5 signals vs 10 decisions); since both
sections read the same single source, v1.1's real output will show
matching totals between the two sections — the brief's numbers were
illustrative sample data, not a mandate to source a second dataset
that does not exist in this codebase.

### TASK 4 — AI Layer Monitoring

**Unavailable today — exactly the brief's own anticipated case.**
`ai/audit/request_log.py`'s `RequestLog` and
`ai/audit/response_log.py`'s `ResponseLog` are **in-memory only**
(confirmed by reading both files directly — "In-memory record...
this module never imports `database/`"). A GitHub Actions run starts a
fresh Python process every 15 minutes; any AI usage that happened
during a *different* process (e.g. a user's `/ai_ask` Telegram command
handled by the long-running `telegram.polling` process, once deployed)
is invisible to `monitoring/run_snapshot.py` — there is no persistence
layer bridging the two. Per the brief's own explicit instruction
("Agar data mavjud bo'lmasa: AI: No data collected yet. Fake
statistika yaratish taqiqlanadi.") v1.1 reports `ai_status="NO_DATA"`
and `ai_requests_today=0` unconditionally in this Alpha layer, with
the reason documented here and in `docs/OWNER_SNAPSHOT_REPORTER.md`
rather than silently omitted.

### TASK 5 — Market Data Monitoring Upgrade

**Real** for Provider/Symbol (already-read `Config.MARKET_DATA_PROVIDER`/
`DEFAULT_SYMBOL`) and Status (existing `get_market_health()`).
**Proxy** for Candles/Timeframes: `Config.TIMEFRAME_HISTORY` is a real,
configured constant (`{"M15": 200, "H1": 200, "H4": 100, ...}`), but
`main.py` only ever constructs `TradingPipeline(symbol="XAUUSD",
interval="M15", ...)` — the live pipeline only fetches M15 today.
Reporting "Timeframes: M15, H1, H4" (the brief's own worked example)
would misrepresent what the system actually does. v1.1 reports the
single real interval currently configured (`M15`) and its configured
candle count (`200`, from `Config.TIMEFRAME_HISTORY["M15"]`) rather
than the brief's three-timeframe example, which does not reflect the
current single-timeframe pipeline.

### TASK 6 — Error Intelligence

**Real.** `monitoring.error_monitor.ErrorMonitor` (existing,
persisted via `MonitoringRepository`) already exposes
`get_recent_errors()`/`get_error_counts()`. Today/Critical/Warning
splits and Last Error module+time are all directly computable from
`get_recent_errors(hours=24)`'s already-returned `ErrorEvent.severity`/
`.module`/`.timestamp` fields — no new adapter needed.

### TASK 7 — System Runtime Metrics

**Real**, self-measured. `monitoring/run_snapshot.py` can honestly
time its own collect→format→send sequence with `time.perf_counter()`
(same "always a real, measured number, never estimated" convention
`monitoring/provider_health.py`'s `latency_ms` already established) —
this is the only "pipeline"/"workflow" execution this process can ever
honestly observe (its own). "Next Run" is a deterministic computation
from the known `cron: "*/15 * * * *"` schedule, not a guess.

### TASK 8 — Database Statistics

**Real.** `SignalRepository`/`MonitoringRepository` both already
expose row-returning read methods; simple `len()` counts over
`get_signals_today()` (today's scope, matching every other v1.1
field's "today" framing) and `MonitoringRepository.get_recent_errors()`/
`get_recent_decision_entries()` need no new database method.
`db_pipeline_events_total` will read 0 today for the same reason as
TASK 1 (`DecisionLogger` unwired) — documented, not hidden.

## What needs a new adapter

**Nothing.** Every v1.1 field is computable by aggregating fields
already returned by an existing, already-imported function
(`get_signals_today()`, `get_market_health()`, `get_recent_errors()`)
or by the collector's own self-timing. No new repository method, no
new monitoring submodule, no new Telegram client. All new logic is
pure aggregation inside `monitoring/snapshot_collector.py` (TASK 2's
own established pattern) and pure formatting inside
`telegram/owner/snapshot_formatter.py` (TASK 3's own established
pattern) — the same split this package's Alpha phase already used.

## Reused outright (no duplication)

- `monitoring.system_monitor.get_health()`
- `monitoring.market_monitor.get_market_health()`
- `monitoring.signal_monitor.get_signal_health()`
- `monitoring.error_monitor.ErrorMonitor`
- `database.signal_repository.SignalRepository` (`get_signals_today()`,
  `get_latest_signal()`)
- `database.monitoring_repository.MonitoringRepository`
  (`get_recent_decision_entries()`, for the honest 0-today count)
- `telegram.bot.TelegramBot` (via the existing
  `telegram/owner/snapshot_sender.py`, unchanged)
- `core.secrets.Secrets`

## Conclusion

v1.1 is additive composition only, consistent with the Alpha phase's
own LOCK Policy ("permitted: new snapshot fields, new report formats,
new monitoring metrics feeding the collector"). No Director Decision
pause required — every source was confirmed to already exist by
reading the actual code, not assumed from a prior phase's docs.
