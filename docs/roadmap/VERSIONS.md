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
(`platform_layer/telegram/owner/*`), permissions, admin tooling.

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
Intelligence Integration Layer (DONE) — `ai_layer/ai_engine/intelligence_runtime.py`'s
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
and `ai_layer/voice_ai/conversation_bridge.py`'s real "user speaks → AI
understands → AI replies by voice" round trip via the existing,
unmodified `ConversationEngine.ask()`. `65.3` Personal AI Assistant
Foundation (DONE) — top-level `assistant/`, Senior/Seniorita Identity
metadata (deliberately not `ai_layer.personal_ai.persona_manager.Persona`), a per-user
`AssistantProfile` + `AssistantManager` gated strictly Owner-only, and
structural (not real-call) Conversation/Voice/Memory integration
points. `65.4` Personal AI Runtime Integration (DONE) — real
composition via `ai_layer/ai_service/assistant/runtime_adapter.py` (the third
composition-root-shaped file, after `ai_layer/ai_engine/intelligence_runtime.py` and
`ai_layer/voice_ai/conversation_bridge.py`): real `ConversationEngine.ask()`,
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
`ai_layer.knowledge_ai.memory_manager`) — Owner-only via a dedicated `enable_trade_journal` flag.
This same phase also extended the Phase 66.1 LOCKed `ChartAnalysis`
with one new, additive `chart_id` field (LOCK-permitted extension).
`66.3` AI Learning Intelligence Foundation (DONE) — new `ai/learning/`
subpackage, the first phase where AI infrastructure begins preparing
to learn from the user (though this phase itself performs no
evaluation, coaching, or teaching): primitive-only, in-memory
`LearningRecord`/`LearningTopic`/`LearningLevel`/`LearningSource`/
`LearningStatus` (distinct from the pre-existing, DB-persisted
`ai_layer.knowledge_ai.learning_loop.models.LearningRecord`, Phase 60.6/60.7, reviewed but not
reused), `LearningRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`update()`/`archive()`, no real AI
inference), `journal_adapter.py` (pure `TradeJournalEntry` ->
`LearningRuntime.create()` input mapping, never infers `topic`/`level`),
and `memory_adapter.py` (`memory_reference_key()`, never imports
`ai_layer.knowledge_ai.memory_manager`) — Owner-only via a dedicated `enable_learning_intelligence`
flag. `66.4` AI Coaching Intelligence Foundation (DONE) — new
`ai/coaching/` subpackage: AI still never decides a trade (GoldBot's
Trading Core and AI Analyst remain the only decision source); this
phase builds the Foundation for explaining mistakes, surfacing
weaknesses, and carrying a study/action suggestion. Primitive-only, in-
memory `CoachingRecommendation`/`CoachingTopic`/`CoachingPriority`/
`CoachingType`/`CoachingStatus`, `CoachingRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`archive()`/`update_status()`, no LLM/
reasoning/inference), `learning_adapter.py` (pure `LearningRecord` ->
`CoachingRuntime.create()` input mapping, relays `topic` directly since
`LearningRecord` already carries one), and `journal_adapter.py` (pure
`TradeJournalEntry` -> `CoachingRuntime.create()` input mapping, never
infers `topic`) — Owner-only via a dedicated
`enable_coaching_intelligence` flag. `66.5` AI Performance Intelligence
Foundation (DONE) — new `ai/performance/` subpackage: AI still never
decides a trade (GoldBot's Trading Core and AI Analyst remain the only
decision source); this phase builds the Foundation for understanding
trade performance (quality scores, discipline tracking, pattern
storage). Primitive-only, in-memory `PerformanceRecord`/
`PerformanceMetric`/`PerformanceCategory` (`PerformanceMetric`, a
generic named observation, distinct from the pre-existing, fixed-shape
`backtesting_layer.statistics.performance_metrics.PerformanceMetrics`), `PerformanceRuntime`
(CRUD-only: `create()`/`get()`/`list()`/`update_notes()`/`archive()`,
no scoring algorithm), `journal_adapter.py` (pure `TradeJournalEntry`
-> `PerformanceRuntime.create()` input mapping, never computes win/loss),
`coaching_adapter.py` (pure `PerformanceRecord` -> `CoachingRuntime.create()`
input mapping, structure only), `analytics_adapter.py` (reuses
`backtesting_layer.statistics.strategy_report.compute_win_rate()` directly), and
`memory_adapter.py` (`performance_memory_key()`, never imports
`ai_layer.knowledge_ai.memory_manager`) — Owner-only via a dedicated
`enable_performance_intelligence` flag. `66.6` AI Strategy Intelligence
Foundation (DONE) — new `ai/strategy/` subpackage: AI still never
opens a trade, gives a signal, manages risk, or affects the Decision
Engine (GoldBot's Trading Core remains the only decision source); this
phase builds the Foundation for answering "Qaysi strategiya qanday
ishlayapti?" (Which strategy is performing how?). Primitive-only,
in-memory `StrategyRecord`/`StrategyType`/`StrategyStatus`/
`StrategyConfidence` (`StrategyStatus` distinct from the Trading-Core-
LOCKed `strategy_layer.strategy_manager.lifecycle.strategy_status.StrategyStatus` -- import
of `strategies/` forbidden outright by this phase's own Rule 1, making
reuse architecturally impossible rather than merely impractical),
`StrategyRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
no LLM/GPT/Claude/Gemini/reasoning/inference of any kind),
`performance_adapter.py` (type-only `PerformanceRecord` -> Strategy
input mapping, never imports the Performance Runtime),
`journal_adapter.py` (pure `TradeJournalEntry` -> Strategy input
mapping, never relays per-trade confidence as a per-strategy value),
and `memory_adapter.py` (`strategy_reference_key()`, never imports
`ai_layer.knowledge_ai.memory_manager`) — Owner-only via a dedicated `enable_strategy_intelligence`
flag. `66.7` AI Portfolio Intelligence Foundation (DONE) — new
`ai/portfolio/` subpackage: AI still never opens a trade, sizes a lot,
replaces the Risk Manager, or affects the Decision Engine (GoldBot's
Trading Core remains the only decision/sizing source); this phase
builds the Foundation for answering "Portfolio qanday holatda?" (What
state is the portfolio in?). Primitive-only, in-memory
`PortfolioRecord`/`PortfolioStatus`/`PortfolioRiskLevel`/
`PortfolioHealth` (no pre-existing Portfolio model found anywhere;
`risk_layer.risk_engine.risk_manager.RiskResult` is the nearest conceptual neighbor by
name only, Trading Core, import forbidden outright by Rule 1),
`PortfolioRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
no LLM/GPT/Claude/Gemini/reasoning/inference of any kind),
`performance_adapter.py` (type-only `PerformanceRecord` -> Portfolio
input mapping, relays `notes` only), `strategy_adapter.py` (the first
`66.x` adapter to operate over a `Sequence[StrategyRecord]` rather
than a single record, deterministically counting `strategy_count`/
`active_strategy_count`, not inference), and `memory_adapter.py`
(`portfolio_reference_key()`, never imports `ai_layer.knowledge_ai.memory_manager`) — Owner-only
via a dedicated `enable_portfolio_intelligence` flag. `66.8` AI
Research Intelligence Foundation (DONE, final phase of the `66.x`
sub-sequence) — new `ai/research/` subpackage: AI still never opens a
trade, gives a signal, computes risk, selects a strategy, or touches
Trading Core; this phase builds a single scientific layer accepting
data from every prior `66.x` Foundation module. Primitive-only,
in-memory `ResearchRecord`/`ResearchStatus`/`ResearchPriority`/
`ResearchCategory` (no pre-existing Research model found anywhere,
including no pre-existing top-level `research/` package),
`ResearchRuntime` (CRUD-only:
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
no LLM/GPT/Claude/Gemini/OpenAI/reasoning/inference of any kind),
`performance_adapter.py`/`strategy_adapter.py`/`portfolio_adapter.py`
(each a type-only mapping from an existing `PerformanceRecord`/
`StrategyRecord`/`PortfolioRecord`, relaying `notes` and setting a
fixed `category` value that is a structural constant of that adapter,
never content-based inference), and `memory_adapter.py`
(`research_reference_key()`, never imports `ai_layer.knowledge_ai.memory_manager`) — Owner-only
via a dedicated `enable_research_intelligence` flag. This closes the
`66.x` AI Trading Intelligence sub-sequence entirely; the Director's
own next roadmap moves to GoldBot Core Owner Monitoring Alpha (Track
B), not a new AI Foundation phase. Track B is now underway: Phase B.0
(a follow-up Worker Brief under the same title as the already-shipped
"GoldBot Core Owner Monitoring Alpha") extended `monitoring/` with
resource metrics, health classification, a performance counter, and
per-pipeline-stage timing — see `docs/PHASE_B0_AUDIT.md`/
`docs/PHASE_B0_FREEZE.md`. See
`docs/roadmap/AI_EVOLUTION.md`'s own "Phase 63.x" section for the
full sequence and its "Official Intelligence Pipeline" section for how
these sub-phases compose (`Market → Knowledge → Memory → Reasoning →
Conversation → Explanation → Content → Translation → Media →
Broadcast`). This table is not repeated here to avoid two documents
drifting out of sync — `docs/roadmap/AI_EVOLUTION.md` is the single
source for this sequence's detail.

