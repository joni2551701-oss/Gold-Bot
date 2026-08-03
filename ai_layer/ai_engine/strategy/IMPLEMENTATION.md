# AI Strategy Intelligence (`ai/strategy/`)

Phase 66.6 (AI Strategy Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_6_AUDIT.md`'s TASK 0 audit — the seventh
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/performance/` (Phase 66.5).

## What this package is

A Foundation for structuring strategy-shaped metadata (`StrategyRecord`)
that answers one question: "Qaysi strategiya qanday ishlayapti?"
(Which strategy is performing how?). It never opens a trade, never
gives a signal, never manages risk, and never affects the Decision
Engine — GoldBot's Trading Core remains the only source of any
BUY/SELL/NO_TRADE decision. This phase builds the contract and CRUD
runtime only; it does not evaluate, grade, or draw conclusions itself.

### TASK 8 — Future Compatibility (architecture only, no code)

The brief's own nine future directions are recorded here as
Foundation-level compatibility notes, not implemented:

- **Strategy Versioning** — `StrategyRecord.strategy_version` is a
  plain string field today (`"v1"`, `"v2"`, ...); a version *history*
  (which version ran when) is not tracked by this Foundation.
- **Market Regime** (Trending/Range/High-Low Volatility/News) — no
  regime field exists on `StrategyRecord`; a future phase would add one
  additively.
- **Strategy Evolution History** — no time-series of a strategy's own
  performance across months exists; `StrategyRuntime` stores only the
  current state of each record.
- **A/B Strategy Testing** — no comparison mechanism between two
  `StrategyRecord`s exists.
- **Optimization Hooks** — no parameter-tuning surface exists.
- **Auto Benchmark** — no automatic comparison against a baseline
  exists.
- **Simulation** — no backtest/replay wiring exists in this package
  (see `backtesting/` for the separate, already-existing Trading Core
  replay engine, untouched by this phase).
- **Recommendation** — no AI-generated suggestion of any kind exists;
  `notes`/`confidence` are always caller-supplied.
- **Correlation** — no cross-strategy relationship tracking exists.

`tests/ai/strategy/test_ai_strategy_compatibility.py` permanently
confirms none of these nine concepts exists as a module, class, or
method anywhere in this package.

## What this package is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind.
- No Risk computation, no Trading Core interaction of any kind.
- No LLM call, no Reasoning, no real inference anywhere — `strategy_name`/
  `strategy_type`/`strategy_version`/`confidence`/`notes`/`status` are
  always caller-supplied, never generated or graded by this package.
- No database — SQLite/Postgres/Redis, none anywhere in this package.
  `StrategyRuntime` stores records in an in-memory dict.
- No network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
  `voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
  `portfolio/`, `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` — zero exceptions,
  permanently enforced by `tests/ai/strategy/test_ai_strategy_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_6_AUDIT.md`, `docs/PHASE66_6_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_STRATEGY.md` — the full subsystem documentation.
- `ai/performance/` — the sibling package this phase's
  `performance_adapter.py` reads from (type-only, no Runtime import).
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `strategies/lifecycle/` — the pre-existing Trading Core Strategy
  metadata contract this package's own models are deliberately
  independent from (import forbidden by Rule 1).
