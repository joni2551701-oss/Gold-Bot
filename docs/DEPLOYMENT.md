# GoldBot Deployment Guide (v0.3)

> **Worker deployment permissions boundary:** what the Worker may and
> may not do unilaterally during deployment (Phase 1/Phase 2, and the
> always-Director-Approval list) is defined authoritatively in
> `CLAUDE.md`'s "Deployment Authority — Director Order No. 021"
> section. This document covers the deployment mechanics; that section
> is the single source of truth for Worker authority.

**Production branch: `main`.** As of TASK-DEPLOY-003, `main` is the sole
authoritative production branch and is deployed to the VPS through
`.github/workflows/production_deploy.yml` via a manual
`workflow_dispatch` on the `main` ref (GitHub Actions run #39,
`30318793728`, deployed commit `61bbcb5`, both `validate` and `deploy`
jobs green). `main` now contains the full production surface —
`platform_layer/telegram/polling.py`, `core/pipeline.py`, `main.py`, and the
`scripts/deploy/` release scripts — so the earlier "`main` is a stale
pre-`TradingPipeline` snapshot" note is **obsolete** and has been
removed; verified present on `main` at that commit.

Deploy flow: **GitHub Actions → `push` to `main` *or* `workflow_dispatch`
(ref: `main`) → rsync/SSH → VPS**. See
`docs/deployment/PRODUCTION_DEPLOYMENT.md` for the full pipeline and
`docs/deployment/TASK_DEPLOY_003_REPORT.md` for the deploy record.

> **Reconciliation note (closed — TASK-CICD-001):** the *automatic*
> triggers have been migrated to `main`. `production_deploy.yml`'s
> `push:` filter now names `main`, and `trading_bot.yml`'s scheduled
> checkout is now pinned to `ref: main`. Both the automatic and the
> manual (`workflow_dispatch`) paths therefore deploy the same branch —
> `main` — with no divergence. No workflow references
> `claude/code-analysis-optimization-pwfo3q` any longer, except
> `ci.yml`, which still validates `claude/**` development branches by
> design (validation only, never a deploy or runtime target).

GoldBot is two independent processes sharing one SQLite database file
— see `docs/ARCHITECTURE.md`'s System Overview. Today, the trading
pipeline (`main.py`) runs on GitHub Actions
(`.github/workflows/trading_bot.yml`, scheduled every 5 minutes) and
needs no separate VPS. The Telegram product layer
(`platform_layer/telegram/polling.py`) is a long-running process and does need a
host that stays up — a VPS, a small always-on container, or similar.
This guide covers both. For process supervision, crash recovery, and
a monitoring foundation specific to unattended VPS hosting, see
`docs/production_setup.md` (Phase 58).

## Requirements

- **Python 3.11** (matches `.github/workflows/ci.yml` and
  `trading_bot.yml`'s pinned `python-version`; not tested against
  other versions).
