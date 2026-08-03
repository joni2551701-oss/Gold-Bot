# AI Research Intelligence (`ai/research/`)

Phase 66.8 (AI Research Intelligence Foundation). **Final phase of the
`66.x` AI Trading Intelligence sub-sequence.** Genuine new subpackage
inside the already-existing `ai/` top-level package, confirmed by
`docs/PHASE66_8_AUDIT.md`'s TASK 0 audit — sitting immediately after
`ai/portfolio/` (Phase 66.7). Per the brief's own framing: this
phase's job is to create a single scientific layer that accepts data
from every prior `66.x` Foundation module, while AI still never
opens a trade, gives a signal, computes risk, selects a strategy, or
touches Trading Core in any way.

## Position in the pipeline

Trading Core → Trade Journal (66.2) → Learning (66.3) → Coaching
(66.4) → Performance Intelligence (66.5) → Strategy Intelligence
(66.6) → Portfolio Intelligence (66.7) → **Research Intelligence
(66.8, final)**.

Research Intelligence never evaluates a trade, never sizes a lot,
never mines a pattern, never detects a market regime, and performs no
real AI inference of any kind (Rule 4: "GPT/Claude/Gemini/OpenAI/
AI-inference/Reasoning YO'Q"). It never touches `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, `monitoring/`,
`telegram/`, `database/`, `voice/`, `assistant/`, `core.`, `ai_layer.knowledge_ai.memory_manager`,
or `ai_layer.ai_engine.reasoning` (Rule 1/TASK 7's own isolation list).

## Model (TASK 2)

- `models.py` — `ResearchStatus` (ACTIVE/ARCHIVED), `ResearchPriority`
  (LOW/MEDIUM/HIGH/CRITICAL), `ResearchCategory`
  (MARKET/STRATEGY/PERFORMANCE/PORTFOLIO/LEARNING/GENERAL).
  `ResearchRecord` (TASK 2's own exact field list: `research_id`,
  `title`, `category`, `priority`, `status`, `summary`,
  `source_count`, `notes`, `created_at`). `generate_research_id()` — a
  stateless uuid4 generator.

### No naming collision

Documented in `docs/PHASE66_8_AUDIT.md`: a repository-wide search
found no pre-existing `Research`-shaped model anywhere, and no
pre-existing top-level `research/` package at all — confirmed absent
by direct filesystem check, not merely import-forbidden the way
`strategies/` (Phase 66.6) and `risk/` (Phase 66.7) were.

## Runtime (TASK 3)

`research_runtime.py`'s `ResearchRuntime` is CRUD-only, exactly as
Rule 5 requires ("CRUD only."): `create()`/`get()`/`list()`/
`update()`/`update_notes()`/`archive()`, nothing else. In-memory only
(Rule 3) — a private dict, the same "Foundation, not a real
persistence layer" convention `ai/portfolio/portfolio_runtime.py`'s
own `_records` dict already established. `update()` mutates only
`priority`/`status`/`summary`/`source_count`, each left unchanged when
its argument is `None`; `update_notes()` only ever mutates `notes`.
`archive()` sets `status=ResearchStatus.ARCHIVED` and never deletes a
record. Owner-gated: every method re-checks
`ai_layer.fundamental_ai.access.is_research_intelligence_enabled_for()` itself.

## Performance Adapter (TASK 4)

`performance_adapter.py`'s `performance_record_to_research_input()` is
a pure, type-only mapping — TASK 4's own instruction: "Reuse qiladi.
Inference YO'Q." It reads an existing
`ai_layer.ai_engine.performance.models.PerformanceRecord` (Phase 66.5, LOCKed) and
relays `notes`, and sets `category=ResearchCategory.PERFORMANCE` — a
**structural constant of this specific adapter, not content-based
inference**: every record this adapter ever produces originates from a
`PerformanceRecord`, so its category is fixed by construction with
zero ambiguity and zero content-reading. `title`/`priority`/`status`/
`summary`/`source_count` are deliberately absent — `PerformanceRecord`
carries no field shaped for any of the five. Never imports
`ai_layer.ai_engine.performance.performance_runtime`. The one file in `ai/research/`
permitted to import `ai_layer.ai_engine.performance.models`.

## Strategy Adapter (TASK 5)

`strategy_adapter.py`'s `strategy_record_to_research_input()` follows
the identical single-record mapping posture, reading an existing
`ai_layer.ai_engine.strategy.models.StrategyRecord` (Phase 66.6, LOCKed) — relays
`notes`, sets `category=ResearchCategory.STRATEGY` (structural
constant, not inference). Unlike Phase 66.7's own
`strategy_adapter.py` (the first `66.x` adapter to operate over a
`Sequence[StrategyRecord]` for deterministic counting), this phase's
version reverts to the more common single-record precedent —
`ResearchRecord.source_count` has no natural single-type counting
target, so no sequence-aggregation logic exists here (see
`docs/PHASE66_8_AUDIT.md`'s "Question 6"). Never imports
`ai_layer.ai_engine.strategy.strategy_runtime`. The one file in `ai/research/`
permitted to import `ai_layer.ai_engine.strategy.models`.

## Portfolio Adapter (TASK 6)

`portfolio_adapter.py`'s `portfolio_record_to_research_input()` is the
third and final sibling-Foundation adapter, reading an existing
`ai_layer.ai_engine.portfolio.models.PortfolioRecord` (Phase 66.7, LOCKed) — relays
`notes`, sets `category=ResearchCategory.PORTFOLIO` (structural
constant, not inference). Never imports
`ai_layer.ai_engine.portfolio.portfolio_runtime`. The one file in `ai/research/`
permitted to import `ai_layer.ai_engine.portfolio.models`.

## Owner Mode (TASK 8)

`access.py`'s `is_research_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_research_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/portfolio/access.py`'s shape exactly.

## Memory Preparation (TASK 7)

`memory_adapter.py`'s `research_reference_key(record) -> str` builds a
plain string key (`"research:{research_id}"`) for a future,
separately-approved phase to use once real Memory storage is wired —
this module never imports `ai_layer.knowledge_ai.memory_manager` at all. Mirrors
`ai_layer.ai_engine.portfolio.memory_adapter.portfolio_reference_key()`'s own
precedent exactly.

## Future Compatibility (TASK 9)

No implementation exists for Research Dataset, Pattern Mining, Market
Regime Detection, Knowledge Graph Integration, Paper Generator,
Backtest Dataset, AI Dataset Builder, Research Report, Research
Versioning, Research Export, or Research Archive (beyond `archive()`'s
own status flip) — only the architecture (this Foundation's own
`ResearchRecord`/`ResearchStatus`/`ResearchPriority`/
`ResearchCategory` vocabulary and CRUD surface) is ready for a future,
separately-approved phase to build on top of. The brief's own TASK 9
names all eleven directions explicitly.
`tests/ai/research/test_ai_research_compatibility.py` permanently
confirms none of them exists as a module, class, or method anywhere in
this package.

## What it is not

- No BUY/SELL, no signal generation, no risk computation, no strategy
  selection, no Trading Core interaction of any kind.
- No pattern mining, no market regime detection, no dataset assembly.
- No real AI inference — `title`/`summary`/`notes`/`source_count` are
  always caller-supplied, never generated or graded by this package;
  each sibling-Foundation adapter's `category` value is a fixed
  structural constant of that adapter, never inferred from record
  content.
- No database — `ResearchRuntime` is in-memory only.
- No LLM, no Reasoning, no network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
  `voice/`, `assistant/`, `core.`, `ai_layer.knowledge_ai.memory_manager`, or `ai_layer.ai_engine.reasoning` —
  zero exceptions, permanently enforced by
  `tests/ai/research/test_ai_research_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## AI Foundation closed

This is the final phase in the `66.x` AI Trading Intelligence
sub-sequence. All nine Foundation modules are now built and LOCKed:
Trading Analyst (66.0), Chart Intelligence (66.1), Trade Journal
(66.2), Learning (66.3), Coaching (66.4), Performance (66.5), Strategy
(66.6), Portfolio (66.7), Research (66.8). See
`docs/roadmap/AI_EVOLUTION.md` for the Director's own next-steps notes
(GoldBot Core Owner Monitoring Alpha, Track B — not a new AI
Foundation phase).

## Related

- `docs/PHASE66_8_AUDIT.md`, `docs/PHASE66_8_FREEZE.md` — full
  documentation of this phase.
- `ai/research/README.md` — the package's own top-level README.
- `ai/performance/` — the sibling package this phase's
  `performance_adapter.py` reads from (type-only, no Runtime import).
- `ai/strategy/` — the sibling package this phase's `strategy_adapter.py`
  reads from (type-only, no Runtime import).
- `ai/portfolio/` — the sibling package this phase's
  `portfolio_adapter.py` reads from (type-only, no Runtime import).
- `docs/ai/AI_PORTFOLIO.md` — the immediately preceding phase's own
  documentation.
