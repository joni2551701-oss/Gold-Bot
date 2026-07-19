# GoldBot — Version Roadmap

Governed by `docs/constitution/CONSTITUTION.md`. This roadmap
reflects the real, completed phase history in this repository plus
the Director's own stated "what comes next" direction
(`docs/PHASE61_7_FREEZE.md`), not a speculative plan invented for
this document. Per the Phase 62.1c ruling: **this document is Actual
Development Status** — `docs/roadmap/AI_EVOLUTION.md` and
`docs/VISION.md` hold the forward-looking vision; this table never
claims a version is further along than the real code, tests, and
Freeze documents behind it prove.

## Version History

### v0.1 — Core Trading Foundation
**Status: COMPLETED.** Core trading pipeline: Data → Context →
Strategy → Signal → Decision → Risk → Telegram delivery.

### v0.2 — Database & Product Layer
**Status: COMPLETED.** Database layer, repositories, user/subscription
models.

### v0.3 — Telegram Owner Foundation
**Status: COMPLETED.** Telegram Owner panel foundation
(`telegram/owner/*`), permissions, admin tooling.

### v0.4 — AI Foundation
**Status: COMPLETED.** Providers, router, capabilities, runtime
foundation (Phases 59–61.6).

### v0.4.7 — AI Runtime + Production Intelligence
**Status: COMPLETED.** `AIService` as the single real orchestration
point over `RuntimeManager`/`ProviderCircuitBreaker`/`RuntimeProfile`/
`EventBus` (Phase 61.7), then production-wired further with retry
backoff, cost protection, and full Owner runtime control (Phase 62.2).
This is the version currently in force — the AI Runtime track has no
further scheduled work beyond what is already frozen
(`docs/PHASE62_2_RUNTIME_FREEZE.md`).

### v0.5 — Business Layer
**Status: NOT STARTED.** Subscription/billing/monetization.

### v0.6 — Owner Control Center
**Status: NOT STARTED.** Unified Owner Telegram dashboard beyond
today's per-domain commands (see `docs/owner/OWNER_PANEL.md`).

### v0.7 — Broadcast Foundation (Owner-only)
**Status: NOT STARTED.** Periodic delivery of queued Runtime/Provider
alerts via a live process loop (the gap `docs/PHASE61_7_FREEZE.md`
names explicitly: `deliver_alerts()` is not yet called from any
running loop). Phase 63.0 built the foundation/contract layer this
version will eventually wire live (`broadcast/`, `media/`,
`translation/`) — the contracts exist; the live loop does not.

### v0.8 — Web Dashboard
**Status: NOT STARTED.**

### v0.9 — Academy / Education Platform
**Status: NOT STARTED.**

### v1.0 — Full Production Release
**Status: NOT STARTED.** Trading Core + AI Layer + Business Layer +
Owner Control Center, all live together.

## Senior Trading AI Platform — how it maps onto v0.5–v0.9

`docs/VISION.md`'s "Market Media Intelligence" and "User Platform
Intelligence" pillars are not a new version number — they are the
destination v0.5 through v0.9 above are each one piece of. AI
Education and the Content Engine belong to v0.9's scope; Media
Intelligence (Voice/Video/Broadcast) belongs to v0.7's scope, once its
Phase 63.0 foundation gets a live wiring phase; Multi-language belongs
to `translation/`'s eventual real backend, also under v0.7. No
existing version number is renumbered or merged — several documents
(`docs/PHASE61_7_FREEZE.md`, `docs/owner/OWNER_PANEL.md`,
`docs/telegram/OWNER_SYSTEM.md`) already reference v0.5–v0.9 by these
exact numbers.

## Phase 63.x — AI Intelligence Layer sub-phases

