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

## AI Media Intelligence Platform (roadmap vision, Phase 62.1b)

Recorded here as Director-approved roadmap vision only — **no code,
no new module, no new capability**. This section names a future
direction on top of the Phase 63.0 Senior Trading AI Foundation
(`ai/persona/`, `ai/content/`, `broadcast/`, `media/`, `translation/`),
not a phase in progress. Every item below still operates inside
Article 1's permanent boundary: explaining and educating, never
deciding or executing.

```
Education Content → Weekly Outlook → Market Room → Trade Replay → (future) Voice/Video/Avatar/Multi-channel
```

**Education Content** — SMC (Smart Money Concepts) education, XAUUSD
analysis walkthroughs, general market lessons. Maps to
`ContentType.EDUCATION` (already defined, Phase 63.0).

**Weekly Outlook** — macro view, technical view, scenario planning,
risk framing for the coming week. Maps to `ContentType.WEEKLY_OUTLOOK`
(already defined, Phase 63.0).

**Market Room** — live-session-style analysis and setup explanation,
read-only over already-decided pipeline output, same as every other
AI surface (Constitution Article 1).

**Trade Replay** — a specific content flow over a trade's own
lifecycle:

```
Before trade → Decision → Execution → Result → AI Review
```

`AI Review` here means an `ExplanationOutput` built from a *closed*
trade's own history (`lifecycle/`, `analytics/`) — never a live signal
the AI could influence before it resolves.

**Future (unscoped, no target phase)** — voice, video, an AI avatar,
and delivery to YouTube/TikTok/Telegram Video. Every one of these
requires its own separately-approved phase and its own Foundation
Reuse Audit (Constitution Article 11) before a single line of code —
none of them exist today, and `broadcast/`'s `BroadcastProviderType`
enum vocabulary (Phase 63.0) is not itself a connection to any of
these platforms (`docs/policies/BROADCAST_POLICY.md`).

## Related documents

- `docs/roadmap/VERSIONS.md` — where each AI stage lands in the
  overall version roadmap.
- `docs/constitution/CONSTITUTION.md` Article 1 — the permanent
  boundary every stage above operates inside.
- `docs/ai/AI_ARCHITECTURE.md` — the real package structure the
  Intelligence/Assistant/Analyst stages will extend.
- `docs/AI_CONTENT_FOUNDATION.md`, `docs/AI_BROADCAST_FOUNDATION.md` —
  the real Phase 63.0 foundation this vision section builds on top of.
