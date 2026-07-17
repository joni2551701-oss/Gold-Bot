# GoldBot — AI Provider System

Governed by `docs/constitution/CONSTITUTION.md` Article 5 (Provider
Rule). The health/failover/capability-matrix mechanics already live in
`docs/AI_PROVIDER_FOUNDATION.md` (Phase 61.1) — this document states
the real, current provider roster and the contract every one of them
implements, and does not re-derive the health/failover detail.

## The contract

```
BaseAIProvider          ai/providers/base_provider.py
      │
   ┌──┴──┬──────┬──────┐
   │     │      │      │
Gemini OpenAI Claude  Grok
```

**Correction to an earlier brief's assumption**: all four vendor
providers are real today, not three-plus-a-future — `gemini_provider.py`
(Phase 61.2), and `openai_provider.py`/`claude_provider.py`/
`grok_provider.py` (all three, Phase 61.5 TASK 1 "Real Provider
Expansion"). `placeholder_providers.py` remains for any capability a
future provider might cover that none of the four above support yet.

Every provider implements `BaseAIProvider` and returns a
`ProviderResult`. No code outside `ai/providers/` and
`ai/runtime/ai_service.py` ever references a vendor by name
(Constitution Article 5) — not `ai/router/`, not any `Capability`
handler, not `telegram/`.

## Adding, removing, or reordering a vendor

Confined entirely to `ai/providers/` (the provider file itself,
`provider_registry.py`, `provider_capabilities.py`) plus
`ai/router/routing_rules.py`'s declared candidate order. Nothing above
the provider boundary changes.

## Related

- `docs/AI_PROVIDER_FOUNDATION.md` — health tracking, failover
  selection, the capability matrix.
- `docs/ai/AI_RUNTIME.md` — how a provider is actually reached during
  a live request (Circuit Breaker, retry).
- `docs/constitution/CONSTITUTION.md` Article 5.
