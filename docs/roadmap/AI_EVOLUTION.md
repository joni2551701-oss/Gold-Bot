# GoldBot — AI Evolution Timeline

Governed by `docs/constitution/CONSTITUTION.md` Article 1. At every
stage on this timeline, the AI layer's role stays advisory-only — the
timeline describes how much the AI can *explain*, never a step toward
the AI *deciding*. Per the Phase 62.1c ruling, this document is
**Future Vision** — real, current build status lives in
`docs/roadmap/VERSIONS.md` and each phase's own Freeze document, not
here.

**Restructured Phase 62.1d** (Director-instructed, TASK 3) into five
named stages, replacing the prior six-stage list. This restructure
also resolves the Phase 62.1b audit finding that flagged the old
"AI Intelligence"/"AI Assistant" stages as possibly stale: their real
content (Phase 61.3's `knowledge/`, `ai/conversation/`, `ai/memory/`,
`ai/tools/`, `ai/explanation/` work) is now correctly folded into
Stage 1 below as DONE.

```
Stage 1: AI Assistant Foundation → Stage 2: AI Runtime Intelligence
   → Stage 3: AI Market Analyst → Stage 4: AI Media Intelligence
   → Stage 5: Senior Trading AI Ecosystem
```

## Stage definitions

### Stage 1 — AI Assistant Foundation — DONE
Providers (`ai/providers/`), router (`ai/router/`), capability model
(`ai/capabilities/`), caching and auditing (Phases 59–61.2), plus the
real Intelligence-layer components Phase 61.3 built on top of that
foundation: `knowledge/` (6-category static catalog), `ai/conversation/`
(multi-turn state), `ai/memory/` (`MemoryRuntime`), `ai/tools/` (5
advisory-only tools), `ai/explanation/` (`ExplanationEngine`). See
`docs/ai/AI_KNOWLEDGE.md`, `docs/ai/AI_MEMORY.md`, `docs/ai/AI_TOOLS.md`,
`docs/ai/AI_PIPELINE.md` for each piece's current real detail.

Phase 63.1 added a second, complementary explanation path inside the
same package: `ExplanationBuilder` (`ai/explanation/explanation_builder.py`)
is deterministic and template-based — no `AIService`/provider call at
all — turning already-extracted primitive values
(`ExplanationInput`) into a structured `ExplanationOutput` (WHY/WHAT/
WHERE/RISK/INVALIDATION for trades, plus No-Trade and Education
templates). It never imports `decision/`/`risk/`; a caller such as
`core/pipeline.py` extracts the primitives first. See
`docs/PHASE63_1_FREEZE.md`.

### Stage 2 — AI Runtime Intelligence — DONE
`RuntimeManager`, `ProviderCircuitBreaker`, `RuntimeProfile`,
`EventBus` built (61.6) and wired into `AIService.ask()`'s real
control flow (61.7), then production-hardened with retry backoff,
cost protection, and full Owner runtime control (62.2). See
`docs/ai/AI_RUNTIME.md` and `docs/AI_RUNTIME_FLOW.md`.

### Stage 3 — AI Market Analyst — PLANNED
Broader analytical surfaces — trend/performance summaries over
history the AI reads but never acts on, feeding the Owner-facing
`docs/owner/OWNER_PANEL.md` analytics section. No dedicated module
exists yet; this is a planned extension of Stage 1's Explanation
Engine, not a new architectural layer.

### Stage 4 — AI Media Intelligence — PLANNED
Weekly Outlook, Education, Market Room, Trade Replay — see this
document's own "AI Media Intelligence Platform" section below for the
detailed vision. Phase 63.0 already built the **foundation/contract**
layer (`ai/persona/`, `ai/content/`'s `ContentType`,
`ai/explanation/explanation_output.py`, `broadcast/`, `media/`,
`translation/`) — PLANNED here refers to the real generation/delivery
logic on top of that foundation, which does not exist yet
(`docs/policies/BROADCAST_POLICY.md`).

### Stage 5 — Senior Trading AI Ecosystem — FUTURE
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