- Dependencies: `requirements.txt` (unpinned, resolves to current
  patched releases) or `requirements-freeze.txt` (exact tested
  snapshot — see that file's own header for when to use which).
- The 4 required environment variables from `.env.example`
  (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TWELVE_DATA_API_KEY`,
  plus optionally `TELEGRAM_OWNER_ID`/`GEMINI_API_KEY`/`APP_ENV`/`DEBUG`).
- Disk: a writable path for `database/goldbot.db` (SQLite file,
  created automatically on first run).

## Install

```bash
git clone <this-repository>
cd Gold-Bot
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt        # or requirements-freeze.txt
```

## Configure

```bash
cp .env.example .env
# edit .env and fill in real values -- never commit this file
```

If your host doesn't support `.env` file loading natively, export the
same variables directly in your process manager's environment
configuration instead (systemd `Environment=`, a container's `-e`
flags, etc.) — `core/secrets.py` reads plain `os.environ`, so either
approach works identically.

## Run

**Trading pipeline** (one-shot, exits when done — run on a schedule,
e.g. cron or a process manager's timer unit, if not using GitHub
Actions):

```bash
python main.py
```

**Telegram product layer** (long-running — needs a process
supervisor so it restarts on crash/reboot):

```bash
python -m telegram.polling
```

These are two separate `python` invocations. Do not try to run them
in the same process — see `docs/ARCHITECTURE.md` for why they're
architecturally independent.

## Restart

- **Trading pipeline**: nothing to restart — it's one-shot. If a
  scheduled run fails, the next scheduled run tries again
  independently (no state carried between runs beyond the database).
- **Telegram product layer**: restart the process (`systemctl restart
  goldbot-polling`, or your process manager's equivalent). It's safe
  to restart at any time — `platform_layer/telegram/polling.py` holds no unsaved
  in-memory state that a restart would lose; every command's effect
  is already persisted to the database by the time a response is
  sent.

## Backup

The entire persistent state is one file: `database/goldbot.db`
(location configurable via `config.Config.DB_PATH`, which reads
`BASE_DIR` from the repository root by default). Back it up with a
plain file copy — no special SQLite tooling required, as long as no
write is in-flight at the moment of copy (a `sqlite3 goldbot.db
".backup backup.db"` online-safe copy is the more careful option if
the Telegram polling process is actively running during the backup
window).

```bash
# simple, safe when the polling process can be paused briefly:
cp database/goldbot.db database/goldbot.db.backup-$(date +%Y%m%d)

# online-safe (no pause needed), if the polling process is live:
sqlite3 database/goldbot.db ".backup database/goldbot.db.backup-$(date +%Y%m%d)"
```

Nothing else needs backing up — `.env`/environment variables are
deployment configuration, not state, and should be redeployed from
your secrets manager rather than restored from a backup.

## Troubleshooting: "/start doesn't respond"

Audited as part of the GitHub Secrets / Environment Configuration
Audit (Owner Monitoring track). If `TELEGRAM_BOT_TOKEN`/
`TELEGRAM_CHAT_ID`/`TELEGRAM_OWNER_ID`/`TWELVE_DATA_API_KEY`/
`GEMINI_API_KEY` are all correctly set as GitHub Secrets, `/start`
can still appear to get no reply — because **GitHub Actions never
runs `platform_layer/telegram/polling.py`**. `.github/workflows/trading_bot.yml`
only runs the one-shot `python main.py` (outbound signal broadcast)
on a cron schedule; there is no GitHub Actions job for the
long-running inbound listener that `/start` (and every other command)
needs, by design — a scheduled Actions job is the wrong shape for an
always-on process (see `docs/ARCHITECTURE.md`'s System Overview and
"Run" above).

`/start` only gets a reply once `python -m telegram.polling` is
actually running somewhere that stays up — a VPS (`deploy/systemd/
goldbot-polling.service`), a container (`docker-compose.yml`'s
`telegram-polling` service), or equivalent. Correctly configured
secrets are necessary but not sufficient; the polling process must
also be deployed and running. Check `journalctl -u goldbot-polling`
(or the equivalent container logs) for one of two explicit startup
log lines: `Startup aborted: Missing TELEGRAM_BOT_TOKEN` (token unset
or unreadable) or `Telegram polling started.` (`platform_layer/telegram/polling.py`'s
existing success log, confirming the listener actually started). Once
started, the configured `TELEGRAM_OWNER_ID` also receives a one-time
"GoldBot Online" message (Telegram Runtime Activation Alpha, TASK 2)
— the fastest confirmation that polling is actually live, no log
access needed. See `docs/TELEGRAM_RUNTIME.md` for the full runtime
observability layer (startup notification, heartbeat, runtime status).

**`BITGET_API_KEY` is not a real secret in this codebase.** Only an
`ENABLE_BITGET` feature-registry flag exists
(`configuration/feature_registry.py`) for a not-yet-built Bitget
provider — no `core/secrets.py` property, no `.env.example` entry,
no code path reads `BITGET_API_KEY`. Setting it as a GitHub Secret is
harmless but has no effect; do not expect it to change bot behavior.
