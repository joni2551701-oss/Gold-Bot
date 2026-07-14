# GoldBot Architecture Overview

System-level overview and dependency rules. For the detailed
per-module responsibility map, see `docs/code_structure.md`; for the
database-specific schema/relationship map, see
`docs/DATABASE.md`; for the Telegram-specific
service/permission map, see `docs/telegram_layer.md`. This document
is the entry point that ties them together and states the dependency
rules explicitly, which none of the earlier docs did as their primary
focus.

## System Overview

GoldBot is two independent OS processes sharing one SQLite database
file (`database/goldbot.db`):

1. **Trading pipeline** (`main.py`, scheduled by
   `.github/workflows/trading_bot.yml` every 5 minutes during trading
   hours) — one run per invocation, exits when done. Fetches market
   data, analyzes it, and (if a signal clears every gate) sends one
   Telegram notification and persists the result.
2. **Telegram product layer** (`telegram/polling.py`, run as a
   long-lived process) — user registration, settings, subscriptions,
   admin panel, feedback. Reads/writes the same database, entirely
   independent of when the pipeline last ran.

They are never invoked from one another and share no in-memory state
— only the database file connects them.

## Data Flow

```
Market Data (data/)
      |
      v
HTF Bias (context/htf_bias.py)   -- Daily/H4/H1 market-context only
      |                             (Phase A2; never a trade decision,
      |                             see docs/HTF_BIAS.md; result is
      |                             carried in the pipeline's return
      |                             dict, not yet consumed downstream)
      v
Context Engine (context/)        -- SMC structure detection
      |
      v
Strategies (strategies/)         -- 3 independent SMC methodologies
      |
      v
Signal Generation (signals/)     -- aggregates strategy output
      |
      v
AI Layer (ai/)                   -- advisory input only (currently a stub)
      |
      v
Decision Engine (decision/)      -- APPROVE / REJECT / NO_TRADE
      |
      v
Risk Manager (risk/)             -- geometry + stop-loss validation
      |
      v
Telegram Notification Filter     -- (inside core/pipeline.py)
      |                             APPROVE + risk-approved only,
      |                             highest-confidence candidate,
      |                             max 1 message per cycle
      v
Database (database/) <---------> Telegram Product Layer (telegram/)
```

`core/pipeline.py`'s `TradingPipeline` is the only place that wires
every layer above together end to end — see its own docstring and
`docs/AUDIT_REPORT.md` for why the notification-eligibility filter
exists in exactly the shape it does.

## Module Responsibilities (summary — full detail in `docs/code_structure.md`)

| Module | Responsibility |
|---|---|
| `core/` | Cross-cutting infrastructure: pipeline orchestration, logging, secrets. |
| `data/` | Market data fetch and normalization. |
| `context/` | Pure SMC market-structure detection functions, plus HTF Bias (`htf_bias.py`, Phase A2) — a market-context-only Daily/H4/H1 classification, not itself part of `ContextSnapshot`. |
| `strategies/` | Independent signal-candidate generation per SMC methodology. |
| `signals/` | The `SignalCandidate` data contract and strategy aggregation. |
| `ai/` | Advisory-only AI evaluation layer (Phase 55: foundation for a future provider; production analyzer is still a heuristic stub). |
| `decision/` | Blends signal + AI confidence into APPROVE/REJECT/NO_TRADE. |
| `risk/` | SL/TP geometry and stop-loss-distance validation; sizing suggestion only. |
| `execution/` | Inert scaffolding for future MT5 integration — not reachable from any runtime path today. |
| `monitoring/` | Performance/statistics reading, not wired into any live command yet. |
| `database/` | SQLite persistence — the only place SQL is written. |
| `telegram/` | The Telegram product layer: routing, permissions, handlers, services. |

## Dependency Rules

A layer may depend on the layer(s) below it in the data-flow diagram
above, and on `core/`/`config.py` (cross-cutting). It must never
depend upward or sideways into an unrelated layer. Concretely, as
implemented and enforced today (verified by the Phase 48 audit's
circular-import check and re-verified every phase since via the CI
import sweep):

- `context/`, `strategies/`, `signals/` never import `telegram/`,
  `database/`, or `ai/`.
- `ai/` never imports `database/` or `telegram/`.
- `decision/` imports `ai/` (for `AIAnalysisResult`) and `signals/`,
  never `database/` or `telegram/`.
- `risk/` imports `decision/` and `signals/`, never `database/` or
  `telegram/`.
- `telegram/handlers.py` never imports `database/*` or
  `core/pipeline.py` directly — only `telegram/*_service.py` (see
  `telegram/handlers.py`'s own module docstring, which states this
  rule explicitly).
- `database/*_repository.py` never imports `telegram/` — a repository
  knows nothing about Telegram, permissions, or commands.
- `core/pipeline.py` is the one file allowed to import from every
  layer — it is the orchestrator, not a layer itself.

If a change requires violating one of these rules, that is a signal
to stop and reconsider the design, not to add the import and move on
— see `CLAUDE.md`'s "Architecture Rules" for the same point stated as
a working rule rather than a description.
