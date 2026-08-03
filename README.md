# GoldBot

AI-assisted, semi-automated trading signal system for XAUUSD, built on Smart Money Concepts (SMC) market analysis.

## Canonical architecture

GoldBot v1's architecture is frozen. Each Layer is a single folder holding
its documentation **and** its Python code together — one source of truth:

```text
core_layer/
├── README.md  Layer_Contracts.md  Layer_ModuleMap.md  …
├── configuration/
│   ├── README.md  Contracts.md  ModuleMap.md  SequenceDiagram.md
│   └── settings.py  feature_flags.py  …
└── secrets/
    ├── README.md  Contracts.md  …
    └── secrets.py
```

The 17 Layers are `data_layer/`, `core_layer/`, `context_layer/`,
`indicator_layer/`, `strategy_layer/`, `signal_layer/`, `ai_layer/`,
`decision_layer/`, `risk_layer/`, `execution_layer/`,
`trade_monitoring_layer/`, `database_layer/`, `platform_layer/`,
`media_layer/`, `future_expansion/`, `chart_layer/`, `backtesting_layer/`.
Their canonical ordering (01…17) is recorded in the architecture documents,
not in folder names — a Python package name cannot start with a digit.

- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture index and repository rules
- [FOUNDATION_FREEZE_V1.md](FOUNDATION_FREEZE_V1.md) — what the freeze permits and forbids
- [Architecture_Audit_Plan.md](Architecture_Audit_Plan.md) — audit methodology and every Canonical Rule / ACR
- [Architecture_Audit_Tracker.md](Architecture_Audit_Tracker.md) — audit history, Known Gaps, refactoring TODOs
- [MIGRATION_TRACKER.md](MIGRATION_TRACKER.md) — migration of the pre-freeze code into the Layers

Migration is in progress: pre-freeze top-level packages (`core/`, `data/`,
`ai/`, …) still hold most of the running code and move into their Layer
module by module.

## Production branch

**`main` is the production branch** — and the repository's default
branch. As of TASK-CICD-001 (CI/CD migration to `main`), every CI/CD
path targets `main`: `.github/workflows/trading_bot.yml` checks it out
explicitly (`ref: main`) for the scheduled trading pipeline, and
`.github/workflows/production_deploy.yml` deploys `main` on both its
automatic `push:` trigger and manual `workflow_dispatch`. `main` holds
the full production surface (`telegram/polling.py`, `core/pipeline.py`,
`main.py`, and `scripts/deploy/`). The `claude/**` development branches
are validated by `ci.yml` but are no longer a deploy or runtime target.
See `docs/DEPLOYMENT.md` for the current branch/deploy model and
`docs/PHASE_BRANCH_SYNC_AUDIT.md` for the historical branch-state audit.

## Production deployment

As of Phase P1, GoldBot deploys to its production VPS **only** through
`.github/workflows/production_deploy.yml` — push to the production
branch above (or `workflow_dispatch`), and a validated build (pyflakes/
compileall/pytest) is released via a release-based, symlink-switched
layout with automatic rollback on a failed health check. No manual
production deployment is permitted without explicit Director
authorization. See `docs/deployment/PRODUCTION_DEPLOYMENT.md` and
`docs/deployment/ROLLBACK.md`.

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
  Persistence, gated at four points by `core_layer/pipeline/pipeline_guard.py`'s
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
- **AI Infrastructure** (Phase 61.0, not live-wired): eight
  provider-agnostic/capability-agnostic `ai/` subpackages
  (`capabilities/`, `providers/`, `router/`, `context/`, `access/`,
  `session/`, `tools/`, `audit/`) — no real AI/LLM API call yet. See
  `docs/AI_INFRASTRUCTURE.md`.

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
| `docs/AI_INFRASTRUCTURE.md` | Phase 61.0's AI Infrastructure Foundation — capability/provider/router/context/access/session/tools/audit, none live-wired yet. |
| `docs/PHASE61_AI_FOUNDATION_AUDIT.md` | The reuse audit behind Phase 61.0's eight new `ai/` subpackages. |
| `CLAUDE.md` | The enforced, checked-in version of the same architecture and Trading Safety rules, for any AI agent working in this repository. |

Every other `docs/*.md` file is a phase- or topic-specific deep dive
(e.g. `docs/FEATURE_ENGINEERING.md`, `docs/STRATEGY_LIFECYCLE.md`,
`docs/ASSET_INTELLIGENCE.md`, `docs/CONFIGURATION_MANAGEMENT.md`) —
linked from `docs/ARCHITECTURE.md`'s own per-phase sections.

## Environment variables

Read exclusively through `core_layer/secrets/secrets.py` (never hardcoded, no
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
