# GoldBot

AI-assisted, semi-automated trading signal system for XAUUSD, built on Smart Money Concepts (SMC) market analysis.

## Project Overview

GoldBot analyzes XAUUSD price action using Smart Money Concepts (market structure, liquidity, order blocks, fair value gaps, and AMD cycles), evaluates candidate setups through an AI confidence layer, and delivers approved trade signals via Telegram. GoldBot does not place trades automatically — execution remains manual, performed by the trader in their own MT5 terminal.

## Architecture

As of Phase 60.10 (v0.4 Foundation Freeze), GoldBot is two live
processes sharing one SQLite database, plus a large, tested foundation
layer not yet live-wired (see `docs/FOUNDATION_FREEZE_v0.4.md` for the
full inventory):

- **Trading pipeline** (`main.py`, scheduled via `.github/workflows/trading_bot.yml`):
  Market Data → Data Quality → HTF Bias → Context → Market Phase →
  Signal → Signal Quality → Explainability → Features → AI → Decision
  → Risk → Signal History → Telegram Format → Telegram Delivery →
  Persistence, gated at four points by `core/guards/pipeline_guard.py`'s
  `PipelineGuard` (Emergency-controlled: Pause/Kill/Maintenance/Resume,
  Phase 60.8/60.9). One run per invocation; exits when done.
- **Telegram product layer** (`telegram/polling.py`, run as a
  long-lived process): user registration, settings, subscription
  (`FREE`/`PREMIUM`/`VIP`), signal access control, an admin panel, and
  a feedback system — built entirely on top of the pipeline's output,
  without modifying pipeline/strategy/AI/risk logic.
- **Foundation layer** (not live-wired, real and tested):
  Backtesting/Replay, Execution Simulator, Learning Loop, Adaptive
  Intelligence, Fundamental Intelligence, Performance Validation, and
  18 Owner Command modules — see `docs/ARCHITECTURE.md`'s per-phase
  sections and `docs/FOUNDATION_FREEZE_v0.4.md` for what's built and
  what's deliberately still unwired.

See `docs/telegram_layer.md` for the full service/permission map,
`docs/database_schema.md` for the table-by-table schema, and
`docs/commands_reference.md` for every Telegram command. Release-level
notes live in `docs/v0.2_release_notes.md`; the current version
roadmap is in `docs/SYSTEM_OVERVIEW.md`.

## Documentation

Start with `docs/SYSTEM_OVERVIEW.md` for a first-read map of what
GoldBot is and where to go next. The full documentation set:

| Document | Answers |
|---|---|
| `docs/SYSTEM_OVERVIEW.md` | What is GoldBot? Architecture, data flow, version roadmap. |
| `docs/ARCHITECTURE.md` | The detailed, implementation-accurate technical reference — every module, every phase, the exact pipeline stage order. |
| `docs/ARCHITECTURE_RULES.md` | Module boundaries — what each module may and may not do. |
| `docs/DECISION_PRINCIPLES.md` | Decision ownership — which module has final say over what. |
| `docs/DEVELOPMENT_GUIDE.md` | Development rules — the workflow for any code change, and what's forbidden without explicit approval. |
| `docs/DOCUMENTATION_STANDARD.md` | The format every module's own documentation follows. |
| `docs/FOUNDATION_FREEZE_v0.4.md` | What's complete, what's remaining, and the Foundation Principles GoldBot's architecture commits to before the v0.4 AI phase begins. |
| `docs/PHASE60_10_FOUNDATION_AUDIT.md` | The full module inventory, dependency graph, dead-code findings, and duplicate-code findings behind the freeze declaration. |
| `CLAUDE.md` | The enforced, checked-in version of the same architecture and Trading Safety rules, for any AI agent working in this repository. |

Every other `docs/*.md` file is a phase- or topic-specific deep dive
(e.g. `docs/FEATURE_ENGINEERING.md`, `docs/STRATEGY_LIFECYCLE.md`,
`docs/ASSET_INTELLIGENCE.md`, `docs/CONFIGURATION_MANAGEMENT.md`) —
linked from `docs/ARCHITECTURE.md`'s own per-phase sections.

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
