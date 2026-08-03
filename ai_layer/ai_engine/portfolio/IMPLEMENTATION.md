# AI Portfolio Intelligence (`ai/portfolio/`)

Phase 66.7 (AI Portfolio Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_7_AUDIT.md`'s TASK 0 audit — the eighth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/strategy/` (Phase 66.6).

## What this package is

A Foundation for structuring portfolio-shaped metadata (`PortfolioRecord`)
that answers one question: "Portfolio qanday holatda?" (What state is
the portfolio in?). It never opens a trade, never sizes a lot, never
replaces the Risk Manager, never affects the Decision Engine, and
never optimizes a portfolio — GoldBot's Trading Core remains the only
source of any BUY/SELL/NO_TRADE decision and the only sizing
authority. This phase builds the contract and CRUD runtime only; it
does not evaluate, grade, or draw conclusions itself.

### TASK 8 — Future Compatibility (architecture only, no code)

The brief's own ten future directions are recorded here as
Foundation-level compatibility notes, not implemented:

- **Multi Portfolio** (Personal, Prop Firm, Investor) — `PortfolioRecord`
  is already a standalone record with its own `portfolio_id`, so
  multiple portfolios can coexist today; a dedicated
  per-account-type classification field does not exist yet.
- **Capital Allocation** — no capital-amount field exists on
  `PortfolioRecord`.
- **Asset Allocation** — no per-asset breakdown exists.
- **Cross-Asset Portfolio** (Gold, Forex, Crypto, ...) — no
  multi-asset-class linkage exists.
- **Portfolio Correlation Matrix** — no cross-portfolio relationship
  tracking exists.
- **Diversification Analysis** — no diversification scoring exists.
- **Portfolio Benchmark** — no comparison-against-baseline mechanism
  exists.
- **Portfolio Optimization** — no parameter-tuning or rebalancing
  surface exists.
- **Portfolio Simulation** — no backtest/replay wiring exists in this
  package (see `backtesting/` for the separate, already-existing
  Trading Core replay engine, untouched by this phase).
- **Portfolio Recommendation** — no AI-generated suggestion of any
  kind exists; `notes`/`risk_level`/`health` are always caller-supplied
  or adapter-computed via deterministic counting only.

`tests/ai/portfolio/test_ai_portfolio_compatibility.py` permanently
confirms none of these ten concepts exists as a module, class, or
method anywhere in this package.

## What this package is not

- No trade opening, no lot sizing, no Risk Manager replacement, no
  Decision Engine interaction of any kind.
- No portfolio optimization of any kind.
- No LLM call, no Reasoning, no real inference anywhere —
  `portfolio_name`/`status`/`risk_level`/`health`/`notes` are always
  caller-supplied, never generated or graded by this package;
  `strategy_count`/`active_strategy_count` are either caller-supplied
  or deterministically counted by `strategy_adapter.py`, never
  inferred.
- No database — SQLite/Postgres/Redis, none anywhere in this package.
  `PortfolioRuntime` stores records in an in-memory dict.
- No network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
  `voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
  `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` — zero exceptions, permanently
  enforced by `tests/ai/portfolio/test_ai_portfolio_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_7_AUDIT.md`, `docs/PHASE66_7_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_PORTFOLIO.md` — the full subsystem documentation.
- `ai/performance/` — the sibling package this phase's
  `performance_adapter.py` reads from (type-only, no Runtime import).
- `ai/strategy/` — the sibling package this phase's
  `strategy_adapter.py` reads from (type-only, no Runtime import).
- `risk_layer/risk_engine/risk_manager.py` — the pre-existing Trading Core risk-sizing
  contract this package's own models are deliberately independent
  from (import forbidden by Rule 1).