### V1.0 Pre-Freeze Audit — GoldBot V1 Final Audit Foundation
**Status: COMPLETED (audit only, no code change).** A dedicated
audit/verification/stabilization phase — no new strategy, no new AI
Foundation, no Trading Core logic change, no architecture rebuild.
Covered Repository Health, full Architecture Verification (import
graph + circular-import check), Trading Pipeline, Risk Management,
Execution, AI Layer, Monitoring, Database, Configuration,
Error/Logging, Test, Performance, and Production Readiness audits. No
safety-relevant defect found; a set of known, mostly pre-existing gaps
(no RR/drawdown/duplicate-trade enforcement in `risk/`, no automated
DB backup, some architecture-doc drift) was documented for the
Director rather than fixed, per this phase's own Trading Core/AI
Foundation lock rules. See `docs/PHASE_V1_AUDIT.md`,
`docs/V1_RISK_AUDIT.md`, `docs/V1_PERFORMANCE_REPORT.md`, and
`docs/PHASE_V1_FREEZE.md` for full detail.

### V1.0.1 Stabilization — Risk Management Hardening Patch
**Status: COMPLETED.** Director-approved follow-up to the V1.0 audit's
Risk Management findings — this phase was explicitly scoped (its own
RULE 1) to `risk/`, `configuration/`, `database/`, `monitoring/`,
`tests/`, `docs/` only, with `core/`, `decision/`, `execution/`,
`strategies/`, `signals/`, `context/`, and `ai/` all locked. Fixed
every V1.0-audit Risk gap that scope permitted: a configurable
risk-per-trade clamp (`min_risk_per_trade`/`max_risk_per_trade`), a
minimum risk/reward ratio (`min_risk_reward_ratio`, default 2.0),
per-symbol drawdown and daily-loss tracking backed by a new
`risk_account_state` table (`risk_layer/risk_engine/account_state_tracker.py`),
duplicate-trade detection reusing a new append-only `risk_decisions`
log (`risk_layer/risk_validator/duplicate_checker.py`), and — the most significant
correction — Risk now consults `core_layer.emergency.emergency_manager.EmergencyManager`
directly, so `PAUSED`/`KILLED`/`MAINTENANCE` actually stop new trade
approval at the Risk layer, not only Telegram delivery. Every
`RiskManager.evaluate()` call is now logged
(`database_layer/trade_repository/risk_decision_repository.py`), with a new read-only
`core_layer/health_monitor/risk_monitor.py` aggregator. All changes additive/optional
on `RiskManager`'s public signature — the existing `core/pipeline.py`
and `backtesting_layer/backtest_engine/backtest_engine.py` call sites are unchanged and all
8 pre-existing risk tests pass unmodified. 127 new tests (4286 → 4413).
See `docs/PHASE_V1_0_1_RISK_AUDIT.md`, `docs/PHASE_V1_0_1_RISK_FREEZE.md`,
and the updated `docs/trading/RISK_SYSTEM.md`.

