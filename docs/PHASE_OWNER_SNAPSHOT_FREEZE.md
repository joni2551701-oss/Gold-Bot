# GoldBot Core Owner Snapshot Reporter Alpha — Freeze

Governed by `docs/constitution/CONSTITUTION.md` Article 12
(Architecture Evolution Law). Closes "GoldBot Core Owner Snapshot
Reporter Alpha" — a temporary, GitHub-Actions-driven monitoring layer
that delivers Owner Telegram snapshots every 15 minutes ahead of a
real VPS 24/7 deployment.

## Audit Summary

TASK 0's audit (`docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`) confirmed every
health source already exists (`monitoring.system_monitor.get_health()`,
`monitoring.market_monitor.get_market_health()`,
`monitoring.signal_monitor.get_signal_health()`,
`monitoring.error_monitor.ErrorMonitor`,
`database.signal_repository.SignalRepository.get_latest_signal()`) and
the outbound Telegram sender already exists
(`telegram.bot.TelegramBot`). This phase is pure composition — no
health-check logic duplicated, no new Telegram client written. No
Director Decision pause was required.

## Built this phase

- `monitoring/snapshot_models.py` (new) — `OwnerSnapshot`, primitive
  fields only, plus one additive `signals_today` field (LOCK Policy
  explicitly permits new fields).
- `monitoring/snapshot_collector.py` (new) — `collect_snapshot()`,
  pure aggregation of five existing sources, defensive per-field
  degradation (never raises).
- `telegram/owner/snapshot_formatter.py` (new) — `format_snapshot()`,
  pure text formatting, status-to-icon mapping.
- `telegram/owner/snapshot_sender.py` (new) — `send_snapshot()`,
  reuses `telegram.bot.TelegramBot`, sends only to
  `TELEGRAM_OWNER_ID`, never logs the token or the owner id.
- `monitoring/run_snapshot.py` (new) — one-shot entry point
  (`python -m monitoring.run_snapshot`): verify secrets → collect →
  format → send → exit. No infinite loop.
- `.github/workflows/owner_snapshot.yml` (new) — `cron: "*/15 * * *
  *"` + `workflow_dispatch`, own concurrency group, same
  production-branch pin as `trading_bot.yml`.
- `docs/OWNER_SNAPSHOT_REPORTER.md`, `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`,
  `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md` (new documentation);
  `docs/DEPLOYMENT.md` and `docs/architecture/MONITORING.md` extended.
- `tests/monitoring/test_snapshot_models.py`,
  `tests/monitoring/test_snapshot_collector.py`,
  `tests/telegram/owner/test_snapshot_formatter.py`,
  `tests/telegram/owner/test_snapshot_sender.py`,
  `tests/monitoring/test_run_snapshot.py`,
  `tests/workflows/test_owner_snapshot_workflow.py` (new, 89 tests
  total) — exceeding the brief's own 50-test minimum. New
  `tests/workflows/` directory (no workflow-file test coverage
  existed before this phase).

## Not built this phase

- No VPS deployment, no change to `telegram/polling.py` or
  `deploy/systemd/` (Strict Rule: "Telegram pollingga bog'lash"
  forbidden — this reporter is fully independent of the polling
  listener).
- No new database table or schema change — every read goes through an
  existing repository method.
- No AI/LLM call of any kind (Strict Rule).
- No change to `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/` (Strict Rule).
- No persisted snapshot history — `OwnerSnapshot` is computed fresh
  on every one-shot run, matching every comparable monitoring function
  in this codebase's own convention.

## Constitution Compliance (checks run at close)

- **Isolation** — `monitoring/snapshot_*.py` and
  `telegram/owner/snapshot_*.py` import only `monitoring.*`,
  `database.signal_repository`, `telegram.bot`, `core.secrets`,
  `core.logger`, `config`, and stdlib. No `decision`/`risk`/
  `execution`/`ai.*`/`signals`/`strategies` import anywhere.
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`: no changes in any of those directories this phase.
- **Article 9 (Version Compatibility)** — no existing public
  function/class signature changed anywhere; `trading_bot.yml` and
  `ci.yml` are untouched.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  every health/aggregation source and the outbound Telegram sender
  already existed and are reused outright; the only genuinely new
  code is the composition/formatting/entry-point layer itself.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | — (no new top-level package) | — | `monitoring/`, `telegram/owner/` (both pre-existing) |
| Modules | `monitoring/snapshot_models.py`, `snapshot_collector.py`, `run_snapshot.py`, `telegram/owner/snapshot_formatter.py`, `snapshot_sender.py` (5) | — | `monitoring/system_monitor.py`, `market_monitor.py`, `signal_monitor.py`, `error_monitor.py`, `telegram/bot.py`, `database/signal_repository.py` (all composed, not modified) |
| Models | `OwnerSnapshot`, `SnapshotSendResult` (2) | — | `SystemHealth`, `MarketHealth`, `SignalHealth` (read via function calls, not imported as types) |
| Functions | `collect_snapshot()`, `format_snapshot()`, `send_snapshot()`, `run_snapshot_report()`, `main()`, plus private helpers (~10) | — | `get_health()`, `get_market_health()`, `get_signal_health()`, `ErrorMonitor.get_error_counts()`, `SignalRepository.get_latest_signal()` |
| Workflows | `.github/workflows/owner_snapshot.yml` (1) | — | `trading_bot.yml`'s own structural template (checkout/setup-python/install/run) |
| Secrets | — | — | `Secrets.TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/`GEMINI_API_KEY` (all unchanged) |
| Tests | 6 new files, 89 new tests | — | — |
| Docs | `docs/OWNER_SNAPSHOT_REPORTER.md`, `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`, `docs/PHASE_OWNER_SNAPSHOT_FREEZE.md` (3) | `docs/DEPLOYMENT.md`, `docs/architecture/MONITORING.md` (2) | — |

Totals: **0 new top-level packages**, **5 new modules** (inside
already-existing `monitoring/`/`telegram/owner/`), **1 new GitHub
Actions workflow**, **2 new dataclasses**, **0 changes to any
pre-existing public method/field signature**, **89 new tests**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/` returns no output.

## LOCK Policy (in force from this freeze onward)

`monitoring/snapshot_*` and `telegram/owner/snapshot_*`:

- **Permitted**: new snapshot fields, new report formats, new
  monitoring metrics feeding the collector.
- **Forbidden**: rename, move, breaking API change, or any Core
  dependency added to these modules.

## Next phase recommendation

Per the Director's own stated order: this Alpha reporter runs
alongside the still-pending VPS deployment of `telegram.polling`,
feeding the same 3–5 week pre-V1 observation window
`docs/PHASE_CORE_MONITORING_FREEZE.md` and
`docs/PHASE_TELEGRAM_RUNTIME_FREEZE.md` already established. Not
decided here — requires its own dedicated Worker Brief per this
session's Director Policy.

## Related documents

- `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md` — TASK 0's Foundation Reuse
  Audit.
- `docs/OWNER_SNAPSHOT_REPORTER.md` — the full subsystem
  documentation.
- `docs/TELEGRAM_RUNTIME.md` — the live-runtime layer this phase
  substitutes for until a VPS exists.
- `docs/architecture/MONITORING.md` — the wider Core Owner Monitoring
  layer this phase's collector composes.