`v0.4`'s AI Foundation track continues today through a numbered
sub-phase sequence, formalized in `docs/roadmap/AI_EVOLUTION.md`
(Director Decision, Phase 63.3): `63.0` Foundation, `63.1` Explanation,
`63.2` Knowledge, `63.3` Memory, `63.4` Reasoning, `63.5` Conversation,
`63.6` Content, `63.7` Media, `63.8` Broadcast (all DONE) — closes the
`63.0`–`63.8` AI Intelligence Layer sub-phase sequence. `64.0` AI
Intelligence Integration Layer (DONE) — `ai/intelligence_runtime.py`'s
`IntelligenceRuntime`, the first orchestrator composing all eight
layers, deterministic only. `65.0` AI Voice Intelligence Foundation
(DONE) — top-level `voice/`, a genuine new package (not a naming
correction like `media/`/`broadcast/`), Profile/Provider metadata
catalogs only, no synthesis; first phase in a new `65.x` Voice
sub-sequence. `65.1` AI Voice Provider Integration (DONE) — real
OpenAI/ElevenLabs TTS adapters, per-profile provider selection,
fallback handling, and Content/Media/Broadcast/Conversation
integration adapters; Voice is now the terminal stage of the Official
Intelligence Pipeline. `65.2` AI Voice Conversation Intelligence
(DONE) — real OpenAI STT (Whisper), intent detection, voice sessions,
and `voice/conversation_bridge.py`'s real "user speaks → AI
understands → AI replies by voice" round trip via the existing,
unmodified `ConversationEngine.ask()`. `65.3` Personal AI Assistant
Foundation (DONE) — top-level `assistant/`, Senior/Seniorita Identity
metadata (deliberately not `ai.persona.Persona`), a per-user
`AssistantProfile` + `AssistantManager` gated strictly Owner-only, and
structural (not real-call) Conversation/Voice/Memory integration
points. `65.4` Personal AI Runtime Integration (DONE) — real
composition via `assistant/runtime_adapter.py` (the third
composition-root-shaped file, after `ai/intelligence_runtime.py` and
`voice/conversation_bridge.py`): real `ConversationEngine.ask()`,
`VoiceRuntime.generate_audio()`, `MemoryRuntime.store()`/`recall()`,
and `IntelligenceRuntime.run()` calls, plus `AssistantRuntime`
session-lifecycle management on the existing `AssistantManager`.
`66.0` AI Trading Analyst Foundation (DONE) — new `ai/trading_analyst/`
subpackage: a primitive-only `TradingAnalysisInput`/`TradingAnalysis`
contract (resolving Constitution Article 3's absolute `ai/` →
`decision/`/`risk/`/`execution/` import ban against the brief's own
diagram, following `ai/explanation/explanation_input.py`'s precedent),
`TradingAnalystRuntime.analyze()` composing `IntelligenceRuntime.run()`
and `ExplanationBuilder.build()`, and `content_adapter.py` composing
the existing Content/Media/Broadcast pipeline — zero new Trading
Engine, zero diff in `decision/`/`risk/`/`execution/`/`strategies/`/
`signals/`/`context/`/`monitoring/`, Owner-only via a dedicated
`enable_trading_analyst` flag. First phase in a new `66.x` AI Trading
Intelligence sub-sequence. `66.1` AI Chart Intelligence Foundation
(DONE) — new `ai/chart_intelligence/` subpackage, the *chart
interpretation layer*: primitive-only `ChartAnalysisInput`/
`ChartAnalysis`/`ChartContext` (no image bytes stored, only a
content-hash reference), `ChartRuntime` (a pure relay/transform
composing `ExplanationBuilder` in EDUCATION mode, never a Vision API
call), `trading_analyst_adapter.py` (composes `TradingAnalysis` +
`ChartAnalysis` into a combined Explanation), and
`content_adapter.py` (existing Content/Media/Broadcast pipeline,
`ContentType.LIVE_ANALYSIS`/`MediaType.IMAGE` both reused) —
Owner-only via a dedicated `enable_chart_intelligence` flag. `66.2` AI
Trade Journal Intelligence Foundation (DONE) — new `ai/trade_journal/`
subpackage: primitive-only, in-memory `TradeJournalEntry`/
`ReplayContext` (mandatory `chart_id`/`trade_id` links, no database —
Rule 3, no statistics — Rule 4), `TradeJournalRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`update_notes()`), `trading_analyst_adapter.py`
(composes `TradingAnalysis` + `ChartAnalysis` into a `TradeJournalEntry`),
and `memory_adapter.py` (`memory_reference_key()`, never imports
`ai.memory`) — Owner-only via a dedicated `enable_trade_journal` flag.
This same phase also extended the Phase 66.1 LOCKed `ChartAnalysis`
with one new, additive `chart_id` field (LOCK-permitted extension)
(`66.3`-`66.8` not yet briefed). See
`docs/roadmap/AI_EVOLUTION.md`'s own "Phase 63.x" section for the
full sequence and its "Official Intelligence Pipeline" section for how
these sub-phases compose (`Market → Knowledge → Memory → Reasoning →
Conversation → Explanation → Content → Translation → Media →
Broadcast`). This table is not repeated here to avoid two documents
drifting out of sync — `docs/roadmap/AI_EVOLUTION.md` is the single
source for this sequence's detail.

## Notes

- This table intentionally does not promise dates — only scope and
  status, matching this codebase's own convention of never reporting
  a phase "Complete" without GitHub Actions confirmation (`CLAUDE.md`
  Reporting language rule).
- v0.4.7 (Phase 61.7) explicitly did not grow AI Core's capability
  surface — it made existing foundation pieces real and load-bearing.
  See `docs/PHASE61_7_FREEZE.md` for the full freeze declaration.
- Phase 62.0 and Phase 62.1 (a–d) are documentation-only and do not
  correspond to a version bump — no code changed in either.

## Related documents

- `docs/VISION.md` — the destination this roadmap's future versions
  build toward.
- `docs/roadmap/AI_EVOLUTION.md` — the AI-specific stage timeline
  within this same roadmap.
- `docs/PHASE61_7_FREEZE.md`, `docs/PHASE62_2_RUNTIME_FREEZE.md` —
  the most recent phase freezes this table's COMPLETED rows are
  backed by.
