# GoldBot Deployment Guide (v0.3)

GoldBot is two independent processes sharing one SQLite database file
— see `docs/ARCHITECTURE.md`'s System Overview. Today, the trading
pipeline (`main.py`) runs on GitHub Actions
(`.github/workflows/trading_bot.yml`, scheduled every 5 minutes) and
needs no separate VPS. The Telegram product layer
(`telegram/polling.py`) is a long-running process and does need a
host that stays up — a VPS, a small always-on container, or similar.
This guide covers both.

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
  to restart at any time — `telegram/polling.py` holds no unsaved
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
