# Phase 64.0 — AI Intelligence Integration Layer: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/architecture/*`,
`docs/roadmap/*`, `docs/ai/*`) before any code change, per this
phase's own Rule 2.

## The critical question: does an Intelligence Runtime/Orchestrator already exist?

**No.** A direct search (`ai/pipeline*.py`, `**/intelligence*.py`,
`ai/**/orchestrat*.py`, plus a full listing of `ai/`'s 21 subpackages
and every top-level sibling) finds nothing that composes Knowledge →
Memory → Reasoning → Conversation → Explanation → Content → Media →
Broadcast into one callable sequence. Two documents describe this
composition *order* in prose, but neither is backed by orchestrating
code:

- `docs/architecture/AI_FLOW.md` (Phase 62.1b) — a **stale** diagram:
  its own chain stops at `media/` and never mentions `ai/reasoning/`
  or `broadcast/` (both added Phase 63.4/63.0 respectively, after this
  doc was written). No code implements the chain it draws.
- `docs/ai/AI_PIPELINE.md` (Phase 62.1c) — documents only where a
  request's *market context* enters the chain via
  `ai/context/context_adapter.py`; it explicitly defers to `AI_FLOW.md`
  for the rest and, likewise, is prose only.

`ai/runtime/ai_service.py`'s `AIService`/`RuntimeManager` is a
**different** runtime — it survives one provider call (routing,
circuit breaker, cache, retry, cost protection; see
`docs/AI_RUNTIME_FLOW.md`), not a composer of the eight Intelligence
layers. It is not a candidate for extension here; TASK 1's orchestrator
is a distinct, new, single-purpose module, and Article 11 is satisfied
because both the audit's own targeted search and this cross-check
against the one existing "Runtime" name in the codebase confirm no
prior module owns this responsibility.

## Foundation Reuse Audit — per layer (Rule 2's own required table)

Every layer's real Foundation/Manager/Model/Contract/Runtime/Registry
already exists, fully deterministic-callable without any LLM call —
confirmed by re-reading each manager's own source this phase:

| Layer | Foundation/Manager | Deterministic entry point(s) used | Adapter(s) reused |
|---|---|---|---|
| Knowledge | `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py`'s `KnowledgeManager` | `search(query) -> Sequence[KnowledgeEntry]` | — |
| Memory | `ai/memory/memory_runtime.py`'s `MemoryRuntime` | `store(MemoryEntry)`, `recall(key)` | — |
| Reasoning | `ai/reasoning/reasoning_runtime.py`'s `ReasoningRuntime` | `reason(ReasoningResult)` | `ai/reasoning/reasoning_adapters.py`'s `step_from_knowledge_entry()`, `reasoning_result_to_explanation_fields()` |
| Conversation | `ai/conversation/conversation_engine.py`'s `ConversationEngine` | `start_session()`, `append()` (never `ask()`) | — |
| Explanation | `ai/explanation/explanation_builder.py`'s `ExplanationBuilder` | `build(ExplanationInput) -> ExplanationOutput` (template-based, no `AIService` call) | — |
| Content | `ai/content/content_adapter.py`'s `ContentEngine` | `create(...)` (never `generate()`) | — |
| Media | `media_layer/content_manager/media_manager.py`'s `MediaManager` | `create_asset()`/`prepare_asset()` (never `.render()` — doesn't exist) | `media_layer/content_manager/media_pipeline.py`'s `prepare_media_from_content()` (Phase 63.7) |
| Broadcast | `media_layer/telegram_broadcast/broadcast_manager.py`'s `BroadcastManager` | `create_broadcast()`/`prepare_broadcast()` (never send/publish/deliver — don't exist) | `media_layer/telegram_broadcast/broadcast_adapter.py`'s `broadcast_asset_from_content_and_media()` (Phase 63.8) |

**Decision (Rule 3/TASK 1): the orchestrator composes these eight
existing entry points and their existing cross-layer adapters — it
adds zero new business logic to any of them, and creates no
`KnowledgeManager2`/`MemoryEngine`/`ConversationService`-style
parallel class (Rule 3's own explicit examples of what not to build).**

## TASK 1's location decision

Per Rule 5/Module Reuse Principle step 2, before creating anything new:
is there an existing file this belongs in? No single existing file
owns "compose all eight layers" — each layer's own file owns only its
own layer. A new top-level `ai/intelligence/` **package** is
unwarranted (Rule/TASK 1's own instruction: "shoshilmang... faqat
bitta orchestrator") since the entire deliverable is one class in one
file, not a multi-file subsystem. **Decision: one new file,
`ai_layer/ai_engine/intelligence_runtime.py`**, matching this codebase's own
established convention for a single-purpose top-level module directly
under `ai/` (`ai_layer/ai_engine/ai_analyzer.py`, `ai_layer/ai_engine/ai_prompt.py`,
`ai_layer/confidence_ai/confidence_model.py`, `ai_layer/ai_service/interfaces.py`,
`ai_layer/knowledge_ai/learning_context.py`, `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` — none of these are
subpackages either).

## Why this one file may import every layer (an explicit, narrow exception)

Every individual layer's own isolation is unchanged and remains tested
(each layer still only imports its upstream layers — Broadcast still
cannot import Reasoning directly, etc.; TASK 5 adds a permanent AST
test for this). `ai_layer/ai_engine/intelligence_runtime.py` is different in kind: it
is the **composition root** for the Intelligence layer, the same role
`core/pipeline.py` already plays for the Trading layer (which itself
legitimately imports `data/`, `context/`, `strategies/`, `signals/`,
`decision/`, `risk/`, `execution/` — every trading layer — to
orchestrate them in order). A composition root importing every layer
it composes is not a violation of the Intelligence Dependency
Principle; it is the one place that principle's own ordering is
enforced in code rather than only in documentation. `IntelligenceRuntime`
is placed under `ai/`, never `core/` — Rule 1 forbids touching `core/`
at all this phase, and `core/pipeline.py`'s own trading composition is
completely untouched.

## Dependency Compliance (Rule 3)

`ai_layer/ai_engine/intelligence_runtime.py` imports: `ai_layer.knowledge_ai.knowledge_base.knowledge_manager`,
`ai_layer.knowledge_ai.memory_manager.memory_runtime`/`models`, `ai_layer.ai_engine.reasoning.reasoning_runtime`/
`models`/`reasoning_adapters`, `ai_layer.personal_ai.interaction_manager.conversation_engine`,
`ai_layer.explanation_ai.explanation_builder`/`explanation_input`,
`ai_layer.ai_service.content.content_adapter`/`content_types`, `media_layer.content_manager.media_manager`/
`media_pipeline`/`media_types`, `media_layer.telegram_broadcast.broadcast_manager`/
`broadcast_adapter`. It never imports `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `database/`, or `telegram/`
(TASK 5's isolation test enforces this permanently) — the same zero
trading-layer dependency every Phase 61.x–63.x AI module has held.

## Trading Core Isolation

`git diff --stat -- core/ decision/ risk/ execution/ strategies/
signals/` — zero output before any change this phase.

## Conclusion

No Constitution Article conflict. TASK 1–3 (one new orchestrator file,
a primitive `PipelineStage`/`PipelineStageResult` contract, a
stub — deterministic-only, zero-LLM-call — `run()` method walking all
eight layers in Official Intelligence Pipeline order) is the one
genuine piece of new work this phase does. No existing module is
duplicated; every layer's own Manager/Runtime/Engine/Builder is called
exactly as its own phase already built it. Requesting no Director
Decision.
