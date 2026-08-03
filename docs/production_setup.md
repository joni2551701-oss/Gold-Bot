# GoldBot Production Setup (Phase 58)

This document covers what `docs/DEPLOYMENT.md` (Phase 56) does not:
the specific artifacts needed to run GoldBot unattended on a real VPS
— process supervision, crash recovery, log persistence, and a
monitoring foundation. `docs/DEPLOYMENT.md` remains the general
Install/Configure/Run/Restart/Backup reference; this document is the
VPS-specific operational layer on top of it. No trading logic,
architecture, or code behavior changes were made to produce this
document — every artifact it describes is new, additive tooling
(`scripts/`, `deploy/systemd/`, `.env.production`).

## 1. Deployment

### VPS requirements
- **Python 3.11** — same version pinned in `.github/workflows/ci.yml`
  and `trading_bot.yml`; not tested against other versions.
- **Disk**: minimal. The application code plus a `venv` is a few
  hundred MB; `database/goldbot.db` (SQLite) grows slowly (one row per
  signal/user/feedback event) — a few GB of headroom is generous, not
  a hard requirement.
- **Memory**: no benchmark suggests more than a few hundred MB RSS per
  process (`docs/PERFORMANCE.md`); no GPU or special hardware needed.
- **Network**: outbound HTTPS to `api.telegram.org` and Twelve Data's
  API; inbound nothing (polling is outbound-initiated, not a webhook
  — see Section 5).
- **A non-root service user** is recommended (e.g. `goldbot`) that
  owns `/opt/goldbot` and nothing else on the box.

### Python version
Verify before installing:
```bash
python3.11 --version
```
If unavailable, install via your distro's package manager or
`pyenv` — out of scope for this document beyond noting the
requirement.