### P1 — Production Deployment Pipeline Foundation
**Status: COMPLETED.** Director-approved first Production phase after
V1 Freeze — builds the permanent, GitHub-Actions-driven deployment
path: `push -> validate (pyflakes/compileall/pytest) -> rsync release
-> SSH activate -> systemd restart -> health check`. Scoped (RULE 1)
to deploy tooling only — `core/`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `ai/` all locked, zero diff
verified. New: `.github/workflows/production_deploy.yml`;
`scripts/deploy/release_manager.py` (pure, unit-tested release-
selection/rollback logic — no VPS needed to test it),
`release_deploy.sh`, `rollback.sh`; `deploy/systemd/goldbot.service`
(release-based, `User=senior`, never root). Extended, not duplicated:
`scripts/health_check.py` gained two import-level checks
(`main`/`platform_layer.telegram.polling`), reused as both the pre-activation smoke
test and the post-restart health check. Release-based layout
(`/opt/{releases,shared,current,backups}`) never writes
directly into `current`, never overwrites `shared/.env`/`database`/
`logs`, and keeps every previous release on disk so rollback is always
a symlink switch plus a restart — never a rebuild. 155 new tests. See
`docs/PHASE_P1_AUDIT.md`, `docs/PHASE_P1_FREEZE.md`, and
`docs/deployment/PRODUCTION_DEPLOYMENT.md`/`ROLLBACK.md`.

### V2 Phase 1 — Language Foundation
**Status: COMPLETED (FROZEN as of commit `5c1f806`).** Director-
approved incremental delivery (Phase 1.0 → 1.6, each sub-phase
independently code-reviewed, tested, CI-confirmed, and production-
deployed before the next one started). Built the Translation Engine
(`media_layer/translation/ui_catalog.py`, a 77-key static UZ/RU/EN catalog with
`t(key, language, **kwargs)`), localized all 17 `COMMANDS`-registry
USER-tier handlers and every USER-tier keyboard
(`platform_layer/telegram/keyboards.py`), wired `/language`'s inline keyboard to a
real `callback_query` handler (`platform_layer/telegram/callback_router.py`, new),
and closed the two remaining hardcoded-English gaps
(`language_status()`'s own reply text, `contact_handler`'s failure
path). Confirmed via a real Production Telegram Manual Test (UZ/RU/EN
selection via inline buttons, language persistence across bot
restart), not just CI. OWNER/ADMIN-tier commands are permanently
English by design, not deferred. `platform_layer/telegram/signal_formatter.py` and
`platform_layer/telegram/signal_access_service.py` deferred to V2.1 (Signal Product
Layer); `command_router.py`'s generic constants deferred to V2.2
(future Generic Error Catalog). Zero diff in `core/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
and `platform_layer/telegram/owner/` across the entire phase. 47 new tests (4575 →
4622). See `docs/PHASE_V2_PHASE1_FREEZE.md` and
`docs/telegram/TELEGRAM_ARCHITECTURE.md`'s Language Foundation
section.

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
