# GoldBot — Owner Snapshot Reporter (Alpha)

Governed by `docs/constitution/CONSTITUTION.md`. Documents the
"GoldBot Core Owner Snapshot Reporter Alpha" phase: a GitHub-Actions-
driven, one-shot alternative that fills the gap before VPS 24/7
runtime exists. Full Foundation Reuse Audit:
`docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`. Full freeze:
`docs/PHASE_OWNER_SNAPSHOT_FREEZE.md`.

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

## Message format

```
🟢 GoldBot Snapshot
Time:
20:00 UTC
Core:
✅ RUNNING
Database:
✅ OK
Telegram:
✅ OK
Market Data:
✅ ONLINE
Signals Today:
3
Last Signal:
BUY @ 2026-01-01T19:55:00
Errors:
0
Runtime:
15h 20m
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
`docs/PHASE_BRANCH_SYNC_AUDIT.md`).

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
  Audit.
- `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md` — this phase's freeze.
- `docs/TELEGRAM_RUNTIME.md` — the live-runtime heartbeat/notification
  layer this phase substitutes for until a VPS exists.
- `docs/architecture/MONITORING.md` — the wider Core Owner Monitoring
  layer this phase's collector composes.
