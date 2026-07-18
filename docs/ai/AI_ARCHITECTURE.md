# GoldBot — AI Architecture

Governed by `docs/constitution/CONSTITUTION.md` Articles 1, 3, and 5.
This document maps the real `ai/` package as it exists in the
repository today — verified directly via directory listing for this
phase, not transcribed from assumption.

## Real package tree — 21 subpackages under `ai/`

```
ai/
  access/          capability/permission gating for AI requests
  analyzer/        Phase 55 compat entry point -> re-exports ai/ai_analyzer.py
  audit/           provider_stats.py - call/provider auditing, DailyUsage/AI Cost Protection (Phase 62.2)
  cache/           response caching (ResponseCache, cache policy)
  capabilities/    Capability enum + permission matrix
  content/         content_adapter.py - ContentEngine.generate() (real AIService.ask() path,
                   Phase 61.5), extended Phase 63.6 with create()/format()/preview()/validate()/
                   history() (deterministic, no AI call); content_schema.py/content_types.py
                   (ContentRequest/ContentResult/ContentType, Phase 61.5/63.0); models.py/
                   content_adapters.py (Phase 63.6); broadcast_output.py (BroadcastReadyContent,
                   Phase 61.5)
  context/         context_snapshot.py, context_builder.py (signals/context type-only imports)
  conversation/    conversation_engine.py - ConversationEngine.start_session()/ask()
                   (real AIService.ask() path, Phase 61.3), extended Phase 63.5 with
                   append()/summarize()/history()/context()/reset()/close() (deterministic,
                   no AI call); models.py/conversation_adapters.py (Phase 63.5)
  explanation/     explanation_engine.py (signals type-only imports, real AIService.ask() path);
                   explanation_input.py/explanation_output.py/explanation_templates.py/
                   explanation_builder.py/explanation_content_adapter.py (Phase 63.1 -
                   deterministic, template-based, no AI/provider call, no decision/risk import)
  journal/         trade_journal.py (canonical) - AI-side trade journaling
  memory/          context_memory.py/memory_runtime.py (long-term AI memory storage);
                   models.py/memory_registry.py (Phase 63.3 - MemoryEntry contract +
                   MemoryScope catalog, MemoryRuntime extended with store/recall/search)
  profiles/        RuntimeProfile definitions (DEVELOPMENT/TESTING/PRODUCTION)
  prompts/         prompt templates
  providers/       BaseAIProvider, vendor implementations, circuit_breaker.py
  reasoning/       models.py/reasoning_registry.py/reasoning_runtime.py/reasoning_adapters.py
                   (Phase 63.4 - deterministic ReasoningResult store, Knowledge/Memory
                   type-only reads, no ai.explanation import - Intelligence Dependency Principle)
  router/          AIRouter, routing_rules.py
  runtime/         AIService, RuntimeManager, EventBus, self_check.py - production-wired orchestration point (Phase 62.2)
  session/         session/user context for AI product surfaces
  tools/           AI-callable tool definitions (advisory only)
  validation/      response validation, safety.py

  ai_analyzer.py       canonical analyzer (ai/analyzer/ re-exports this)
  ai_prompt.py         prompt construction
  confidence_model.py  AI-side confidence blending helpers (internal to ai/ only - decision/ has its own independent confidence blending in decision_engine.py and does not import this file)
  interfaces.py        AIAnalyzerInterface - the advisory-only contract every future provider must honor
  learning_context.py  learning-context helpers
  trade_journal.py     canonical trade journal (ai/journal/ re-exports this)
```

## Note on the brief's assumption (honest correction)

An earlier task brief referred to "security" and "knowledge" as if
they were subpackages directly under `ai/`. The real repository does
not have either:

- **`knowledge/` is a separate, top-level package** — a sibling of
  `ai/`, not `ai/knowledge/`. It is not part of the AI package tree
  documented here. This same correction recurred in a second Worker
  Brief (Phase 63.2) — see `docs/PHASE63_2_AUDIT.md` — confirming this
  is a stable, standing fact worth stating plainly for any future
  brief: **the real Knowledge Foundation is `knowledge/`, never
  `ai/knowledge/`.**
