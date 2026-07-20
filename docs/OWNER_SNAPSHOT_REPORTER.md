# GoldBot — Owner Snapshot Reporter (Alpha, v1.1)

Governed by `docs/constitution/CONSTITUTION.md`. Documents the
"GoldBot Core Owner Snapshot Reporter Alpha" phase: a GitHub-Actions-
driven, one-shot alternative that fills the gap before VPS 24/7
runtime exists. Full Foundation Reuse Audit:
`docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`. Full freeze:
`docs/PHASE_OWNER_SNAPSHOT_FREEZE.md`.

**v1.1 (Operational Intelligence Upgrade)** extended the reporter with
Pipeline/Signal/Decision/AI/Market/Error/Runtime/Database detail — see
"v1.1 fields" below and `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`/
`docs/PHASE_OWNER_SNAPSHOT_V1_1_FREEZE.md` for the full audit/freeze.
It remains what it always was: a temporary Alpha layer, not a VPS
replacement, not a new source of truth beyond what already existed in
`monitoring/`/`database/`.

## Why this exists

`docs/TELEGRAM_RUNTIME.md`'s startup notification and heartbeat only
fire once `telegram.polling` is actually deployed on a VPS — which,
per `docs/PHASE_BRANCH_SYNC_AUDIT.md`, is not yet true. GitHub
Actions, meanwhile, is already running today (`ci.yml`, `trading_bot.yml`).
This phase adds a third scheduled workflow, `owner_snapshot.yml`, that
runs a short-lived Python process every 15 minutes: collect a snapshot
of Core/Database/Market Data/Signal/Error state, format it, and send
it to the Owner's Telegram — all without a persistent process.

**This does not replace VPS 24/7 runtime.** It is an explicitly
temporary Alpha layer for pre-beta observation, exactly as the
brief's own header states.

## Architecture

```
GitHub Actions (every 15 minutes)
      |
      v
monitoring/run_snapshot.py       (TASK 6 -- one-shot entry point)
      |
      v
monitoring/snapshot_collector.py (TASK 2 -- aggregation only)
      |          \
      v           v
monitoring/       telegram/owner/
snapshot_models.py snapshot_formatter.py  (TASK 1 / TASK 3)
      |
      v
telegram/owner/snapshot_sender.py (TASK 4 -- reuses telegram.bot.TelegramBot)
      |
      v
Owner Telegram
```

## What's reused (no duplication — TASK 0's own rule)

