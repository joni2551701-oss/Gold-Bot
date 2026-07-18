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

Phase 63.2 extended `knowledge/` (the real package — a top-level
sibling of `ai/`, not `ai/knowledge/`) with `KnowledgeManager`, a
class-based lookup/search/filter facade over the existing static
catalog, plus an optional `source` provenance field on `KnowledgeEntry`.
See `docs/PHASE63_2_FREEZE.md`.

Phase 63.3 extended `ai/memory/memory_runtime.py`'s `MemoryRuntime`
(LOCKed since Phase 61.3) with a second, structured surface —
`store()`/`recall()`/`search()`/`filter()`/`list_all()`/`short_term()`/
`long_term()`/`forget()` over a new `MemoryEntry` contract
(`ai/memory/models.py`: `MemoryType`/`MemoryPriority`/`MemoryScope`)
and a new `ai/memory/memory_registry.py` static catalog of the six
`MemoryScope` categories — alongside, not replacing, the original
`save`/`load`/`clear`/`clear_all`/`MemoryLayer` surface. See
`docs/PHASE63_3_FREEZE.md`.

Phase 63.4 built `ai/reasoning/` (Foundation Reuse Audit found no
existing Reasoning module — the one Phase 63.x sub-phase so far that
created a genuinely new subpackage rather than extending one):
`ReasoningRuntime` (`reason`/`explain`/`summarize`/`evaluate`/
`compare`/`chain`/`history`, all deterministic — no LLM, no inference
computed by this module itself) over a primitive-only `ReasoningResult`/
`ReasoningStep` contract, plus `reasoning_adapters.py`'s type-only
reads from `KnowledgeEntry`/`MemoryEntry` (upstream) and a
dict-only, no-import bridge toward `ExplanationInput`'s shape
(downstream — never imported). See `docs/PHASE63_4_FREEZE.md`.

Phase 63.5 extended `ai/conversation/conversation_engine.py`'s
`ConversationEngine` (LOCKed since Phase 61.3) with a second,
deterministic surface — `append()`/`summarize()`/`history()`/
`context()`/`reset()`/`close()` — alongside its original, unchanged
`start_session()`/`ask()` (the latter a real `AIService.ask()`/LLM
call). No second Conversation class was created; Foundation Reuse
Audit found `ConversationEngine` already existed, so Constitution
Article 11 forbade a competing one. `conversation_adapters.py` adds
type-only reads from `KnowledgeEntry`/`MemoryEntry`/`ReasoningResult`
(all upstream) and a dict-only bridge toward `ExplanationInput`'s
shape (downstream — never imported). See `docs/PHASE63_5_FREEZE.md`.

Phase 63.6 extended `ai/content/content_adapter.py`'s `ContentEngine`
(LOCKed since Phase 61.5) with a second, deterministic surface —
`create()`/`format()`/`preview()`/`validate()`/`history()` — alongside
its original, unchanged `generate()` (a real `AIService.ask()`/LLM
call). No second Content class was created; Foundation Reuse Audit
found `ContentEngine` already existed, so Constitution Article 11
forbade a competing one. `content_adapters.py` adds type-only reads
from `ExplanationOutput`/`ConversationContext` (both upstream) — never
imports `translation/`/`media/`/`broadcast/` (downstream). `ContentType`
gained one additive member, `TRADE_REPLAY`. See
`docs/PHASE63_6_FREEZE.md`.

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

## Phase 63.x — AI Intelligence Layer sub-phases (Director Decision, Phase 63.3)

Formalized here per the Director's own Phase 63.3 decision, so no
future Worker Brief needs to re-derive or re-number this sequence.
Each sub-phase is its own Foundation Reuse Audit + Freeze cycle inside
Stage 1/3 above, not a separate top-level Stage:

```
63.0  Foundation                DONE
63.1  Explanation                DONE
63.2  Knowledge                  DONE
63.3  Memory                     DONE
63.4  Reasoning                  DONE
63.5  Conversation                DONE
63.6  Content                     DONE
63.7  Media                       next
63.8  Broadcast
```

`63.4 Reasoning` was inserted between Memory and Conversation by the
Director's own Phase 63.3 decision — "AI shu bilimlarni qanday
bog'laydi" (how the AI connects what it knows), the layer that makes
Knowledge + Memory useful to Conversation and Explanation. Built Phase
63.4: `ai/reasoning/` (`ReasoningRuntime`, deterministic
store/read only — no LLM, no inference computation of its own). See
`docs/PHASE63_4_FREEZE.md`.

Built Phase 63.5: `ai/conversation/`'s `ConversationEngine` extended
with a deterministic surface, alongside its original real-`AIService.ask()`
path. See `docs/PHASE63_5_FREEZE.md`.

Built Phase 63.6: `ai/content/`'s `ContentEngine` extended with a
deterministic surface, alongside its original real-`AIService.ask()`
path; `ai/content/models.py` (`ContentMode`/`ContentMetadata`/
`ContentContext`) and `content_adapters.py` (Explanation/Conversation
type-only reads) added. See `docs/PHASE63_6_FREEZE.md`.

## Official Intelligence Pipeline (Director Decision, Phase 63.3)

The AI Core's real, ordered composition, as of the Phase 63.3 Director
Decision — supersedes any earlier, less specific composition order
this document previously implied:

```
Market → Knowledge → Memory → Reasoning → Conversation → Explanation
   → Content → Translation → Media → Broadcast
```

**Explanation is a position in this chain, not a standalone module.**
It is the output of Knowledge + Memory + Reasoning + Conversation
working together, never a decision-maker of its own — this does not
change anything about `ai/explanation/explanation_builder.py`'s actual
code (it still accepts primitive `ExplanationInput` values directly,
per its own Phase 63.1 Director Decision); it changes how this
pipeline's *future* stages are expected to feed it. Every stage in
this chain remains bound by Constitution Article 1: explain, never
decide.

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
