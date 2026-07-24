# GoldBot Core — Telegram Runtime Activation Alpha — Foundation Audit

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). TASK 0 of the "Telegram Runtime Activation Alpha" brief --
this phase's goal is making the long-running Telegram listener
observable and startup-safe, not changing what it already does.
Builds directly on the prior GitHub Secrets / Environment
Configuration Audit, whose root-cause finding (`docs/DEPLOYMENT.md`'s
"Troubleshooting" section) this phase acts on: secrets are correct,
`telegram/polling.py` just needs to actually run somewhere, and once
it does, the Owner needs proof of that without SSHing in to read
`journalctl`.

## 1. Which file does the Telegram runtime start from?

**`telegram/polling.py`**, module-level `main()` (`asyncio.run(run_polling())`),
invoked as `python -m telegram.polling`. Confirmed as the single,
consistent entry point across every deployment surface:

| Surface | Command |
|---|---|
| `deploy/systemd/goldbot-polling.service` | `ExecStart=/opt/goldbot/venv/bin/python -m telegram.polling` |
| `docker-compose.yml`'s `telegram-polling` service | `command: python -m telegram.polling` |
| `docs/DEPLOYMENT.md`'s "Run" section | `python -m telegram.polling` |
| `Dockerfile`'s own header comment | `docker run --env-file .env goldbot python -m telegram.polling` |

No second, competing entry point exists anywhere (`main.py` is the
separate, one-shot trading pipeline -- see `docs/ARCHITECTURE.md`'s
System Overview; it never imports `telegram.polling`).

`run_polling()`'s existing shape: read `TELEGRAM_BOT_TOKEN` ->
construct an aiogram `Bot` -> `create_dispatcher()` (wires
`command_router.route_message()`/`route_contact()`) ->
`dispatcher.start_polling(bot)` (blocks forever) -> `bot.session.close()`
on exit. TASK 1/2/5/6 below extend this function; TASK 4 adds a new,
separate module it calls into.

## 2. Where does the environment variable come from?

