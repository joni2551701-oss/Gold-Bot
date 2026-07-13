# GoldBot

AI-assisted, semi-automated trading signal system for XAUUSD, built on Smart Money Concepts (SMC) market analysis.

## Project Overview

GoldBot analyzes XAUUSD price action using Smart Money Concepts (market structure, liquidity, order blocks, fair value gaps, and AMD cycles), evaluates candidate setups through an AI confidence layer, and delivers approved trade signals via Telegram. GoldBot does not place trades automatically — execution remains manual, performed by the trader in their own MT5 terminal.

## Architecture

GoldBot v0.2 is two separate processes sharing one SQLite database:

- **Trading pipeline** (`main.py`, scheduled via `.github/workflows/trading_bot.yml`):
  Market Data → Context → Strategy → Signal → AI → Decision → Risk →
  Signal Formatter → Telegram Delivery → Persistence. One run per
  invocation; exits when done.
- **Telegram product layer** (`telegram/polling.py`, run as a
  long-lived process): user registration, settings, subscription
  (`FREE`/`PREMIUM`/`VIP`), signal access control, an admin panel, and
  a feedback system — built entirely on top of the pipeline's output,
  without modifying pipeline/strategy/AI/risk logic.

See `docs/telegram_layer.md` for the full service/permission map,
`docs/database_schema.md` for the table-by-table schema, and
`docs/commands_reference.md` for every Telegram command. Release-level
notes live in `docs/v0.2_release_notes.md`.

## Environment variables

Read exclusively through `core/secrets.py` (never hardcoded, no
`.env` file in production).

| Variable | Required | Notes |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram delivery and command polling fail gracefully (not a crash) if missing |
| `TELEGRAM_CHAT_ID` | Yes | Fixed destination for the scheduled pipeline's signal broadcast |
| `TWELVE_DATA_API_KEY` | Yes | Market data fetch fails gracefully (0 candles) if missing |
| `GEMINI_API_KEY` | Reserved | Read by `Secrets` and checked for presence by `/system`; not yet called by the AI layer, which is still a heuristic stub |
| `TELEGRAM_OWNER_ID` | Optional | Defaults to unset (fail-closed: nobody is OWNER) |
| `APP_ENV` | Optional | Defaults to `"development"` |
| `DEBUG` | Optional | Defaults to `"False"` |

## Testing

```
pip install -r requirements.txt pytest pyflakes pytest-cov
python -m pytest tests/
python -m pytest tests/ --cov=. --cov-report=term-missing   # with coverage
```

`.github/workflows/ci.yml` runs this (plus `compileall` and a full
module import sweep) on every push/PR. See `docs/TESTING.md`
for test philosophy, naming rules, fixtures, and directory layout.
