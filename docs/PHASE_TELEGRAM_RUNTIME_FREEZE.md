# GoldBot Core — Telegram Runtime Activation Alpha — Freeze

Governed by `docs/constitution/CONSTITUTION.md` Article 12
(Architecture Evolution Law). Closes "GoldBot Core Telegram Runtime
Activation Alpha", a direct follow-on to the GitHub Secrets /
Environment Configuration Audit — that audit found secrets were never
the problem; this phase makes the actual, already-correct
`telegram/polling.py` listener observable from inside Telegram itself.

## Audit Summary

TASK 0's audit (`docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`) confirmed:
`telegram/polling.py` is the single, consistent entry point across
every deployment surface; all 49 commands across `COMMANDS`/
`OWNER_COMMANDS`/`ADMIN_COMMANDS` have a matching `{command}_handler`
(verified programmatically, zero missing); `TELEGRAM_OWNER_ID` ->
`telegram.permissions.is_owner()` -> `command_router` gating already
works end-to-end; `deploy/systemd/goldbot-polling.service` and
`docker-compose.yml` were already consistent with each other and with
the entry point. No Director Decision pause was required.

## Built this phase

- `telegram/polling.py` (extended) — `_log_startup_secret_presence()`
  (TASK 6), `_build_startup_message()`/`_notify_owner_startup()`
  (TASK 2), `_heartbeat_loop()` + `HEARTBEAT_INTERVAL_SECONDS` (TASK
  5), all wired into `run_polling()` alongside the existing
  token-check/Bot/Dispatcher setup. The missing-token log line was
  refined to the brief's exact `Startup aborted: Missing
  TELEGRAM_BOT_TOKEN` shape (previously two separate lines from the
  prior audit's own fix).
- `telegram/runtime_monitor.py` (new) — `TelegramRuntimeStatus`
  (`status`/`last_ping`/`errors`/`uptime_seconds`),
  `TelegramRuntimeMonitor` (`record_connected()`/`record_heartbeat()`/
  `record_error()`/`get_status()`), module-level `DEFAULT_RUNTIME_MONITOR`
  singleton + free functions. `record_error()` relays into
  `monitoring.system_monitor.record_error()`.
- `docs/TELEGRAM_RUNTIME.md`, `docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`,
  `docs/PHASE_TELEGRAM_RUNTIME_FREEZE.md` (new documentation);
  `docs/DEPLOYMENT.md`'s Troubleshooting section updated to reference
  the new log line and startup notification.
- `tests/telegram/test_runtime_monitor.py` (new, 22 tests) +
  `tests/telegram/test_polling.py` (extended, 31 new tests) — 53 new
  tests total, exceeding the brief's own 50-test minimum.

## Not built this phase

- No VPS deployment, no systemd/docker-compose file changes — the
  brief's own Strict Rule ("Hozir VPSga o'tmaymiz"). TASK 7 confirmed
  both configs already point at the unchanged entry point; nothing to
  edit.
- No hard abort on `TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/
  `GEMINI_API_KEY` absence — validated and logged (presence/absence
  only) but never blocks startup; see `docs/TELEGRAM_RUNTIME.md`'s
  "Why only one secret gates startup" section for the full reasoning
  behind this divergence from a literal reading of TASK 6.
- No persisted heartbeat/runtime-status history — `TelegramRuntimeStatus`
  is computed live from an in-process singleton, matching
  `monitoring.system_monitor.SystemMonitor`'s own established
  convention (the process itself is long-running, so in-memory state
  persists exactly as long as it's meaningful).
- No change to `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, or any AI-layer module (Strict Rule).
- No change to any existing command's logic, permission tier, or
  response shape — TASK 3 was a re-verification, not a rewrite.

## Constitution Compliance (checks run at close)

- **Isolation** — `telegram/runtime_monitor.py` imports only
  `core_layer.logger.logger`, `monitoring.system_monitor`, and stdlib.
  `telegram/polling.py`'s new code imports only
  `monitoring.system_monitor.get_health` and `telegram.runtime_monitor`
  beyond what already existed. Neither imports `decision`/`risk`/
  `execution`/`ai.*`/`signals`/`strategies`.
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`: no changes in any of those directories this phase.
- **Article 9 (Version Compatibility)** — no existing public
  method/function signature changed. `run_polling()`/`create_dispatcher()`
  keep their existing signatures; the missing-token log wording change
  is a message-text refinement (already covered by this phase's own
  updated test), not a contract change.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  `monitoring.system_monitor.get_health()` and
  `monitoring.system_monitor.record_error()` both already existed and
  are reused outright for the heartbeat's Core/Database check and the
  cross-module error sink, respectively — no duplicate health-check
  writer, no second error-storage path.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | — (no new top-level package) | — | `telegram/`, `monitoring/` (both pre-existing) |
| Modules | `telegram/runtime_monitor.py` (1) | `telegram/polling.py` (1) | `monitoring/system_monitor.py` (composed, not modified) |
| Classes | `TelegramRuntimeMonitor` (1) | — | — |
| Models | `TelegramRuntimeStatus` (1) | — | `monitoring.models.SystemHealth` (read via `get_health()`, not imported directly as a type) |
| Functions | `_log_startup_secret_presence()`, `_build_startup_message()`, `_notify_owner_startup()`, `_heartbeat_loop()`, `record_connected()`, `record_heartbeat()`, `record_error()`, `get_status()` (8) | `run_polling()` (extended in place) | `monitoring.system_monitor.get_health()`, `monitoring.system_monitor.record_error()` |
| Secrets | — | — | `Secrets.TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/`GEMINI_API_KEY` (all unchanged) |
| Tests | 1 new file (22 tests) | 1 file extended (+31 tests) | — |
| Docs | `docs/TELEGRAM_RUNTIME.md`, `docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`, `docs/PHASE_TELEGRAM_RUNTIME_FREEZE.md` (3, new) | `docs/DEPLOYMENT.md` (extended) | — |

Totals: **0 new top-level packages**, **1 new module**, **1 file
extended in place**, **1 new class**, **1 new dataclass model**, **0
changes to any pre-existing public method/field signature**, **53 new
tests**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/` returns no output.

## Next phase recommendation

Per the Director's own stated order: once this phase closes, "GoldBot
Core Alpha Monitoring" begins its 3–5 week real-observation window —
collecting errors, signal quality, API issues, uptime, and real market
conditions — before V1 Freeze fixes. This phase's own
`telegram.runtime_monitor` and the prior phase's `monitoring/`
package are both now live inputs to that window. Not decided here —
requires its own dedicated Worker Brief per this session's Director
Policy.

## Related documents

- `docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md` — TASK 0's Foundation Reuse
  Audit.
- `docs/TELEGRAM_RUNTIME.md` — the full subsystem documentation.
- `docs/DEPLOYMENT.md` — the Troubleshooting section this phase's
  startup notification directly answers.
- `docs/architecture/MONITORING.md` — the GoldBot Core Owner
  Monitoring Alpha layer this phase composes with.