`core.secrets.Secrets` — the sole `os.environ` read point repo-wide
(confirmed by the prior audit's `docs/DEPLOYMENT.md` section and this
codebase's own `docs/SECURITY.md`). `telegram/polling.py` reads
exactly one secret directly: `Secrets().TELEGRAM_BOT_TOKEN` (line 88).
No `.env`/`load_dotenv()` anywhere — plain `os.environ`, populated
identically by a local shell export, systemd's `EnvironmentFile=`, a
container's `--env-file`, or (for `main.py`/CI only) GitHub Actions'
`env:` block.

`TELEGRAM_OWNER_ID`, `TWELVE_DATA_API_KEY`, and `GEMINI_API_KEY` are
**not** currently read anywhere in `telegram/polling.py` itself --
`TELEGRAM_OWNER_ID` is read downstream, inside `telegram.permissions`
(see #3 below), and the other two are trading-pipeline/AI-layer
secrets `telegram/polling.py` has never needed. TASK 6 below adds an
explicit startup validation pass that checks all four (per the
brief), while being honest in its own docstring about which one is
actually load-bearing for polling to function.

## 3. Does OWNER_ID work?

Yes, already verified end-to-end in the prior audit's smoke test and
unchanged since. Chain: `core.secrets.Secrets.TELEGRAM_OWNER_ID`
(defaults to `""`, fail-closed) -> `telegram.permissions.is_owner(user_id)`
(`str(user_id) == owner_id`, `bool(owner_id)` guard) ->
`get_permission_level()` -> `telegram.command_router._required_level()`
gates every command in `OWNER_COMMANDS` (never `ADMIN_COMMANDS`-only
membership) to `PermissionLevel.OWNER`. No separate `OWNER_ID`/
`OWNER_IDS` name exists anywhere -- one canonical name,
`TELEGRAM_OWNER_ID`, read in exactly one place (`Secrets`).

## 4. Is handler registration complete?

Yes -- verified programmatically, not just by inspection:

```python
all_commands = {**COMMANDS, **OWNER_COMMANDS, **ADMIN_COMMANDS}  # 49 unique names
missing = [c for c in all_commands if not hasattr(handlers, f"{c}_handler")]
# missing == []
```

Every one of the 49 command names across `telegram.commands.COMMANDS`/
`OWNER_COMMANDS`/`ADMIN_COMMANDS` has a matching `{command}_handler`
in `telegram/handlers.py`, which `command_router.route_command()`
resolves via `getattr(handlers, f"{command}_handler", None)`. No
orphaned command, no missing handler.

`telegram/polling.py`'s `create_dispatcher()` registers exactly one
aiogram message handler (a catch-all `@dispatcher.message()`), which
delegates every text/contact update to `command_router.route_message()`/
`route_contact()` -- there is no per-command aiogram registration to
audit separately; the router (not the Dispatcher) is where the
49-command mapping lives.

## 5. Reviewed: `deploy/`, `docker-compose.yml`, systemd unit

`deploy/systemd/goldbot-polling.service`: `Type=simple`,
`Restart=always`, `RestartSec=5`, `OnFailure=goldbot-notify-failure@%n.service`,
`ExecStart=... -m telegram.polling`, `EnvironmentFile=/opt/goldbot/.env.production`.
Already production-shaped (crash recovery + failure alerting exist).
Not touched this phase (Strict Rule: "Hozir VPSga o'tmaymiz").

`docker-compose.yml`'s `telegram-polling` service: `restart: unless-stopped`,
`command: python -m telegram.polling`, `env_file: .env`, shares the
`goldbot-db` named volume with `trading-pipeline`. Consistent with the
systemd unit's entry point. Not touched this phase.

Both are confirmed consistent and ready (TASK 7); this phase's new
code (TASK 2/4/5/6) works unmodified under either, since neither
config does anything `telegram/polling.py` doesn't already assume
(plain env vars, `python -m telegram.polling` as the process).

## 6. Reuse decisions for this phase's new work

- **TASK 2 (owner startup notification)** and **TASK 6 (secret
  validation)** extend `telegram/polling.py`'s existing `run_polling()`
  in place -- no new file, no new entry point.
- **TASK 4/5 (runtime status model + heartbeat)**: no existing module
  tracks "is the aiogram Bot/Dispatcher connection itself alive" --
  `monitoring.system_monitor.SystemMonitor` (Core Owner Monitoring
  Alpha, previous phase) tracks trading-pipeline uptime/last_scan/
  last_error via `AdminService`/provider registry, a different
  concern. A new, small `telegram/runtime_monitor.py` is added
  (inside the already-existing `telegram/` package -- no new
  top-level package), and it reuses
  `monitoring.system_monitor.record_error()` as its cross-module error
  sink (same "relay into the shared sink" pattern
  `monitoring.error_monitor.ErrorMonitor.capture()` already
  established), so a Telegram-runtime error also shows up in
  `/owner_status`'s `last_error` field without duplicating storage.
- No new database table: `TelegramRuntimeStatus` (TASK 4) is computed
  live from an in-process singleton, mirroring
  `monitoring.system_monitor.SystemMonitor`'s own `DEFAULT_MONITOR`
  module-level-singleton-in-a-long-running-process convention --
  `telegram/polling.py` is itself the long-running process, so
  in-memory state naturally persists exactly as long as it's
  meaningful (a fresh process restart is a legitimate "runtime reset").

## Constitution / Strict Rule compliance confirmed before implementation

`grep`-audited: `telegram/polling.py`, `telegram/bot.py`,
`telegram/handlers.py`, `telegram/commands.py`, and the new
`telegram/runtime_monitor.py` this phase adds -- none import
`decision`, `risk`, `execution`, or any `ai.*` module. `main.py` and
`core/pipeline.py` (Trading Core) are not touched by this phase at
all. No signal/strategy logic is read or written anywhere in this
audit's scope.
