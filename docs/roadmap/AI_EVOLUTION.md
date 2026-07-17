# GoldBot — AI Evolution Timeline

Governed by `docs/constitution/CONSTITUTION.md` Article 1. At every
stage on this timeline, the AI layer's role stays advisory-only — the
timeline describes how much the AI can *explain*, never a step toward
the AI *deciding*.

```
AI Foundation → AI Runtime → AI Intelligence → AI Assistant
     → AI Analyst → Senior Trading AI
```

## Stage definitions

### AI Foundation (Phases 59–61.5) — Done
Providers (`ai/providers/`), router (`ai/router/`), capability model
(`ai/capabilities/`), basic caching and auditing. The AI could answer
isolated requests but had no unified reliability layer.

### AI Runtime (Phase 61.6–61.7) — Done
`RuntimeManager`, `ProviderCircuitBreaker`, `RuntimeProfile`,
`EventBus` built (61.6) and then wired into `AIService.ask()`'s real
control flow (61.7), making `AIService` the single orchestration
point: runtime health gating, circuit-breaker failover, profile-driven
validation/cache/retry policy, and event publication all real and
tested. See `docs/AI_RUNTIME_FLOW.md` for the full request sequence.

### AI Intelligence — Not started
Deeper context reasoning over `ai/context/`, `ai/memory/`, richer
`ai/explanation/` output — the AI explains *why* a signal looks the
way it does with more of the pipeline's own context available to it,
still strictly read-only over pipeline output.

### AI Assistant — Not started
Multi-turn conversational continuity (`ai/conversation/`,
`ai/session/`) — a user can ask follow-up questions about a signal or
their own trade history and get consistent, context-aware answers
across turns.

### AI Analyst — Not started
Broader analytical surfaces — trend/performance summaries over
history the AI reads but never acts on, feeding the Owner-facing
`docs/owner/OWNER_PANEL.md` analytics section.

### Senior Trading AI — Not started
The most capable stage on this timeline, and still bound by
Constitution Article 1: even at this stage, the AI layer's ceiling is
explaining a decision with full context and history, not making one.
Any future proposal to let the AI vote, approve, or execute is not an
evolution of this timeline — it is a Constitutional Amendment, and
requires the explicit, dedicated Director process Article 1 and the
Amendment section describe.

## Related documents

- `docs/roadmap/VERSIONS.md` — where each AI stage lands in the
  overall version roadmap.
- `docs/constitution/CONSTITUTION.md` Article 1 — the permanent
  boundary every stage above operates inside.
- `docs/ai/AI_ARCHITECTURE.md` — the real package structure the
  Intelligence/Assistant/Analyst stages will extend.