- **There is no dedicated `ai/security/` folder.** AI-relevant safety
  checks live in `ai/validation/safety.py`; Telegram-side security
  concerns live in `telegram/owner/security.py`, outside `ai/`
  entirely.

Per Constitution Article 7 (Reuse Principle) this document records
what is actually real rather than fabricating folders to match an
assumption — the same discipline `docs/architecture/MODULE_DEPENDENCIES.md`
applies to this identical discrepancy.

## Orchestration entry point

`ai/runtime/ai_service.py`'s `AIService.ask()` is the single real
control-flow entry point, production-wired as of Phase 62.2: it gates
on `RuntimeManager.is_healthy()`, routes through `AIRouter`
(`ai/router/`), attempts a provider (`ai/providers/`) guarded by
`ProviderCircuitBreaker` (with an exponential-backoff wait between
retry attempts — `2 ** attempt` seconds, injectable `sleep_fn`),
validates the result (`ai/validation/`), reads/writes `ai/cache/`,
records to `ai/audit/` (including the previously-unaudited
runtime-unhealthy rejection path), checks AI Cost Protection
(`ai/audit/provider_stats.py`'s `compute_daily_usage()`/
`evaluate_cost_protection()` against an optional
`daily_cost_limit`/`daily_token_limit`), and publishes to
`ai/runtime/event_bus.py`'s `EventBus`. The full sequence diagram
lives in `docs/AI_RUNTIME_FLOW.md`; the Phase 62.2 production-wiring
detail lives in `docs/PHASE62_2_RUNTIME_AUDIT.md` and
`docs/PHASE62_2_RUNTIME_FREEZE.md`.

## Isolation boundary (Constitution Article 3)

Zero `ai/*` → `decision/`/`risk/`/`execution/` imports, verified by
grep sweep at the close of every AI-touching phase. The seven
pre-existing `signals/`/`context/` type-only import sites are the one
standing, audited exception (see
`docs/architecture/IMPORT_RULES.md`).

## Deeper detail per subsystem (Phase 62.1c)

This document maps the package tree; each of these covers one
subsystem's real behavior in depth rather than repeating the tree
above:

- `docs/ai/AI_PIPELINE.md` — the Intelligence-layer composition order
  (Persona → Context → Knowledge → Tools → Conversation → Memory →
  Explanation → Content → Media) and where a request's market context
  actually enters it.
- `docs/ai/AI_MEMORY.md` — `ai/memory/`'s `MemoryRuntime` facade.
- `docs/ai/AI_KNOWLEDGE.md` — `knowledge/`'s 6-category static catalog.
- `docs/ai/AI_REASONING.md` — `ai/reasoning/`'s deterministic
  `ReasoningRuntime` and its Knowledge/Memory/Explanation integration
  points (Phase 63.4).
- `docs/ai/AI_CONVERSATION.md` — `ai/conversation/`'s two surfaces
  (real `AIService.ask()` path plus the deterministic extension) and
  its Knowledge/Memory/Reasoning/Explanation integration points
  (Phase 63.5).
- `docs/ai/AI_CONTENT.md` — `ai/content/`'s two surfaces (real
  `AIService.ask()` path plus the deterministic extension) and its
  Explanation/Conversation integration points (Phase 63.6).
- `docs/ai/AI_TOOLS.md` — `ai/tools/`'s 5 advisory-only tools.
- `docs/ai/AI_RUNTIME.md` — current real Runtime state (Manager,
  Circuit Breaker, Event Bus, Metrics, Cost Protection).
- `docs/ai/AI_PROVIDER_SYSTEM.md` — the real provider roster and the
  `BaseAIProvider` contract they all implement.

## Related documents

- `docs/constitution/CONSTITUTION.md` — Articles 1/3/5 this structure
  must always satisfy.
- `docs/architecture/MODULE_DEPENDENCIES.md` — this same tree in the
  context of the full system dependency map.
- `docs/AI_RUNTIME_FLOW.md` — the detailed request-flow sequence
  through this package (Phase 61.7).
- `ai/README.md` — the package's own top-level README.
