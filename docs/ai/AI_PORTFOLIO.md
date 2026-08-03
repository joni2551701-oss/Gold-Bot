# AI Portfolio Intelligence (`ai/portfolio/`)

Phase 66.7 (AI Portfolio Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_7_AUDIT.md`'s TASK 0 audit — the eighth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/strategy/` (Phase 66.6). Per the brief's own
framing: this phase's job is to answer one question — "Portfolio
qanday holatda?" (What state is the portfolio in?) — while AI still
never opens a trade, sizes a lot, replaces the Risk Manager, affects
the Decision Engine, or optimizes a portfolio; GoldBot's Trading Core
remains the only source of any BUY/SELL/NO_TRADE decision and the only
sizing authority.

## Position in the pipeline

Trading Core → Trade Journal (66.2) → Learning (66.3) → Coaching
(66.4) → Performance Intelligence (66.5) → Strategy Intelligence
(66.6) → **Portfolio Intelligence (66.7)** → Research Intelligence
(66.8, future).

Portfolio Intelligence never evaluates a trade, never sizes a lot,
never optimizes an allocation, and performs no real AI inference of
any kind (Rule 4: "GPT/Claude/Gemini/Reasoning/Inference YO'Q"). It
never touches `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
`voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
`research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` (TASK 9's own isolation list).

## Model (TASK 2)

- `models.py` — `PortfolioStatus` (ACTIVE/PAUSED/ARCHIVED),
  `PortfolioRiskLevel` (LOW/MEDIUM/HIGH/CRITICAL), `PortfolioHealth`
  (GOOD/WARNING/POOR). `PortfolioRecord` (TASK 2's own exact field
  list: `portfolio_id`, `portfolio_name`, `status`, `risk_level`,
  `health`, `strategy_count`, `active_strategy_count`, `notes`,
  `created_at`). `generate_portfolio_id()` — a stateless uuid4
  generator.

### No naming collision

Documented in `docs/PHASE66_7_AUDIT.md`: a repository-wide search
found no pre-existing `Portfolio`-shaped model anywhere.
`risk_layer/risk_engine/risk_manager.py`'s `RiskResult`/`RiskManager` are the nearest
conceptual neighbor by name only — a per-trade sizing contract, not a
per-portfolio one, and Trading Core (`risk/`) — import forbidden
outright by this phase's own Rule 1, the same absolute-ban posture
`docs/PHASE66_6_AUDIT.md` already established for `strategies/`.

## Runtime (TASK 3)

`portfolio_runtime.py`'s `PortfolioRuntime` is CRUD-only, exactly as
Rule 5 requires ("Foundation. CRUD only."):
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
nothing else. In-memory only (Rule 3) — a private dict, the same
"Foundation, not a real persistence layer" convention
`ai/strategy/strategy_runtime.py`'s own `_records` dict already
established. `update()` mutates only `status`/`risk_level`/`health`/
`strategy_count`/`active_strategy_count`, each left unchanged when its
argument is `None`; `update_notes()` only ever mutates `notes`.
`archive()` sets `status=PortfolioStatus.ARCHIVED` and never deletes a
record. Owner-gated: every method re-checks
`ai_layer.ai_engine.portfolio.access.is_portfolio_intelligence_enabled_for()` itself.

## Performance Adapter (TASK 4)

`performance_adapter.py`'s `performance_record_to_portfolio_input()`
is a pure, type-only mapping — TASK 4's own instruction: "Type-only...
Inference YO'Q." It reads an existing
`ai_layer.ai_engine.performance.models.PerformanceRecord` (Phase 66.5, LOCKed) and
relays only `notes`. `portfolio_name`/`status`/`risk_level`/`health`/
`strategy_count`/`active_strategy_count` are deliberately absent —
`PerformanceRecord` carries no field shaped for any of the six. Never
imports `ai_layer.ai_engine.performance.performance_runtime`. The one file in
`ai/portfolio/` permitted to import `ai_layer.ai_engine.performance.models`.

## Strategy Adapter (TASK 5)

`strategy_adapter.py`'s `strategy_records_to_portfolio_input()` is the
first `66.x` adapter to operate over a **sequence** of source records
rather than a single one — TASK 5's own instruction ("Type-only...
Inference YO'Q") still applies, but `PortfolioRecord.strategy_count`/
`.active_strategy_count` are aggregate counts no single
`ai_layer.ai_engine.strategy.models.StrategyRecord` (Phase 66.6, LOCKed) could ever
supply. `strategy_count = len(records)` and `active_strategy_count`
counts records whose `status == StrategyStatus.ACTIVE` — both are
**deterministic counting, not inference**, the same class of operation
`ai_layer.ai_engine.performance.analytics_adapter.performance_records_to_win_rate_metric()`
(Phase 66.5) already performed. `notes` is deliberately absent — with
multiple source records, no single canonical note exists to relay
without an arbitrary choice. The one file in `ai/portfolio/` permitted
to import `ai_layer.ai_engine.strategy.models`.

## Owner Mode (TASK 7)

`access.py`'s `is_portfolio_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_portfolio_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/strategy/access.py`'s shape exactly.

## Memory Preparation (TASK 6)

`memory_adapter.py`'s `portfolio_reference_key(record) -> str` builds
a plain string key (`"portfolio:{portfolio_id}"`) for a future,
separately-approved phase to use once real Memory storage is wired —
this module never imports `ai_layer.knowledge_ai.memory_manager` at all. Mirrors
`ai_layer.ai_engine.strategy.memory_adapter.strategy_reference_key()`'s own precedent
exactly.

## Future Compatibility (TASK 8)

No implementation exists for Multi Portfolio (Personal/Prop Firm/
Investor), Capital Allocation, Asset Allocation, Cross-Asset Portfolio,
Portfolio Correlation Matrix, Diversification Analysis, Portfolio
Benchmark, Portfolio Optimization, Portfolio Simulation, or Portfolio
Recommendation — only the architecture (this Foundation's own
`PortfolioRecord`/`PortfolioStatus`/`PortfolioRiskLevel`/
`PortfolioHealth` vocabulary and CRUD surface) is ready for a future,
separately-approved phase to build on top of. The Director's own notes
for this phase name these ten directions explicitly, plus Portfolio
Intelligence as a research datasource for Phase 66.8.
`tests/ai/portfolio/test_ai_portfolio_compatibility.py` permanently
confirms none of them exists as a module, class, or method anywhere in
this package.

## What it is not

- No trade opening, no lot sizing, no Risk Manager replacement, no
  Decision Engine interaction of any kind.
- No portfolio optimization of any kind.
- No real AI inference — `portfolio_name`/`status`/`risk_level`/
  `health`/`notes` are always caller-supplied, never generated or
  graded by this package; `strategy_count`/`active_strategy_count` are
  either caller-supplied or deterministically counted, never inferred.
- No database — `PortfolioRuntime` is in-memory only.
- No LLM, no network call.
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
- `ai/portfolio/README.md` — the package's own top-level README.
- `ai/performance/` — the sibling package this phase's
  `performance_adapter.py` reads from (type-only, no Runtime import).
- `ai/strategy/` — the sibling package this phase's `strategy_adapter.py`
  reads from (type-only, no Runtime import, sequence-based counting).
- `risk_layer/risk_engine/risk_manager.py` — the pre-existing Trading Core risk-sizing
  contract this package's own models are deliberately independent
  from (import forbidden by Rule 1).
- `docs/ai/AI_STRATEGY.md` — the immediately preceding phase's own
  documentation.
