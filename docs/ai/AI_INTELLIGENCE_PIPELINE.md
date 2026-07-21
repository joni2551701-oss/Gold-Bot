# GoldBot — AI Intelligence Pipeline

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `ai/intelligence_runtime.py`
(Phase 64.0), real code, foundation-only — no live Telegram handler
calls this yet.

## What this is

The one composition root for the Official Intelligence Pipeline
(`docs/roadmap/AI_EVOLUTION.md`):

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Media → Broadcast
```

Two documents (`docs/architecture/AI_FLOW.md`, `docs/ai/AI_PIPELINE.md`)
described this order in prose before this phase; neither was backed by
orchestrating code. `docs/PHASE64_0_AUDIT.md` confirmed no orchestrator
existed anywhere in the codebase — `IntelligenceRuntime` is the first.

## `IntelligenceRuntime.run(topic: str) -> PipelineRun`

```
IntelligenceRuntime.run("BOS")
  KNOWLEDGE     KnowledgeManager.search(topic)                         -- deterministic lookup
       │
       ▼
  MEMORY        MemoryRuntime.store(MemoryEntry)/.recall()             -- deterministic storage
       │
       ▼
  REASONING     ReasoningRuntime.reason(ReasoningResult)                -- deterministic storage
       │            (steps built via reasoning_adapters.step_from_knowledge_entry())
       ▼
  CONVERSATION  ConversationEngine.start_session()/.append()             -- deterministic, never .ask()
       │
       ▼
  EXPLANATION   ExplanationBuilder.build(ExplanationInput)                -- template-based, no AIService call
       │            (fields via reasoning_adapters.reasoning_result_to_explanation_fields())
       ▼
  CONTENT       ContentEngine.create(...)                                  -- deterministic, never .generate()
       │
       ▼
  MEDIA         media.media_pipeline.prepare_media_from_content(...)        -- deterministic (Phase 63.7)
       │
       ▼
  BROADCAST     broadcast.broadcast_adapter.broadcast_asset_from_content_and_media(...)
                + BroadcastManager.prepare_broadcast(...)                    -- deterministic (Phase 63.8)