| New file | Reuses |
|---|---|
| `monitoring/snapshot_collector.py` | `monitoring.system_monitor.get_health()`, `monitoring.market_monitor.get_market_health()`, `monitoring.signal_monitor.get_signal_health()`, `monitoring.error_monitor.ErrorMonitor`, `database.signal_repository.SignalRepository.get_latest_signal()` (already existed) |
| `telegram/owner/snapshot_sender.py` | `telegram.bot.TelegramBot` (the same outbound bot `main.py`'s pipeline uses) |
| Owner identity | `core.secrets.Secrets.TELEGRAM_OWNER_ID` (the same source every other Owner-only path uses) |

No new health-check logic, no new Telegram client, no Core code
touched.

## `OwnerSnapshot` fields — what they honestly mean

`monitoring/snapshot_models.py`:

```python
@dataclass(frozen=True)
class OwnerSnapshot:
    timestamp: str
    status: str              # "OK" | "DEGRADED"
    core_status: str         # from SystemHealth.status
    database_status: str     # from SystemHealth.database_status
    telegram_status: str     # see below -- NOT polling liveness
    market_data_status: str  # from MarketHealth.data_source_status
    last_signal: Optional[str]
    error_count: int
    uptime_info: str         # see below -- per-process, not Core uptime
    signals_today: int = 0   # additive field, LOCK Policy permits this
```

Two fields need an explicit caveat, documented here so they are never
misread:

- **`telegram_status`** reflects whether *this run's own*
  `TelegramBot` construction succeeded (a valid `TELEGRAM_BOT_TOKEN`
  was readable) — it says nothing about whether the separate,
  long-running `telegram.polling` listener is up. This one-shot
  script has no way to observe that process at all.
- **`uptime_info`** is `monitoring.system_monitor.SystemMonitor`'s
  in-memory, per-process uptime. Since GitHub Actions starts a fresh
  Python process every 15 minutes, this will read a few seconds on
  every single run — it is **not** a continuous "Core has been up for
  N hours" figure. This is a known, honest limitation of a one-shot
  Alpha reporter, not a bug (see `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`'s
  decision #4).

## v1.1 fields — what they honestly mean

Full Foundation Reuse Audit for every field below:
`docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`. Every field is additive
(new fields with defaults, LOCK Policy permits this) — nothing above
was renamed, moved, or removed.

- **`pipeline_runs_today`/`pipeline_last_at`/`pipeline_last_status`**
  are a **proxy**: sourced from the `signals` table (the only real,
  wired per-cycle decision record — `main.py` runs
  `TradingPipeline(..., persist_signals=True)`, so one row is
  persisted per candidate the pipeline evaluates), not a literal count
  of `main.py` executions. A run that aborts before the database stage
  leaves no trace here. There is no honest source for pipeline
  duration anywhere in this codebase — the formatter always shows
  `Duration: N/A` rather than inventing one.
- **`signals_approved`/`signals_rejected`/`strategy_breakdown`/
  `last_signal_score`** and **`decision_total`/`decision_approved`/
  `decision_rejected`/`decision_avg_confidence_pct`** are **real**,
  aggregated from the same `signals` table rows
  (`ai_decision`/`strategy_name`/`confidence_score`).
  `decision_risk_pass_rate_pct` is the honest substitute for a numeric
  "risk score" — no such field is persisted anywhere, only a
  `PASSED`/`BLOCKED` `risk_status` string, so this reports the real
  percentage of today's decisions that passed Risk Manager review.
- **`ai_requests_today`/`ai_status`** are **always `0`/`"NO_DATA"`** by
  design. `ai/audit/request_log.py`/`response_log.py` are in-memory
  only, never persisted — a fresh GitHub Actions process every 15
  minutes can never see AI activity from a *different* process. Not a
  bug; exactly the brief's own anticipated fallback.
- **`market_provider`/`market_symbol`/`market_timeframe`/
  `market_candles_configured`** are **real** configuration values
  (`Config.MARKET_DATA_PROVIDER`, the collector's own symbol/provider
  arguments, `Config.TIMEFRAME_HISTORY`). `market_timeframe` is always
  `M15` — the single interval `main.py` actually fetches today, not a
  three-timeframe example.
- **`errors_critical`/`errors_warning`/`last_error_module`/
  `last_error_time`** are **real**, aggregated from
  `ErrorMonitor.get_recent_errors()`'s already-persisted severity/
  module/timestamp fields.
- **`runtime_execution_seconds`** is a **real**, `time.perf_counter()`-
  measured duration of this run's own `collect_snapshot()` +
  `format_snapshot()` — it deliberately excludes the Telegram send
  itself (which hasn't happened yet when the message is composed).
  **`runtime_next_check`** is a deterministic computation from the
  known 15-minute cron schedule, not a guess.
- **`db_signals_total`/`db_errors_total`** are **real** row counts
  (today-scoped, matching every other v1.1 field).
  **`db_pipeline_events_total`** reads `0` today for the same reason
  as `pipeline_runs_today`'s own caveat: `monitoring_decision_pipeline`
  has no production writer yet.

## Owner failure notification

If `collect_snapshot()`/`format_snapshot()` itself raises,
`monitoring/run_snapshot.py` sends the Owner a short failure message
instead of the run only showing up as red in GitHub Actions (Actions
failures are not otherwise visible to the Owner in Telegram):

```
🔴 GoldBot Snapshot Failed
Module:
monitoring.run_snapshot
Error:
<str(exception)>
Time:
18:15 UTC
```

Best-effort only — if the failure notification's own send also fails,
that second failure is logged, never re-raised (the run has already
failed once). The exception text this shows can never contain
`TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`: it originates from
`collect_snapshot()`/`format_snapshot()`, neither of which lets a raw
`TelegramBot` exception escape (`_telegram_status()` already catches
its own exceptions internally).

## Message format (v1.1)

```
🟢 GoldBot Snapshot v1.1
⏰ Time:
20:00 UTC
🖥 Core:
✅ RUNNING
📊 Pipeline:
Runs Today: 12
Last: ✅ SUCCESS
Last At: 19:58 UTC
Duration: N/A
📈 Market:
XAUUSD (M15)
twelvedata:
✅ ONLINE
🎯 Signals:
Today: 5
Approved: 1
Rejected: 4
Strategies: AMD: 3, FVG: 2
Last Signal:
BUY @ 2026-01-01T19:55:00
Score: 82
🧠 AI:
No data collected yet
⚖️ Decision:
Total: 10
Approved: 2
Rejected: 8
Avg Confidence: 74.0%
Risk Pass Rate: 32.0%
💾 Database:
Signals: 245
Errors: 12
Pipeline Events: 0
✅ HEALTHY
⚠️ Errors:
Today: 3
Critical: 0
Warning: 3
Last: MarketDataNormalizer @ 17:25 UTC
⚠️ REVIEW
📡 Telegram:
✅ OK
Runtime:
15h 20m
Next Check: 20:15 UTC
```

`🟢`/`🟡` reflects overall `status`; each individual line gets its own
✅/⚠️/❌/❓ icon from `telegram/owner/snapshot_formatter.py`'s status map.

## Secrets

`monitoring/run_snapshot.py`'s `_verify_secrets()` checks all four
secrets named in the brief (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_OWNER_ID`,
`TWELVE_DATA_API_KEY`, `GEMINI_API_KEY`), logging presence/absence
only, never a value. Only the first two actually gate sending —
`monitoring.run_snapshot` never reads the latter two directly, and
their absence already degrades individual `collect_snapshot()` fields
gracefully rather than crashing. A missing `TELEGRAM_BOT_TOKEN`/
`TELEGRAM_OWNER_ID` logs an exact `Snapshot send aborted: Missing X`
line and exits non-zero, so the GitHub Actions run shows red with a
clear, specific reason (TASK 7's own requirement) instead of a silent
no-op.

## Entry point

```
python -m monitoring.run_snapshot
```

One-shot — collects, formats, sends, exits. No infinite loop (unlike
`telegram.polling`, which GitHub Actions could never run anyway — see
`docs/PHASE_BRANCH_SYNC_AUDIT.md`).

## Schedule

`.github/workflows/owner_snapshot.yml`: `cron: "*/15 * * * *"` plus
`workflow_dispatch` for manual runs. Own concurrency group
(`goldbot-owner-snapshot`), separate from `trading_bot.yml`'s
`goldbot` group — the two workflows never block each other. Same
production-branch pin as `trading_bot.yml`
(`ref: claude/code-analysis-optimization-pwfo3q`, see
`docs/PHASE_BRANCH_SYNC_AUDIT.md`). `timeout-minutes: 5` (Audit &
Hardening) bounds a hung TwelveData/Telegram call — the job's own real
completion time is a few seconds, so 5 minutes is a generous ceiling,
not a normal-case limit.

## LOCK Policy (per the brief)

`monitoring/snapshot_*` and `telegram/owner/snapshot_*` are locked as
of this phase's freeze:

- **Allowed**: new snapshot fields, new report format variations, new
  monitoring metrics feeding in.
- **Forbidden**: renaming, moving, breaking the existing
  `OwnerSnapshot`/`collect_snapshot()`/`format_snapshot()`/
  `send_snapshot()` public shapes, or adding a Core dependency.

## Related documents

- `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md` — TASK 0's Foundation Reuse
  Audit (Alpha).
- `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md` — the Alpha phase's freeze.
- `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md` — v1.1's own Foundation
  Reuse Audit (Real/Proxy/Unavailable classification per field).
- `docs/PHASE_OWNER_SNAPSHOT_V1_1_FREEZE.md` — v1.1's freeze.
- `docs/TELEGRAM_RUNTIME.md` — the live-runtime heartbeat/notification
  layer this phase substitutes for until a VPS exists.
- `docs/architecture/MONITORING.md` — the wider Core Owner Monitoring
  layer this phase's collector composes.
