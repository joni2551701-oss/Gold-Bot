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
63.7  Media                       DONE
63.8  Broadcast                   DONE
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

Built Phase 63.7: top-level `media/`'s `MediaManager` (a sibling of
`ai/`, not `ai/media/` — see `docs/PHASE63_7_AUDIT.md`) extended with
a deterministic `MediaAsset` surface, alongside its original Owner
ENABLED/DISABLED intent tracking; `media/models.py` (`MediaAsset`/
`MediaAssetStatus`), `media_adapter.py`/`media_pipeline.py` (Content
type-only reads) added. See `docs/PHASE63_7_FREEZE.md`.

Built Phase 63.8: top-level `broadcast/`'s `BroadcastManager` (a
sibling of `ai/`, not `ai/broadcast/` — see `docs/PHASE63_8_AUDIT.md`)
extended with a deterministic `BroadcastAsset` surface, alongside its
original `would_broadcast()`/`prepare()`; `broadcast/models.py`
(`BroadcastStatus`/`BroadcastAsset`, plus `TELEGRAM`/`MINI_APP`
provider types and `BroadcastTriggerType`), `broadcast_adapter.py`
(Content/Media type-only reads, optional Persona reference) added.
This closes the `63.0`–`63.8` AI Intelligence Layer sub-phase
sequence — Broadcast is the pipeline's terminal layer; no real
delivery exists yet. See `docs/PHASE63_8_FREEZE.md`.

Built Phase 64.0 — **AI Intelligence Integration Layer**, the first
phase after the `63.0`–`63.8` sequence closed: `ai/intelligence_runtime.py`'s
`IntelligenceRuntime`, the first orchestrator to actually call all
eight layers (`Knowledge → Memory → Reasoning → Conversation →
Explanation → Content → Media → Broadcast`) in sequence, deterministic
only, zero LLM calls. No new Foundation, no new parallel Manager —
every stage calls that layer's own existing entry point. See
`docs/PHASE64_0_FREEZE.md`.

Built Phase 65.0 — **AI Voice Intelligence Foundation**, the first
phase in a new `65.x` Voice sub-sequence: top-level `voice/` (a
genuine new sibling of `ai/`, unlike the `63.7`/`63.8` naming
corrections — see `docs/PHASE65_0_AUDIT.md`), `VoiceManager`/
`VoiceProfileRegistry`/`VoiceRuntime`, static Profile catalog
(Senior/Seniorita/Narrator) and Provider catalog (OpenAI/ElevenLabs/
Local/Custom), all metadata-only — no STT, no TTS, no real API call,
no LLM call. See `docs/PHASE65_0_FREEZE.md`.

