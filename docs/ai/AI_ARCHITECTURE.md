# GoldBot — AI Architecture

Governed by `docs/constitution/CONSTITUTION.md` Articles 1, 3, and 5.
This document maps the real `ai/` package as it exists in the
repository today — verified directly via directory listing for this
phase, not transcribed from assumption.

## Real package tree — 19 subpackages under `ai/`

```
ai/
  access/          capability/permission gating for AI requests
  analyzer/        Phase 55 compat entry point -> re-exports ai/ai_analyzer.py
  audit/           provider_stats.py - call/provider auditing
  cache/           response caching (ResponseCache, cache policy)
  capabilities/    Capability enum + permission matrix
  content/         content assembly helpers
  context/         context_snapshot.py, context_builder.py (signals/context type-only imports)
  conversation/    multi-turn conversation state
  explanation/     explanation_engine.py (signals type-only imports)
  journal/         trade_journal.py (canonical) - AI-side trade journaling
  memory/          long-term AI memory storage
  profiles/        RuntimeProfile definitions (DEVELOPMENT/TESTING/PRODUCTION)
  prompts/         prompt templates
  providers/       BaseAIProvider, vendor implementations, circuit_breaker.py
  router/          AIRouter, routing_rules.py
  runtime/         AIService, RuntimeManager, EventBus, self_check.py - orchestration point
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
  documented here.
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
control-flow entry point as of Phase 61.7: it gates on
`RuntimeManager.is_healthy()`, routes through `AIRouter`
(`ai/router/`), attempts a provider (`ai/providers/`) guarded by
`ProviderCircuitBreaker`, validates the result
(`ai/validation/`), reads/writes `ai/cache/`, records to
`ai/audit/`, and publishes to `ai/runtime/event_bus.py`'s `EventBus`.
The full sequence diagram lives in `docs/AI_RUNTIME_FLOW.md`.

## Isolation boundary (Constitution Article 3)

Zero `ai/*` → `decision/`/`risk/`/`execution/` imports, verified by
grep sweep at the close of every AI-touching phase. The seven
pre-existing `signals/`/`context/` type-only import sites are the one
standing, audited exception (see
`docs/architecture/IMPORT_RULES.md`).

## Related documents

- `docs/constitution/CONSTITUTION.md` — Articles 1/3/5 this structure
  must always satisfy.
- `docs/architecture/MODULE_DEPENDENCIES.md` — this same tree in the
  context of the full system dependency map.
- `docs/AI_RUNTIME_FLOW.md` — the detailed request-flow sequence
  through this package (Phase 61.7).
- `ai/README.md` — the package's own top-level README.
