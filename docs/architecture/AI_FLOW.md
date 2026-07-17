# GoldBot — AI Flow

Governed by `docs/constitution/CONSTITUTION.md` Article 1. This
document covers a different flow than `docs/AI_RUNTIME_FLOW.md`:
Runtime Flow is *how a single request survives* (RuntimeManager →
Circuit Breaker → Provider → Cache → Validation → Audit — see
`docs/PHASE62_2_RUNTIME_FREEZE.md` for that flow in full). This
document is *what shape of intelligence a request can draw on* —
the composition of `ai/`'s Intelligence-layer subpackages, built
across Phase 61.3 (AI Intelligence Layer) and Phase 63.0 (Senior
Trading AI Foundation).

## The composition flow

```
Persona                ai/persona/         identity/tone contract (Phase 63.0)
   ↓
Context                ai/context/         context_snapshot.py / context_builder.py
   ↓
Knowledge               knowledge/          top-level package (sibling of ai/, not ai/knowledge/)
   ↓
Tools                    ai/tools/           AI-callable tool definitions, advisory only
   ↓
Conversation              ai/conversation/    multi-turn state
   ↓
Memory                     ai/memory/          long-term AI memory storage
   ↓
Explanation                 ai/explanation/     explanation_engine.py + explanation_output.py
   ↓
Content                      ai/content/         ContentType / ContentRequest / ContentResult (Phase 61.5/63.0)
   ↓
Media                         media/              top-level, Phase 63.0 — MediaType catalog, foundation only
```

This is a **composition** order, not a request's literal call
sequence — not every request touches every layer. A simple
signal-explanation request touches `ai/context/` and
`ai/explanation/` only; a hypothetical future conversational request
would additionally touch `ai/conversation/` and `ai/memory/`. What
this diagram fixes is the *dependency* order: a layer never depends on
one below it in this list (e.g. `ai/explanation/` never imports
`ai/content/`).

## What is real today vs. foundation-only

| Layer | Status |
|---|---|
| `ai/persona/` | Foundation only (Phase 63.0) — one registered persona, never read by a prompt builder yet |
| `ai/context/` | Real — `context_snapshot.py`/`context_builder.py` are live, type-only readers of `signals/`/`context/` |
| `knowledge/` | Built Phase 61.3 — AI Knowledge Foundation |
| `ai/tools/` | Real — AI-callable tool registry, advisory only, never triggers a pipeline action |
| `ai/conversation/` | Built Phase 61.3 — Conversation Engine |
| `ai/memory/` | Built Phase 61.3 — Memory Runtime |
| `ai/explanation/` | Real — `explanation_engine.py`'s three methods (`explain_signal()`/`summarize_report()`/`explain_topic()`); `explanation_output.py`'s `ExplanationOutput` contract (Phase 63.0) is not yet read by the engine |
| `ai/content/` | Real contract (`ContentRequest`/`ContentResult`/`ContentType`), no real generation dispatch yet |
| `media/` | Foundation only (Phase 63.0) — `TEXT` enabled, everything else disabled |

## Where this meets the Runtime

Every one of these subpackages, when it needs to actually call a
provider, goes through `ai/runtime/ai_service.py`'s `AIService.ask()`
— never a direct provider call (Constitution Article 5). See
`docs/AI_RUNTIME_FLOW.md` for that mechanism.

## Related

- `docs/AI_RUNTIME_FLOW.md` — the request-survival mechanism (retry,
  circuit breaker, cache, cost protection).
- `docs/ai/AI_ARCHITECTURE.md` — the full real `ai/` package map, all
  19 subpackages plus the Phase 63.0 top-level additions.
- `docs/roadmap/AI_EVOLUTION.md` — where each of these layers sits on
  the AI Foundation → Senior Trading AI timeline.
- `docs/AI_PERSONA.md`, `docs/AI_CONTENT_FOUNDATION.md`,
  `docs/AI_BROADCAST_FOUNDATION.md` — the Phase 63.0 foundation-only
  layers in detail.