### Environment variables
See Section 3 (`.env.production`) for the full list. The three
always-required ones are `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
`TWELVE_DATA_API_KEY` — `core/secrets.py` raises `ValueError` at first
use if any of these is missing (fails loud, not silently).

### Folder structure
Recommended VPS layout (paths the systemd units in Section 2 assume;
adjust both together if you deploy elsewhere):

```
/opt/
├── venv/                     # Python 3.11 virtualenv
├── database/
│   └── goldbot.db             # created automatically on first run
├── scripts/
│   ├── health_check.py        # Phase 58
│   └── notify_failure.sh      # Phase 58
├── .env.production             # real secrets, chmod 600, gitignored on the VPS
└── ... (the rest of the repository, unchanged)
```

`deploy/systemd/*.service`/`*.timer` are installed to
`/etc/systemd/system/`, not left inside `/opt/goldbot` (systemd does
not read unit files from an arbitrary application directory by
default).

## 2. Process management

Two processes need supervision (`docs/ARCHITECTURE.md`'s System
Overview): the long-running Telegram polling listener and the trading
pipeline (one-shot, needs a scheduler if not using GitHub Actions).

### Option A: systemd (chosen for this phase)
**Why**: no daemon dependency, ships with every mainstream Linux VPS
distro, and this project's own Docker artifacts (`Dockerfile`,
`docker-compose.yml`, Phase 56) have never been build-tested end to
end in this project's history (`docs/v0.3_stabilization_report.md`,
Phase 57) — systemd is the lower-risk default for a first real VPS
deploy. Docker remains available as Option B below for anyone who
has already verified it builds in their own environment.

New unit files, `deploy/systemd/`:

| File | Type | Purpose |
|---|---|---|
| `goldbot-polling.service` | simple, `Restart=always` | Long-running `telegram/polling.py`. Crash → systemd restarts it after 5s. |
| `goldbot-pipeline.service` | oneshot | Runs `main.py` once. |
| `goldbot-pipeline.timer` | timer | Fires `goldbot-pipeline.service` every 5 minutes (mirrors `trading_bot.yml`'s cadence). Use this **or** GitHub Actions, not both against the same database, to avoid overlapping cycles. |
| `goldbot-healthcheck.service` | oneshot | Runs `scripts/health_check.py`. |
| `goldbot-healthcheck.timer` | timer | Fires the health check every 10 minutes. |
| `goldbot-notify-failure@.service` | oneshot, templated | Fired automatically by the four units above via `OnFailure=` — sends a Telegram alert to `TELEGRAM_OWNER_ID` naming which unit failed. |

Install:
```bash
sudo cp deploy/systemd/*.service deploy/systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now goldbot-polling.service
sudo systemctl enable --now goldbot-pipeline.timer      # only if not using GitHub Actions
sudo systemctl enable --now goldbot-healthcheck.timer
```

**Auto restart**: `Restart=always` + `RestartSec=5` on
`goldbot-polling.service` — a crash (unhandled exception escaping
`run_polling()`, OOM-kill, etc.) restarts the listener within 5
seconds.

**Crash recovery**: the pipeline is inherently self-healing —
`goldbot-pipeline.service` is one-shot and stateless between runs
(`core/pipeline.py`'s cycle reads fresh market data every time), so a
failed cycle simply tries again on the next timer tick 5 minutes
later; nothing needs to be "recovered."

**Log persistence**: `StandardOutput=journal` /
`StandardError=journal` route every process's stdout/stderr (the only
output `core_layer/logger/logger.py` produces today — see `logs/README.md`) into
`journald`, which persists across reboots as long as
`/var/log/journal/` exists (`sudo mkdir -p /var/log/journal &&
sudo systemctl restart systemd-journald` if it doesn't already, on a
fresh VPS). This satisfies "log persistence" without any change to
`core_layer/logger/logger.py` — exactly the path `logs/README.md` already
anticipated ("wherever its host process manager already captures
stdout"). View logs with:
```bash
journalctl -u goldbot-polling.service -f
journalctl -u goldbot-pipeline.service --since today
```

### Option B: Docker Compose (already exists, alternative)
`Dockerfile`/`docker-compose.yml` from Phase 56 remain valid and
untouched. `docker-compose.yml` already gives `restart:
unless-stopped` (auto restart / crash recovery for
`telegram-polling`) and a named volume (`goldbot-db`) for database
persistence. It does **not** yet give the Telegram crash-alert or
health-check foundation this phase adds for Option A — that would be
a natural, separate follow-up (e.g. a `healthcheck:` block plus a
sidecar) if Docker becomes the chosen path, out of scope here since
this phase's Docker verification is still limited to
`docker compose config` (see `docs/v0.3_stabilization_report.md`) —
no daemon has built or run it end to end in this project's history.

## 3. Environment — `.env.production`

New file: `.env.production` (repository root, tracked in git — not
gitignored, exactly like `.env.example`, because it contains **no
real secret values**, only variable names and explanatory comments).
Copy it to the VPS as a real, `chmod 600`, gitignored file and fill in
actual values there — never commit real values anywhere.

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_OWNER_ID=
TWELVE_DATA_API_KEY=
GEMINI_API_KEY=
APP_ENV=production
DEBUG=False
```

Note: the Phase 58 brief names four variables
(`TELEGRAM_BOT_TOKEN`/`TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/
`GEMINI_API_KEY`); `TELEGRAM_CHAT_ID` is included in addition because
`core/secrets.py`'s `TELEGRAM_CHAT_ID` property has no default and
`main.py`'s scheduled broadcast cannot run without it — leaving it out
would make this template incomplete for an actual production
deployment. `.env.production`'s own header explains this.

## 4. Database

- **Location**: `database/goldbot.db`, path from
  `config.Config.DB_PATH` (`BASE_DIR/database/goldbot.db`, where
  `BASE_DIR` is the repository root at runtime — see `config.py`).
  Unchanged from `docs/DEPLOYMENT.md`.
- **Migration startup**: `database_layer.database_manager.database.Database.init_db()` calls
  `database_layer.database_manager.models.init_schema()` (and each repository's own
  `init_*_schema()`) on construction — idempotent `CREATE TABLE IF NOT
  EXISTS` / `CREATE INDEX IF NOT EXISTS` / `PRAGMA table_info()`-guarded
  `ALTER TABLE`, confirmed by reading `database_layer/database_manager/models.py` this phase.
  Nothing to run manually; the schema is always current on process
  start. `database/migrations/README.md` documents the (still unused)
  foundation for a future versioned-migration script, unchanged this
  phase.
- **Backup strategy**: unchanged from `docs/DEPLOYMENT.md`'s Backup
  section — a plain file copy (safe when polling can be paused
  briefly) or `sqlite3 goldbot.db ".backup ..."` (online-safe, no
  pause needed). For unattended VPS backups, a simple daily cron
  entry is enough given the file's small size and low write volume:
  ```
  0 3 * * * sqlite3 /opt/database/goldbot.db ".backup /opt/goldbot/backups/goldbot-$(date +\%Y\%m\%d).db"
  ```
  (create `/opt/goldbot/backups/` and prune old files with your own
  retention policy — no retention tooling exists in this codebase, and
  none is added by this phase.)

## 5. Telegram

- **Polling, not webhook.** Confirmed by reading
  `telegram/polling.py` this phase: `run_polling()` calls aiogram's
  `dispatcher.start_polling(bot)`, which long-polls
  `api.telegram.org` — there is no `set_webhook()` call anywhere in
  the codebase, and no inbound HTTP listener/port to open on the VPS.
  This means no reverse proxy, TLS certificate, or firewall inbound
  rule is needed for Telegram itself.
- **Permissions**: three tiers (`telegram/permissions.py`) — OWNER
  (from `TELEGRAM_OWNER_ID`, fail-closed if unset), ADMIN (from the
  `admins` database table via `AdminService`), USER (everyone else).
  Unchanged this phase; re-confirmed by reading the module.
- **Admin/owner account setup** (production checklist):
  1. Create the bot via `@BotFather`, obtain `TELEGRAM_BOT_TOKEN`.
  2. Send the bot a message from the intended owner's Telegram
     account, then read your own `user_id` (e.g. via `@userinfobot`
     or the bot's own `/start` handler echoing `from_user.id` in logs)
     — set that value as `TELEGRAM_OWNER_ID`.
  3. Determine `TELEGRAM_CHAT_ID` — the destination for
     `main.py`'s scheduled signal broadcast (a channel, group, or the
     owner's own DM `chat_id`, depending on how GoldBot is meant to be
     used).
  4. Additional admins are granted via the `admins` table at runtime
     (an OWNER-only Telegram command, per `telegram/admin_service.py`)
     — not via environment variables.

## 6. Monitoring foundation

Three new, additive artifacts — foundation-level, not a full
observability stack:

- **Health check** — `scripts/health_check.py`: verifies config
  loads, the three required secrets are present (never prints their
  values), and the database is reachable (`SELECT 1`). Exit 0
  healthy, exit 1 otherwise. Run manually (`python
  scripts/health_check.py`) or on a schedule via
  `goldbot-healthcheck.timer` (Section 2).
- **Error alert / crash notification** — `scripts/notify_failure.sh`
  + `deploy/systemd/goldbot-notify-failure@.service`: any of the
  three scheduled units (`goldbot-polling`, `goldbot-pipeline`,
  `goldbot-healthcheck`) failing triggers `OnFailure=`, which runs
  this script and sends a plain-text Telegram message to
  `TELEGRAM_OWNER_ID` naming the failed unit, the host, and the UTC
  timestamp. Deliberately implemented in bash calling the Telegram
  Bot API directly via `curl` — not through `telegram/` — so a
  Python-level crash cannot also silently break the alert path. The
  script never fails the calling unit (exits 0 even if the alert
  itself can't be sent, logging to stderr instead), to avoid a
  failure-notification loop.
- **What this is not**: no metrics/dashboards, no external uptime
  monitor, no PagerDuty/OpsGenie-style escalation, no log aggregation
  beyond journald. This is intentionally a foundation — the same
  "additive, not a rewrite" posture every other Phase 5x foundation
  module (`ai/`, `execution/`, `database/migrations/`) has followed.

## Result

GoldBot is ready for a real VPS deployment:
- `docs/DEPLOYMENT.md` (Phase 56) covers install/configure/run/backup
  generically.
- This document covers VPS-specific process supervision
  (`deploy/systemd/`), a production environment template
  (`.env.production`), and a monitoring foundation
  (`scripts/health_check.py`, `scripts/notify_failure.sh`).
- Nothing here required a code change to `core/`, `data/`, `context/`,
  `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
  `execution/`, `database/`, or `telegram/` — every artifact is new,
  standalone tooling, consistent with this phase's audit-and-prepare
  scope.

**Known gaps, disclosed rather than silently claimed as solved**:
- The systemd unit files and `notify_failure.sh`'s alert path have
  been reviewed for correctness but not run end-to-end against a live
  `systemd`/`journald` + real Telegram bot in this sandbox (no
  `systemd` PID 1 available in this container to test
  `systemctl`/`journalctl` against).
- Docker (Option B) remains build-untested end to end, unchanged from
  Phase 56/57.
- No automated backup retention/rotation exists — the cron example in
  Section 4 is a starting point, not a maintained tool.
