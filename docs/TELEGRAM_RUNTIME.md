# GoldBot — Telegram Runtime (Activation Alpha)

Governed by `docs/constitution/CONSTITUTION.md`. Documents the
observability layer added on top of `platform_layer/telegram/polling.py`'s existing
long-running listener in the "GoldBot Core Telegram Runtime Activation
Alpha" phase. Full Foundation Reuse Audit:
`docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`. Full freeze:
`docs/PHASE_TELEGRAM_RUNTIME_FREEZE.md`. Builds directly on the prior
GitHub Secrets / Environment Configuration Audit's root-cause finding
(`docs/DEPLOYMENT.md`'s "Troubleshooting" section): secrets were never
the problem — the Owner now gets proof the listener is actually alive
without SSHing in to read logs.

## Why this phase exists

`platform_layer/telegram/polling.py` (`python -m telegram.polling`) already correctly
starts the bot, reads its token, and routes every command — the prior
audit proved this end-to-end. What it didn't have: any signal, from
inside Telegram itself, that the process actually started, and no way
to answer "is polling still alive right now?" short of reading raw
process logs. This phase adds exactly that, without touching what
already works.

## Single entry point

```
python -m telegram.polling
```

The only Telegram runtime entry point, consistent across every
deployment surface (`deploy/systemd/goldbot-polling.service`,
`docker-compose.yml`'s `telegram-polling` service, `Dockerfile`'s own
comment, `docs/DEPLOYMENT.md`). `main.py` remains the separate,
one-shot trading pipeline — the two are never combined.

## What's new

| Area | Where | What |
|---|---|---|
| Secret validation | `platform_layer/telegram/polling.py`'s `_log_startup_secret_presence()` | Logs presence/absence (never the value) of `TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/`GEMINI_API_KEY` at every startup. Only `TELEGRAM_BOT_TOKEN` actually aborts startup (`Startup aborted: Missing TELEGRAM_BOT_TOKEN`) — see "Why only one secret gates startup" below. |
| Startup notification | `platform_layer/telegram/polling.py`'s `_notify_owner_startup()` | Sends a one-time "🟢 GoldBot Online" message to `TELEGRAM_OWNER_ID` once polling actually starts. Silently skipped (not an error) if no owner is configured. Regular users never see this message — it is not a broadcast. |
| Heartbeat | `platform_layer/telegram/polling.py`'s `_heartbeat_loop()` | Every `HEARTBEAT_INTERVAL_SECONDS` (300s / 5 minutes), logs an internal `BOT_HEARTBEAT Telegram=OK Core=<OK/DOWN> Database=<OK/DOWN>` line and records a ping on `platform_layer.telegram.runtime_monitor`. **Never sent to the owner as a Telegram message** — internal log/monitoring only, per the brief's own rule. |
| Runtime status | `platform_layer/telegram/runtime_monitor.py` (new) | `TelegramRuntimeStatus`/`TelegramRuntimeMonitor` — tracks the Bot/Dispatcher connection's own `status`/`last_ping`/`errors`/`uptime_seconds`. In-memory only (module-level `DEFAULT_RUNTIME_MONITOR` singleton), mirrors `core_layer.health_monitor.system_monitor.SystemMonitor`'s own convention. |

## Why only one secret gates startup

The brief asks to validate all four secrets at startup and abort with
`Startup aborted: Missing SECRET_NAME` if any is missing. Read
literally, that would mean a Telegram bot with a perfectly valid
`TELEGRAM_BOT_TOKEN` refuses to start just because `GEMINI_API_KEY`
(an AI-layer secret) or `TWELVE_DATA_API_KEY` (a market-data secret)
happens to be unset — `platform_layer/telegram/polling.py` never reads either one
directly, and an Owner who hasn't configured AI/market-data yet would
be locked out of `/start` entirely for an unrelated reason. Instead:
all four are validated and logged (presence/absence, never the value)
for startup visibility, but only `TELEGRAM_BOT_TOKEN` — the one
secret this module actually needs to construct its `Bot` — aborts
startup. `TELEGRAM_OWNER_ID` already has its own fail-closed default
(`""`, "nobody is OWNER") in `platform_layer.telegram.permissions`, so it correctly
degrades rather than blocking the listener too. See
`docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`'s #2 for the full reasoning.

## Startup notification format

```
🟢 GoldBot Online
Status:
Core: Running
Telegram: Connected
Monitoring: Active
Time:
2026-07-20 18:00
```

Sent once, to `TELEGRAM_OWNER_ID` only, immediately before
`dispatcher.start_polling()` blocks. A send failure (network issue,
owner blocked the bot, etc.) is caught, logged, and relayed into
`platform_layer.telegram.runtime_monitor.record_error()` — it never prevents polling
from starting.

## Runtime status model

```python
@dataclass(frozen=True)
class TelegramRuntimeStatus:
    status: str              # "CONNECTED" | "DISCONNECTED"
    last_ping: Optional[str] # ISO 8601 timestamp of the last heartbeat, or None
    errors: int              # cumulative error count this process lifetime
    uptime_seconds: float    # time since this process's TelegramRuntimeMonitor was created
```

Field name is `uptime_seconds`, not the brief's own literal `uptime` —
matching every comparable model in this codebase
(`core_layer.health_monitor.models.SystemHealth.uptime_seconds`,
`core_layer.health_monitor.models.MarketHealth`) rather than introducing a
one-off different name for the same concept.

`platform_layer.telegram.runtime_monitor.record_error()` also relays into
`core_layer.health_monitor.system_monitor.record_error()` (the same
"relay into the shared sink" pattern
`core_layer.health_monitor.error_monitor.ErrorMonitor.capture()` already
established in the prior GoldBot Core Owner Monitoring Alpha phase),
so a Telegram-runtime error also surfaces in `/owner_status`'s
`last_error` field without a second, duplicate storage path.

## Heartbeat

Runs alongside `dispatcher.start_polling()` as a background
`asyncio.Task`, cancelled cleanly in `run_polling()`'s `finally` block
on shutdown. Each tick:

1. Calls `core_layer.health_monitor.system_monitor.get_health()` (reused outright,
   not duplicated) to derive `Core`/`Database` status.
2. Records a heartbeat timestamp on `platform_layer.telegram.runtime_monitor`.
3. Logs `BOT_HEARTBEAT Telegram=OK Core=<OK/DOWN> Database=<OK/DOWN>`
   at INFO level — internal only, never a Telegram message.

A health-check failure inside the loop is caught, logged, and relayed
into `platform_layer.telegram.runtime_monitor.record_error()` — the loop itself never
dies from one bad tick.

## Owner commands (unchanged, re-verified this phase)

`/start`, `/owner_status`, `/health`, `/signals`, `/errors`,
`/pipeline`, `/report` — all re-verified end-to-end via
`command_router.route_command()` with this phase's new runtime code in
place: OWNER gets real data, USER gets `Permission denied.` for every
OWNER-only command, `/start` remains open to any user. No command
logic changed this phase.

## Deployment readiness (not deployed this phase)

`deploy/systemd/goldbot-polling.service` (`ExecStart=... -m
telegram.polling`, `Restart=always`, `RestartSec=5`,
`OnFailure=goldbot-notify-failure@%n.service`) and
`docker-compose.yml`'s `telegram-polling` service (`command: python -m
telegram.polling`, `restart: unless-stopped`) both already point at
the same, unchanged entry point this phase's new code lives inside —
no config change was needed or made. Per the brief's own Strict Rule
("Hozir VPSga o'tmaymiz"), neither is invoked this phase; this section
documents readiness only.

## Dependency rules

`platform_layer/telegram/runtime_monitor.py` imports only `core_layer.logger.logger`,
`core_layer.health_monitor.system_monitor` (the established cross-module error sink),
and stdlib — never `decision`/`risk`/`execution`/`ai.*`/`signals`/
`strategies`. `platform_layer/telegram/polling.py`'s new code adds one import
(`core_layer.health_monitor.system_monitor.get_health`) alongside its existing
`platform_layer.telegram.runtime_monitor` import — same isolation boundary every
other `platform_layer/telegram/owner/*.py` monitoring integration already respects.

## Related documents

- `docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md` — this phase's Foundation
  Reuse Audit.
- `docs/PHASE_TELEGRAM_RUNTIME_FREEZE.md` — this phase's freeze.
- `docs/architecture/MONITORING.md` — the wider Core Owner Monitoring
  layer `platform_layer.telegram.runtime_monitor` composes with.
- `docs/DEPLOYMENT.md` — the "Troubleshooting" section this phase's
  startup notification directly answers.
