# GoldBot Core Owner Snapshot Reporter Alpha — Foundation Reuse Audit

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). TASK 0 of the Owner Snapshot Reporter brief. This phase
adds a GitHub-Actions-driven, one-shot alternative to the Telegram
Runtime's live heartbeat (`docs/TELEGRAM_RUNTIME.md`) — useful
precisely because the Telegram Runtime's own heartbeat/startup
notification only fire once `telegram.polling` is actually deployed
on a VPS (not yet true, per `docs/PHASE_BRANCH_SYNC_AUDIT.md`'s own
finding), whereas GitHub Actions is already running today
(`trading_bot.yml`, `ci.yml`).

## Reviewed: `monitoring/`

- `monitoring/system_monitor.py` — `get_health()` returns
  `SystemHealth` (`status`, `uptime_seconds`, `data_connection`,
  `database_status`, `last_scan`, `last_error`). **Reused outright**
  for `core_status`/`database_status`/`error_count`(via `last_error`
  presence)/`uptime_info` in the new collector — no duplicate health
  check written.
- `monitoring/signal_monitor.py` — `get_signal_health()` returns
  `SignalHealth` (`total_signals`, `buy_count`, `sell_count`,
  `none_count`, `average_confidence`). **Reused outright** for
  "Signals Today" count.
- `monitoring/market_monitor.py` — `get_market_health()` returns
  `MarketHealth` (`data_source_status`, ...), composing
  `monitoring.provider_health.check_provider_health()`. **Reused
  outright** for `market_data_status`.
- `monitoring/error_monitor.py` — `ErrorMonitor.get_error_counts(hours=24)`
  returns `Dict[str, int]`. **Reused outright**; `sum(counts.values())`
  gives `error_count`, matching `telegram/owner/monitoring_commands.py`'s
  own `get_daily_report()` precedent exactly.
- `monitoring/decision_logger.py` — reviewed, not needed here (no
  decision-trace field in `OwnerSnapshot`).
- **No existing module produces a single, structured "everything in
  one snapshot" object** — `telegram/owner/monitoring_commands.py`'s
  `get_daily_report()` comes closest but returns pre-formatted free
  text (a `ProviderCommandResult`), not a reusable data model. This is
  the genuine gap `monitoring/snapshot_models.py`/`snapshot_collector.py`
  fill — composition of existing sources, not new health logic (TASK
  2's own constraint).

## Reviewed: `telegram/`

- `telegram/bot.py` — `TelegramBot` (wraps aiogram `Bot`,
  `async send_message(text, chat_id)`, token from `core.secrets.Secrets`,
  never crashes on missing/invalid token). **Reused outright** as the
  sender in TASK 4 — no new Telegram client written.
- `telegram/permissions.py` — `is_owner()`, sourced from
  `Secrets.TELEGRAM_OWNER_ID`. **Reused outright**: TASK 4 sends only
  to the configured owner chat_id, the same identity source every
  other Owner-only path in this codebase uses.
- `telegram/owner/monitoring_commands.py` — reviewed in full; its
  `get_daily_report()` independently re-derives a very similar
  composition (system + signals + errors) but is Telegram-command-shaped
  (returns `ProviderCommandResult`, invoked interactively via
  `/report`). Not reusable as-is for a GitHub Actions one-shot script,
  but confirms the same underlying sources are already proven
  sufficient for a "daily digest"-shaped message — no new aggregation
  concept being invented.

## Reviewed: `core/`

- `core/secrets.py` — `Secrets.TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`/
  `TWELVE_DATA_API_KEY`/`GEMINI_API_KEY` all already exist with the
  exact names TASK 7 asks to verify. **Reused outright**, not
  modified.
- `core/logger.py` — `setup_logger()`. **Reused outright** for TASK 7's
  clear-failure-reason logging.
- `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/` — **not imported anywhere in this phase**
  (Strict Rule).

## Reviewed: `database/`

- `database/signal_repository.py`'s `get_latest_signal()` **already
  exists** (`SELECT * FROM signals ORDER BY created_at DESC, id DESC
  LIMIT 1`) — reused outright for `OwnerSnapshot.last_signal`, no new
  query written.
- `database/monitoring_repository.py` — `MonitoringRepository`
  (`get_recent_errors()`, `get_recent_decision_entries()`), reviewed;
  `ErrorMonitor.get_error_counts()` already wraps the error side of
  this repository, so the collector goes through `ErrorMonitor`, not
  `MonitoringRepository` directly (one less layer to duplicate).
- No schema change of any kind this phase (Strict Rule) — every read
  above uses an existing table/method.

## Reviewed: `configuration/`

- `configuration/feature_flags.py`/`feature_registry.py` reviewed —
  no snapshot/reporter-shaped flag exists; none needed (this phase's
  entry point is invoked directly by its own dedicated workflow, not
  gated by a runtime feature toggle, matching `main.py`'s own
  ungated-by-`configuration/` precedent).

## Reviewed: `.github/workflows/`

- `ci.yml` — validation-only, never touched.
- `trading_bot.yml` — the direct structural template this phase's new
  `owner_snapshot.yml` follows (checkout → setup-python → install
  requirements → run script, secrets via `env:`), same `ref:
  claude/code-analysis-optimization-pwfo3q` pin (per
  `docs/PHASE_BRANCH_SYNC_AUDIT.md`'s finding that this branch is the
  production branch).

## Decisions carried into TASK 1-7

1. **No duplicate monitoring** — every field in `OwnerSnapshot` is
   sourced from an existing `monitoring/*` function; `snapshot_collector.py`
   is pure aggregation (TASK 2's own constraint).
2. **No new Telegram client** — `snapshot_sender.py` constructs and
   uses `telegram.bot.TelegramBot`, the same outbound bot `main.py`'s
   pipeline already uses.
3. **`telegram_status` is honestly scoped** — it reflects whether
   *this run's own* `TelegramBot` construction/send succeeded, not
   whether the separate, long-running `telegram.polling` listener is
   up (a different process this script cannot observe). Documented in
   `docs/OWNER_SNAPSHOT_REPORTER.md` to avoid the field being
   misread as a polling-liveness check.
4. **`uptime_info` is honestly scoped** — `monitoring.system_monitor.SystemMonitor`'s
   uptime is in-memory, per-process. A GitHub Actions run is a fresh
   process every 15 minutes, so this field will read a few seconds
   every run, not continuous Core uptime. Documented as a known Alpha
   limitation (this phase's own header: "Bu VPS 24/7 runtime o'rnini
   bosmaydi") rather than fabricated with fake persistent state.
5. **`last_signal` reuses `SignalRepository.get_latest_signal()`**
   verbatim — already exists, no new query.