Built Phase 65.1 — **AI Voice Provider Integration**: real
`OpenAIVoiceProvider`/`ElevenLabsVoiceProvider` TTS adapters
(`voice/provider_adapters/`, real HTTP via `requests`, gated on
`core/secrets.py`'s `OPENAI_API_KEY`/new `ELEVENLABS_API_KEY`),
`LocalVoiceProvider`/`CustomVoiceProvider` skeletons,
`VoiceProviderContract` (`voice/provider_contract.py`), per-profile
provider selection and adapter registry (extends `VoiceManager`, no
duplicate Manager), fallback handling (extends `VoiceRuntime`), and
three new Content-sibling integration adapters
(`media_asset_to_voice_request()`/`broadcast_asset_to_voice_request()`/
`conversation_turn_to_voice_request()`, extends `voice/adapter.py`).
Voice is now the terminal narrating stage of the Official Intelligence
Pipeline below. See `docs/PHASE65_1_FREEZE.md`.

Built Phase 65.2 — **AI Voice Conversation Intelligence**: the first
real, LLM-backed "user speaks → AI understands → AI replies by voice"
round trip. `voice/stt/` (real `OpenAISTTProvider` via OpenAI's Whisper
REST endpoint, `LocalSTTProvider`/`CustomSTTProvider` skeletons,
`STTProviderContract`, `STTManager` single active-provider selection —
mirrors `voice/provider_adapters/`'s Phase 65.1 shape for the opposite
direction); `voice/intents/` (`VoiceIntent`, deterministic keyword
`detect_intent()`, metadata only); `voice/session/` (`VoiceSession`/
`VoiceSessionManager`, a genuinely different session concept from
`ai/session/`'s `ConversationState`, linked by a
`conversation_session_id` pointer); `voice/conversation_bridge.py`'s
`handle_voice_turn()` — the second composition-root exception in this
codebase (the first is `ai/intelligence_runtime.py`, Phase 64.0, which
stays deliberately deterministic) — composes STT → intent detection →
the *existing*, unmodified `ConversationEngine.ask()` (real call) →
the *existing*, unmodified `VoiceRuntime.generate_audio()`/
`generate_with_fallback()`. Zero new business logic in any of the four
systems it composes. `voice/` still never imports `ai.memory`/
`ai.reasoning`/`ai.explanation`/top-level `knowledge` directly,
anywhere, with zero exemptions (Phase 65.2's own Rule 2). See
`docs/PHASE65_2_FREEZE.md`.

Built Phase 65.3 — **Personal AI Assistant Foundation**: top-level
`assistant/` (`IdentityManager`/`AssistantIdentity`/
`identity_registry.py`: Senior/Seniorita presentation metadata,
deliberately not `ai.persona.Persona` — Rule 3 Persona Protection),
`AssistantManager` (per-user `AssistantProfile` CRUD, Owner-only via
`assistant/access.py`'s `is_personal_ai_enabled_for()`, deliberately
*not* `ai/access/access_control.py`'s matrix since that grants ADMIN
equally), and `assistant/conversation_adapter.py`'s three structural
(not real-call) Conversation/Voice/Memory integration points. The
brief's own diagram places Assistant *before* Conversation in the
Official Intelligence Pipeline below, so — applying the Intelligence
Dependency Principle literally one layer earlier than it has ever been
applied — `assistant/` imports nothing downstream of it: not `voice/`,
not `ai.conversation/`, not `ai.memory/`, not `ai.persona/`. See
`docs/PHASE65_3_FREEZE.md`.

Built Phase 65.4 — **Personal AI Runtime Integration**: connects the
Phase 65.3 Foundation to the real Runtimes it deliberately never
imported before. `AssistantManager` extended in place with
`AssistantRuntime` lifecycle methods (`create_runtime()`/
`load_runtime()`/`restore_runtime()`/`close_runtime()`/
`runtime_status()`, all Owner-gated, no new Manager). New
`assistant/runtime_adapter.py` — the third composition-root-shaped
file in this codebase (after `ai/intelligence_runtime.py` and
`voice/conversation_bridge.py`) — is the one file in `assistant/`
permitted to import `ai.conversation.conversation_engine`,
`ai.intelligence_runtime`, `ai.memory.memory_runtime`, and
`voice.runtime`: `advance_conversation()` (real `ConversationEngine.ask()`),
`synthesize_voice()` (real `VoiceRuntime.generate_audio()`/
`generate_with_fallback()`), `remember_turn()`/`recall_turn()` (real
`MemoryRuntime.store()`/`recall()`), `run_intelligence_pipeline()`
(reuses `IntelligenceRuntime.run()` as-is — Reasoning is reached only
through it), and `run_personal_ai_turn()` composing the full round
trip. Zero new business logic in any of the five systems it composes;
every other file in `assistant/` keeps Phase 65.3's zero-downstream-
import posture unchanged. See `docs/PHASE65_4_FREEZE.md`.

```
65.0  Voice Foundation                    DONE
65.1  Voice Provider Integration          DONE
65.2  Voice Conversation Intelligence     DONE
65.3  Personal AI Assistant Foundation    DONE
65.4  Personal AI Runtime Integration     DONE
66.0  AI Trading Analyst Foundation       DONE
66.1  Chart Intelligence Foundation       DONE
66.2  Trade Journal Intelligence Foundation DONE
66.3  Learning Intelligence Foundation     DONE
66.4  Coaching Intelligence Foundation     DONE
66.5  Performance Intelligence            FUTURE (not yet briefed)
66.6  Strategy Intelligence               FUTURE (not yet briefed)
66.7  Portfolio Intelligence              FUTURE (not yet briefed)
66.8  Research Intelligence               FUTURE (not yet briefed)
```

Built Phase 66.0 — **AI Trading Analyst Foundation**, the first phase
in a new `66.x` AI Trading Intelligence sub-sequence: new
`ai/trading_analyst/` subpackage (inside the already-existing `ai/`
top-level package, confirmed by `docs/PHASE66_0_AUDIT.md`'s TASK 0
audit). `TradingAnalysisInput`/`TradingAnalysis`/`TradingRiskLevel`
(`models.py`) — a primitive-only contract resolving the tension
between the brief's own diagram (which implies reading live
`TradeDecision`/`RiskResult` objects) and Constitution Article 3's
absolute rule that `ai/` never imports `decision/`/`risk/`/
`execution/`, following the exact precedent
`ai/explanation/explanation_input.py`'s own `ExplanationInput` already
established. `TradingAnalystRuntime.analyze()`
(`analyst_runtime.py`) composes two real, unmodified systems —
`IntelligenceRuntime.run()` (Phase 64.0, grounding only) and
`ExplanationBuilder.build()` (Phase 63.1, TRADE-mode) — zero new
business logic; Owner-gated via a dedicated `enable_trading_analyst`
feature flag (`access.py`), deliberately not routed through
`ai/access/access_control.py`'s `AccessControl` matrix. `recommendation`
("WHY BUY/SELL/WAIT/SKIP") always echoes the already-decided
`direction` it received, never invents a new verdict (Director Note
1). `content_adapter.py` composes the existing Content → Media →
Broadcast pipeline (`ContentType.LIVE_ANALYSIS` reused as-is, no new
`ContentType`) — the one file in the package permitted to import
`ai.content/`, `media/`, `broadcast/`. Zero diff in `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`,
`monitoring/` this phase (Rule 1). Not wired into `core/pipeline.py`
or any Telegram command — foundation only. See
`docs/PHASE66_0_FREEZE.md`.

Built Phase 66.1 — **AI Chart Intelligence Foundation**, the second
phase in the `66.x` AI Trading Intelligence sub-sequence: new
`ai/chart_intelligence/` subpackage (inside the already-existing `ai/`
top-level package, confirmed by `docs/PHASE66_1_AUDIT.md`'s TASK 0
audit) — the *chart interpretation layer* the Director's own framing
names: a single deterministic pipeline a future phase would route
TradingView screenshots, MT5 screenshots, Telegram images, and PDF
charts through uniformly (`ChartImageType`), not a single-screenshot
tool. `ChartAnalysisInput`/`ChartAnalysis`/`ChartContext` (`models.py`)
are primitive-only, following the same Article 3 resolution
`ai/trading_analyst/models.py` already established — `ChartContext`
never stores image bytes, only a content-hash reference. `ChartRuntime`
(`chart_runtime.py`) is a pure relay/transform composing the existing,
unmodified `ExplanationBuilder` in `EDUCATION` mode — no Vision API,
LLM, or image recognition model call anywhere in this phase (Rule 4).
`trading_analyst_adapter.py` composes an existing `TradingAnalysis`
(Phase 66.0) with this phase's own `ChartAnalysis` into a combined
Explanation — the pipeline's own "TradingAnalyst → ChartAnalysis →
Explanation" order, the one file permitted to import
`ai.trading_analyst`. `content_adapter.py` reuses the existing
Content → Media → Broadcast pipeline (`ContentType.LIVE_ANALYSIS`
reused a second time, `MediaType.IMAGE` reused as-is).
`vision_provider_types.py`'s `ChartVisionProviderType` is pure
future-compatible vocabulary (OpenAI/Gemini/Claude/Local Vision) — no
provider wired, no API call. Owner-only via a dedicated
`enable_chart_intelligence` flag. Zero diff in `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, `monitoring/`
this phase (Rule 1). Not wired into `core/pipeline.py` or any Telegram
command — foundation only. See `docs/PHASE66_1_FREEZE.md`.

Built Phase 66.2 — **AI Trade Journal Intelligence Foundation**, the
third phase in the `66.x` AI Trading Intelligence sub-sequence: new
`ai/trade_journal/` subpackage (inside the existing `ai/` top-level
package, confirmed by `docs/PHASE66_2_AUDIT.md`'s TASK 0 audit —
which also reviewed the pre-existing, Trading-Core-coupled
`ai.journal.trade_journal.TradeJournalEntry`, Phase 55, and
DB-persisted `learning.models.LearningRecord`, Phase 60.6/60.7,
neither reusable for this phase's own primitive-only, in-memory
mandate). `TradeJournalEntry`/`ReplayContext` (`models.py`) are
primitive-only, `chart_id`/`trade_id` mandatory links (Director Note
4) — this same phase also extended the Phase 66.1 LOCKed
`ChartAnalysis` with one new, additive `chart_id` field
(LOCK-permitted extension). `TradeJournalRuntime`
(`journal_runtime.py`) is CRUD-only —
`create()`/`get()`/`list()`/`update_notes()`, in-memory dict, no
database (Rule 3), no statistics/analytics of any kind (Rule 4;
win rate/Sharpe/profit factor/drawdown belong to a future 66.5).
`trading_analyst_adapter.py` composes an existing `TradingAnalysis`
(66.0) and `ChartAnalysis` (66.1) into a `TradeJournalEntry` — the
pipeline's own "TradingAnalysis → ChartAnalysis → TradeJournal" order.
`memory_adapter.py`'s `memory_reference_key()` never imports
`ai.memory` at all (Rule 6 — Memory itself never changes). Owner-only
via a dedicated `enable_trade_journal` flag. Zero diff in `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`,
`monitoring/` this phase (Rule 1). Not wired into `core/pipeline.py`
or any Telegram command — foundation only. See
`docs/PHASE66_2_FREEZE.md`.

Built Phase 66.3 — **AI Learning Intelligence Foundation**, the
fourth phase in the `66.x` AI Trading Intelligence sub-sequence, and
per the Director's own framing the first phase where AI infrastructure
begins preparing to learn *from the user*, not just narrate the
Trading Core's own output — though this phase itself performs no
evaluation, coaching, or teaching of any kind. New `ai/learning/`
subpackage (inside the existing `ai/` top-level package, confirmed by
`docs/PHASE66_3_AUDIT.md`'s TASK 0 audit, which also reviewed and
declined to reuse the pre-existing, DB-persisted
`learning.models.LearningRecord`, Phase 60.6/60.7, and
`ai/learning_context.py`'s `LearningContext`, both trade-outcome
statistics concerns rather than per-user topic mastery).
`LearningRecord`/`LearningTopic`/`LearningLevel`/`LearningSource`/
`LearningStatus` (`models.py`) are primitive-only, in-memory. `LearningRuntime`
(`learning_runtime.py`) is CRUD-only —
`create()`/`get()`/`list()`/`update()`/`archive()`, no real AI
inference, no performance computation, no coaching, no lesson/quiz
generation. `journal_adapter.py` maps an existing `TradeJournalEntry`
(Phase 66.2) into `LearningRuntime.create()`'s own keyword arguments —
pure mapping, never infers `topic`/`level`. `memory_adapter.py`'s
`memory_reference_key()` never imports `ai.memory`. Owner-only via a
dedicated `enable_learning_intelligence` flag. Zero diff in
`decision/`, `risk/`, `execution/`, `signals/`, `telegram/`,
`database/`, `monitoring/`, `strategies/` this phase (Rule 1/2). Not
wired into `core/pipeline.py` or any Telegram command — foundation
only. See `docs/PHASE66_3_FREEZE.md`.

Built Phase 66.4 — **AI Coaching Intelligence Foundation**, the fifth
phase in the `66.x` AI Trading Intelligence sub-sequence: AI still
never decides a trade — GoldBot's Trading Core and AI Analyst remain
the only source of any BUY/SELL/NO_TRADE decision; this phase only
builds the Foundation for explaining a trader's own mistakes,
surfacing weaknesses, and carrying a study/action suggestion. New
`ai/coaching/` subpackage (inside the existing `ai/` top-level package,
confirmed by `docs/PHASE66_4_AUDIT.md`'s TASK 0 audit, which found no
pre-existing Coaching model, Runtime, Manager, or Registry anywhere in
the codebase). `CoachingRecommendation`/`CoachingTopic`/
`CoachingPriority`/`CoachingType`/`CoachingStatus` (`models.py`) are
primitive-only, in-memory — `CoachingTopic` mirrors
`ai.learning.models.LearningTopic`'s own value set for coherence but
is a separate, local enum (no cross-package import in `models.py`).
`CoachingRuntime` (`coaching_runtime.py`) is CRUD-only —
`create()`/`get()`/`list()`/`archive()`/`update_status()`, no LLM, no
reasoning, no real inference of any kind; `update_status()` rejects
ARCHIVED (a dedicated, one-way action via `archive()` only).
`learning_adapter.py` maps an existing `LearningRecord` (Phase 66.3)
into `CoachingRuntime.create()`'s own keyword arguments — pure
mapping, and unlike the Journal Adapter it *can* relay `topic` directly
since `LearningRecord` already carries an explicit one.
`journal_adapter.py` maps an existing `TradeJournalEntry` (Phase 66.2)
the same way, deliberately never returning `topic` (no topic-shaped
field to relay without inferring one). Owner-only via a dedicated
`enable_coaching_intelligence` flag. Zero diff in `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, `telegram/`,
`database/`, `monitoring/` this phase (Rule 1). Not wired into
`core/pipeline.py` or any Telegram command — foundation only. Five
Director Notes recorded for a future, separately-briefed phase (not
implemented here): a Skill Tree view over `CoachingTopic`, per-user
Weakness Tracking, Adaptive Coaching, a Learning History chain
(Lesson → Exercise → Quiz → Replay → Exam → Certificate), and Academy
integration. See `docs/PHASE66_4_FREEZE.md`.

## Official Intelligence Pipeline (Director Decision, Phase 63.3; extended Phase 65.1)

The AI Core's real, ordered composition, as of the Phase 63.3 Director
Decision — supersedes any earlier, less specific composition order
this document previously implied. Phase 65.1 appended `→ Voice` as the
terminal narrating stage, per that phase's own Director Brief pipeline
diagram (`Content → Media → Broadcast → Voice Narration`):

```
Market → Knowledge → Memory → Reasoning → Conversation → Explanation
   → Content → Translation → Media → Broadcast → Voice
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