```

Every arrow above is a call to that layer's own, pre-existing,
already-LOCKed deterministic entry point — `IntelligenceRuntime` adds
zero new business logic anywhere. `run()` returns a `PipelineRun`
(`topic: str`, `stages: List[PipelineStageResult]`); each
`PipelineStageResult` (`stage: PipelineStage`, `ok: bool`,
`detail: str`) is a plain dataclass carrying only primitive values —
never another layer's own dataclass object (Rule 4).

## What it is not

- Not a new Manager for any layer — `IntelligenceRuntime` calls
  `KnowledgeManager`/`MemoryRuntime`/`ReasoningRuntime`/
  `ConversationEngine`/`ExplanationBuilder`/`ContentEngine`/
  `MediaManager`/`BroadcastManager` exactly as each phase already built
  them; none of the eight is subclassed, wrapped, or duplicated.
- Not an LLM caller — every stage is deterministic; `ConversationEngine.ask()`
  and `ContentEngine.generate()` (the two real `AIService.ask()`-calling
  paths in this pipeline) are never called. `test_intelligence_runtime.py`'s
  own structural test enforces this.
- Not wired into `telegram/command_router.py`, `core/pipeline.py`, or
  any Owner command — foundation only, callable standalone.
- Not the same thing as `ai/runtime/ai_service.py`'s `AIService`/
  `RuntimeManager` — that Runtime survives *one provider call* (retry,
  circuit breaker, cache); this Runtime *composes eight Intelligence
  layers*. Different concern, different file, both real.

## Real callers of `run()` (updated Phase 66.0)

`IntelligenceRuntime.run()` itself is unmodified, unmoved, and its
signature unchanged (Phase 65.4's own Rule 1, still honored by Phase
66.0's own Rule 1: no rename/move/breaking API) — but it now has two
real callers:

- `assistant/runtime_adapter.py`'s `run_intelligence_pipeline()`
  (Phase 65.4) — a thin wrapper that Owner-gates the call and passes
  `profile.user_id` as `telegram_id`.
- `ai/trading_analyst/analyst_runtime.py`'s
  `TradingAnalystRuntime.analyze()` (Phase 66.0) — calls
  `run(topic=data.symbol)` for its Knowledge/Memory/Reasoning/
  Conversation grounding side-effect only; the returned `PipelineRun`
  is not inspected further, since `TradingAnalysis`'s own summary comes
  from a separate, second `ExplanationBuilder.build()` call built from
  `TradingAnalysisInput`'s richer TRADE-mode fields.

`ai/intelligence_runtime.py` itself required zero code change for
either caller.

## Why this one file may import every layer

Every individual layer's own isolation is unchanged and still
independently tested (Broadcast still cannot import Reasoning
directly, etc.). `ai/intelligence_runtime.py` is the **composition
root** — the one place allowed to import every layer it composes,
the same role `core/pipeline.py` plays for the Trading layer. See
`docs/PHASE64_0_AUDIT.md` for the full reasoning.

## Note — `ai/chart_intelligence/` does not call `run()` (Phase 66.1)

Unlike `ai/trading_analyst/analyst_runtime.py`, Phase 66.1's
`ai/chart_intelligence/chart_runtime.py` does **not** call
`IntelligenceRuntime.run()` — TASK 0's own audit found no need for
Knowledge/Memory/Reasoning/Conversation grounding for a pure
relay/transform over caller-supplied chart fields; `ChartRuntime`
composes `ExplanationBuilder` directly instead. Recorded here so a
future reader does not assume every `66.x` runtime is a third caller
of this file. Phase 66.2's `ai/trade_journal/journal_runtime.py`
likewise never calls `run()` — `TradeJournalRuntime` is CRUD-only
(Rule 4), with no Explanation/Knowledge/Memory grounding of any kind.
Phase 66.3's `ai/learning/learning_runtime.py` follows the same
pattern — `LearningRuntime` is CRUD-only (Rule 10: no real AI
inference), never calls `run()` or any Explanation/Knowledge/Memory
system. Phase 66.4's `ai/coaching/coaching_runtime.py` follows the
same pattern again — `CoachingRuntime` is CRUD-only ("LLM yo'q.
Reasoning yo'q. Inference yo'q."), never calls `run()` or any
Explanation/Knowledge/Memory system. Phase 66.5's
`ai/performance/performance_runtime.py` follows the same pattern once
more — `PerformanceRuntime` is CRUD-only ("AI xulosa bermaydi. GPT
chaqirmaydi. Scoring algoritm yaratmaydi."), never calls `run()` or any
Explanation/Knowledge/Memory system. Phase 66.6's
`ai/strategy/strategy_runtime.py` follows the same pattern once more
again — `StrategyRuntime` is CRUD-only (Rule 5: "Bu Foundation. Faqat
CRUD."), never calls `run()` or any Explanation/Knowledge/Memory
system. Phase 66.7's `ai/portfolio/portfolio_runtime.py` follows the
same pattern once more — `PortfolioRuntime` is CRUD-only (Rule 5:
"Foundation. CRUD only."), never calls `run()` or any Explanation/
Knowledge/Memory system.

## Related

- `docs/PHASE64_0_AUDIT.md`, `docs/PHASE64_0_FREEZE.md` — TASK 0's
  audit and the phase this was built in.
- `docs/architecture/AI_FLOW.md`, `docs/ai/AI_PIPELINE.md` — the two
  prose-only documents this phase's `run()` is the first code to
  actually implement.
- `docs/AI_RUNTIME_FLOW.md` — the different, provider-call-survival
  Runtime this module is not.
- `docs/ai/AI_CONTENT.md`, `AI_MEDIA.md`, `AI_BROADCAST.md`,
  `AI_REASONING.md`, `AI_CONVERSATION.md`, `AI_MEMORY.md`,
  `AI_KNOWLEDGE.md` — the eight layers this Runtime composes, each in
  its own depth.
