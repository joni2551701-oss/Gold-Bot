# GoldBot — AI Architecture

Governed by `docs/constitution/CONSTITUTION.md` Articles 1, 3, and 5.
This document maps the real `ai/` package as it exists in the
repository today — verified directly via directory listing for this
phase, not transcribed from assumption.

## Real package tree — 26 subpackages under `ai/`

```
ai/
  access/          capability/permission gating for AI requests
  analyzer/        Phase 55 compat entry point -> re-exports ai/ai_analyzer.py
  audit/           provider_stats.py - call/provider auditing, DailyUsage/AI Cost Protection (Phase 62.2)
  cache/           response caching (ResponseCache, cache policy)
  capabilities/    Capability enum + permission matrix
  content/         content_adapter.py - ContentEngine.generate() (real AIService.ask() path,
                   Phase 61.5), extended Phase 63.6 with create()/format()/preview()/validate()/
                   history() (deterministic, no AI call); content_schema.py/content_types.py
                   (ContentRequest/ContentResult/ContentType, Phase 61.5/63.0); models.py/
                   content_adapters.py (Phase 63.6); broadcast_output.py (BroadcastReadyContent,
                   Phase 61.5)
  trading_analyst/ models.py (TradingAnalysisInput/TradingAnalysis/TradingRiskLevel, primitive-only
                   contract per Constitution Article 3), access.py (is_trading_analyst_enabled_for,
                   Owner-only), analyst_runtime.py (TradingAnalystRuntime.analyze() -- composes
                   IntelligenceRuntime + ExplanationBuilder, zero new business logic),
                   content_adapter.py (Content/Media/Broadcast pipeline prep, LIVE_ANALYSIS reused)
                   (Phase 66.0)
  chart_intelligence/ models.py (ChartAnalysisInput/ChartAnalysis/ChartContext/ChartImageType/
                   ChartAnalysisType, primitive-only, no image bytes stored; ChartAnalysis gained
                   chart_id in Phase 66.2, a LOCK-permitted additive extension), access.py
                   (is_chart_intelligence_enabled_for, Owner-only), chart_runtime.py
                   (ChartRuntime.analyze()/explain() -- pure relay/transform + ExplanationBuilder,
                   never calls a Vision API), trading_analyst_adapter.py (TradingAnalysis +
                   ChartAnalysis -> combined Explanation, the one file importing ai.trading_analyst),
                   content_adapter.py (Content/Media/Broadcast pipeline prep, LIVE_ANALYSIS reused),
                   vision_provider_types.py (ChartVisionProviderType, future-compatible vocabulary
                   only, no API) (Phase 66.1)
  trade_journal/   models.py (TradeJournalEntry/ReplayContext, primitive-only, in-memory,
                   chart_id/trade_id mandatory links), access.py (is_trade_journal_enabled_for,
                   Owner-only), journal_runtime.py (TradeJournalRuntime -- create/get/list/
                   update_notes CRUD only, in-memory dict, no database), trading_analyst_adapter.py
                   (TradingAnalysis + ChartAnalysis -> TradeJournalEntry, the one file importing
                   ai.trading_analyst and ai.chart_intelligence), memory_adapter.py
                   (memory_reference_key() -- a plain string key, never imports ai.memory) (Phase
                   66.2)
  learning/        models.py (LearningRecord/LearningTopic/LearningLevel/LearningSource/
                   LearningStatus, primitive-only, in-memory, per-user topic-mastery -- distinct
                   from the pre-existing, unrelated top-level learning/ package), access.py
                   (is_learning_intelligence_enabled_for, Owner-only), learning_runtime.py
                   (LearningRuntime -- create/get/list/update/archive CRUD only, in-memory dict,
                   no database, no real AI inference), journal_adapter.py (TradeJournalEntry ->
                   LearningRecord input mapping, pure, the one file importing ai.trade_journal),
                   memory_adapter.py (memory_reference_key() -- a plain string key, never imports
                   ai.memory) (Phase 66.3)
  coaching/        models.py (CoachingRecommendation/CoachingTopic/CoachingPriority/CoachingType/
                   CoachingStatus, primitive-only, in-memory, no BUY/SELL/verdict field of any
                   kind), access.py (is_coaching_intelligence_enabled_for, Owner-only),
                   coaching_runtime.py (CoachingRuntime -- create/get/list/archive/update_status
                   CRUD only, in-memory dict, no database, no LLM/reasoning/inference of any kind),
                   learning_adapter.py (LearningRecord -> Coaching input mapping, pure, the one
                   file importing ai.learning), journal_adapter.py (TradeJournalEntry -> Coaching
                   input mapping, pure, the one file importing ai.trade_journal) (Phase 66.4)
  performance/     models.py (PerformanceRecord/PerformanceMetric/PerformanceCategory,
                   primitive-only, in-memory, no BUY/SELL/verdict field of any kind, distinct from
                   analytics.performance_metrics.PerformanceMetrics), access.py
                   (is_performance_intelligence_enabled_for, Owner-only), performance_runtime.py
                   (PerformanceRuntime -- create/get/list/update_notes/archive CRUD only, in-memory
                   dict, no database, no scoring algorithm), journal_adapter.py (TradeJournalEntry
                   -> Performance input mapping, pure, the one file importing ai.trade_journal),
                   coaching_adapter.py (PerformanceRecord -> Coaching input mapping, pure, no
                   ai.coaching import needed), analytics_adapter.py (reuses
                   analytics.strategy_report.compute_win_rate(), the one file importing analytics),
                   memory_adapter.py (performance_memory_key() -- a plain string key, never imports
                   ai.memory) (Phase 66.5)
  strategy/        models.py (StrategyRecord/StrategyType/StrategyStatus/StrategyConfidence,
                   primitive-only, in-memory, no BUY/SELL/verdict field of any kind, StrategyStatus
                   distinct from strategies.lifecycle.strategy_status.StrategyStatus -- import of
                   strategies/ forbidden outright), access.py (is_strategy_intelligence_enabled_for,
                   Owner-only), strategy_runtime.py (StrategyRuntime -- create/get/list/update/
                   update_notes/archive CRUD only, in-memory dict, no database, no LLM/reasoning),
                   performance_adapter.py (PerformanceRecord -> Strategy input mapping, type-only,
                   the one file importing ai.performance -- never imports
                   ai.performance.performance_runtime), journal_adapter.py (TradeJournalEntry ->
                   Strategy input mapping, pure, the one file importing ai.trade_journal),
                   memory_adapter.py (strategy_reference_key() -- a plain string key, never imports
                   ai.memory) (Phase 66.6)
  portfolio/       models.py (PortfolioRecord/PortfolioStatus/PortfolioRiskLevel/PortfolioHealth,
                   primitive-only, in-memory, no lot-size/verdict field of any kind, no pre-existing
                   Portfolio model found anywhere), access.py (is_portfolio_intelligence_enabled_for,
                   Owner-only), portfolio_runtime.py (PortfolioRuntime -- create/get/list/update/
                   update_notes/archive CRUD only, in-memory dict, no database, no LLM/reasoning),
                   performance_adapter.py (PerformanceRecord -> Portfolio input mapping, type-only,
                   the one file importing ai.performance -- never imports
                   ai.performance.performance_runtime), strategy_adapter.py (Sequence[StrategyRecord]
                   -> Portfolio input mapping, type-only, the one file importing ai.strategy --
                   deterministic strategy_count/active_strategy_count counting, never imports
                   ai.strategy.strategy_runtime), memory_adapter.py (portfolio_reference_key() -- a
                   plain string key, never imports ai.memory) (Phase 66.7)
  context/         context_snapshot.py, context_builder.py (signals/context type-only imports)
  conversation/    conversation_engine.py - ConversationEngine.start_session()/ask()
                   (real AIService.ask() path, Phase 61.3), extended Phase 63.5 with
                   append()/summarize()/history()/context()/reset()/close() (deterministic,
                   no AI call); models.py/conversation_adapters.py (Phase 63.5)
  explanation/     explanation_engine.py (signals type-only imports, real AIService.ask() path);
                   explanation_input.py/explanation_output.py/explanation_templates.py/
                   explanation_builder.py/explanation_content_adapter.py (Phase 63.1 -
                   deterministic, template-based, no AI/provider call, no decision/risk import)
  journal/         trade_journal.py (canonical) - AI-side trade journaling
  memory/          context_memory.py/memory_runtime.py (long-term AI memory storage);
                   models.py/memory_registry.py (Phase 63.3 - MemoryEntry contract +
                   MemoryScope catalog, MemoryRuntime extended with store/recall/search)
  profiles/        RuntimeProfile definitions (DEVELOPMENT/TESTING/PRODUCTION)
  prompts/         prompt templates
  providers/       BaseAIProvider, vendor implementations, circuit_breaker.py
  reasoning/       models.py/reasoning_registry.py/reasoning_runtime.py/reasoning_adapters.py
                   (Phase 63.4 - deterministic ReasoningResult store, Knowledge/Memory
                   type-only reads, no ai.explanation import - Intelligence Dependency Principle)
  router/          AIRouter, routing_rules.py
  runtime/         AIService, RuntimeManager, EventBus, self_check.py - production-wired orchestration point (Phase 62.2)
  session/         session/user context for AI product surfaces
  tools/           AI-callable tool definitions (advisory only)
  validation/      response validation, safety.py

  ai_analyzer.py            canonical analyzer (ai/analyzer/ re-exports this)
  ai_prompt.py              prompt construction
  confidence_model.py       AI-side confidence blending helpers (internal to ai/ only - decision/ has its own independent confidence blending in decision_engine.py and does not import this file)
  intelligence_runtime.py   IntelligenceRuntime - the Official Intelligence Pipeline composition root (Knowledge -> Memory -> Reasoning -> Conversation -> Explanation -> Content -> Media -> Broadcast), deterministic-only, Phase 64.0
  interfaces.py             AIAnalyzerInterface - the advisory-only contract every future provider must honor
  learning_context.py       learning-context helpers
  trade_journal.py          canonical trade journal (ai/journal/ re-exports this)
```

## Note on the brief's assumption (honest correction)

An earlier task brief referred to "security" and "knowledge" as if
they were subpackages directly under `ai/`. The real repository does
not have either:

- **`knowledge/` is a separate, top-level package** — a sibling of
  `ai/`, not `ai/knowledge/`. It is not part of the AI package tree
  documented here. This same correction recurred in a second Worker
  Brief (Phase 63.2) — see `docs/PHASE63_2_AUDIT.md` — confirming this
  is a stable, standing fact worth stating plainly for any future
  brief: **the real Knowledge Foundation is `knowledge/`, never
  `ai/knowledge/`.**
- **There is no dedicated `ai/security/` folder.** AI-relevant safety
  checks live in `ai/validation/safety.py`; Telegram-side security
  concerns live in `telegram/owner/security.py`, outside `ai/`
  entirely.
- **`media/` is a separate, top-level package** (Phase 63.0 TASK 5,
  extended Phase 63.7) — a sibling of `ai/`, not `ai/media/`. A Phase
  63.7 Worker Brief referred to `ai/media/` throughout; the same
  correction this document already made for `knowledge/` applies here
  too — see `docs/PHASE63_7_AUDIT.md`.
- **`broadcast/` is a separate, top-level package** (Phase 63.0 TASK 4,
  extended Phase 63.8) — a sibling of `ai/`, not `ai/broadcast/`. A
  Phase 63.8 Worker Brief referred to `ai/broadcast/` throughout; the
  same correction applies a third time — see `docs/PHASE63_8_AUDIT.md`.
- **`voice/` is a separate, top-level package** (Phase 65.0) — a
  sibling of `ai/`, not `ai/voice/`. Unlike the three corrections
  above, this is not a naming discrepancy: neither `voice/` nor
  `ai/voice/` existed anywhere in the repository before this phase —
  see `docs/PHASE65_0_AUDIT.md`'s TASK 0 finding, which confirms this
  is a genuine new top-level package case (the same reasoning
  `docs/PHASE63_0_FOUNDATION_AUDIT.md` originally used to justify
  `broadcast/`).
- **`assistant/` is a separate, top-level package** (Phase 65.3;
  extended Phase 65.4) — a sibling of `ai/`, not `ai/assistant/`. Same
  genuine-new-package reasoning as `voice/` above (see
  `docs/PHASE65_3_AUDIT.md`). Phase 65.3 built it importing
  **nothing** from `ai/` except `ai.access.permissions.AIRole` (it
  sits before Conversation in the Official Intelligence Pipeline, so
  per the Intelligence Dependency Principle it may depend on nothing
  downstream of it). Phase 65.4 adds one deliberate, narrow exception:
  `assistant/runtime_adapter.py` — and only that one file — is now
  permitted to import `ai.conversation/`, `ai.memory/`, and
  `ai.intelligence_runtime` for real integration; every other file in
  `assistant/` keeps the original zero-downstream-import posture (see
  `docs/PHASE65_4_AUDIT.md`).

Per Constitution Article 7 (Reuse Principle) this document records
what is actually real rather than fabricating folders to match an
assumption — the same discipline `docs/architecture/MODULE_DEPENDENCIES.md`
applies to this identical discrepancy.

## Orchestration entry point

`ai/runtime/ai_service.py`'s `AIService.ask()` is the single real
control-flow entry point, production-wired as of Phase 62.2: it gates
on `RuntimeManager.is_healthy()`, routes through `AIRouter`
(`ai/router/`), attempts a provider (`ai/providers/`) guarded by
`ProviderCircuitBreaker` (with an exponential-backoff wait between
retry attempts — `2 ** attempt` seconds, injectable `sleep_fn`),
validates the result (`ai/validation/`), reads/writes `ai/cache/`,
records to `ai/audit/` (including the previously-unaudited
runtime-unhealthy rejection path), checks AI Cost Protection
(`ai/audit/provider_stats.py`'s `compute_daily_usage()`/
`evaluate_cost_protection()` against an optional
`daily_cost_limit`/`daily_token_limit`), and publishes to
`ai/runtime/event_bus.py`'s `EventBus`. The full sequence diagram
lives in `docs/AI_RUNTIME_FLOW.md`; the Phase 62.2 production-wiring
detail lives in `docs/PHASE62_2_RUNTIME_AUDIT.md` and
`docs/PHASE62_2_RUNTIME_FREEZE.md`.

## Isolation boundary (Constitution Article 3)

Zero `ai/*` → `decision/`/`risk/`/`execution/` imports, verified by
grep sweep at the close of every AI-touching phase. The seven
pre-existing `signals/`/`context/` type-only import sites are the one
standing, audited exception (see
`docs/architecture/IMPORT_RULES.md`).

## Deeper detail per subsystem (Phase 62.1c)

This document maps the package tree; each of these covers one
subsystem's real behavior in depth rather than repeating the tree
above:

- `docs/ai/AI_PIPELINE.md` — the Intelligence-layer composition order
  (Persona → Context → Knowledge → Tools → Conversation → Memory →
  Explanation → Content → Media) and where a request's market context
  actually enters it.
- `docs/ai/AI_MEMORY.md` — `ai/memory/`'s `MemoryRuntime` facade.
- `docs/ai/AI_KNOWLEDGE.md` — `knowledge/`'s 6-category static catalog.
- `docs/ai/AI_REASONING.md` — `ai/reasoning/`'s deterministic
  `ReasoningRuntime` and its Knowledge/Memory/Explanation integration
  points (Phase 63.4).
- `docs/ai/AI_CONVERSATION.md` — `ai/conversation/`'s two surfaces
  (real `AIService.ask()` path plus the deterministic extension) and
  its Knowledge/Memory/Reasoning/Explanation integration points
  (Phase 63.5).
- `docs/ai/AI_CONTENT.md` — `ai/content/`'s two surfaces (real
  `AIService.ask()` path plus the deterministic extension) and its
  Explanation/Conversation integration points (Phase 63.6).
- `docs/ai/AI_MEDIA.md` — top-level `media/`'s `MediaManager` (Owner
  ENABLED/DISABLED intent plus the deterministic `MediaAsset` surface)
  and its Content integration point (Phase 63.7).
- `docs/ai/AI_BROADCAST.md` — top-level `broadcast/`'s `BroadcastManager`
  (would_broadcast/prepare plus the deterministic `BroadcastAsset`
  surface) and its Content/Media integration point (Phase 63.8).
- `docs/ai/AI_INTELLIGENCE_PIPELINE.md` — `ai/intelligence_runtime.py`'s
  `IntelligenceRuntime`, the composition root that calls all eight
  layers above in Official Intelligence Pipeline order (Phase 64.0).
- `docs/ai/AI_VOICE.md` — top-level `voice/`'s `VoiceManager`/
  `VoiceProfileRegistry`/`VoiceRuntime` (Profile + Provider metadata
  catalogs, deterministic request/result lifecycle, Phase 65.0), real
  OpenAI/ElevenLabs TTS provider adapters, per-profile provider
  selection, and fallback handling (Phase 65.1), real OpenAI STT
  (Whisper), intent detection, voice sessions, and the real "user
  speaks → AI understands → AI replies by voice" round trip via
  `voice/conversation_bridge.py` (Phase 65.2), and its Content/
  Media/Broadcast/Conversation integration points.
- `docs/ai/AI_PERSONAL_ASSISTANT.md` — top-level `assistant/`'s
  `IdentityManager`/`AssistantManager` (Senior/Seniorita identity
  metadata, per-user `AssistantProfile`, Owner-only gate, Phase 65.3),
  extended with real `AssistantRuntime` lifecycle management and
  `runtime_adapter.py`'s real Conversation/Voice/Memory/Intelligence
  Pipeline composition (Phase 65.4).
- `docs/ai/AI_TRADING_ANALYST.md` — `ai/trading_analyst/`'s
  `TradingAnalystRuntime` (analyzes an already-made Trading Core
  result, never decides), its primitive-only `TradingAnalysisInput`
  contract (the Constitution Article 3 resolution), and its
  Explanation/Content/Media/Broadcast integration points (Phase 66.0).
- `docs/ai/AI_CHART_INTELLIGENCE.md` — `ai/chart_intelligence/`'s
  `ChartRuntime` (reads and narrates an already-supplied chart
  interpretation, never decides, never calls a Vision API), its
  primitive-only `ChartAnalysisInput`/`ChartContext` contracts (no
  image bytes stored), and its Trading Analyst/Explanation/Content/
  Media/Broadcast integration points (Phase 66.1).
- `docs/ai/AI_TRADE_JOURNAL.md` — `ai/trade_journal/`'s
  `TradeJournalRuntime` (CRUD-only, in-memory, no database, no
  statistics), its primitive-only `TradeJournalEntry`/`ReplayContext`
  contracts (mandatory `chart_id`/`trade_id` links, metadata-only
  replay pointers), and its Trading Analyst/Chart Intelligence/Memory
  integration points (Phase 66.2).
- `docs/ai/AI_LEARNING.md` — `ai/learning/`'s `LearningRuntime`
  (CRUD-only, in-memory, no real AI inference, no performance
  computation), its primitive-only `LearningRecord` contract (per-user
  topic mastery, distinct from the pre-existing `learning/` package's
  own trade-outcome-statistics `LearningRecord`), and its Trade
  Journal/Memory integration points (Phase 66.3).
- `docs/ai/AI_COACHING.md` — `ai/coaching/`'s `CoachingRuntime`
  (CRUD-only, in-memory, no LLM/reasoning/inference, no BUY/SELL/
  verdict field of any kind), its primitive-only
  `CoachingRecommendation` contract (`learning_id`/`journal_id` links
  to its two upstream sources), and its Learning/Trade Journal
  integration points (Phase 66.4).
- `docs/ai/AI_PERFORMANCE.md` — `ai/performance/`'s `PerformanceRuntime`
  (CRUD-only, in-memory, no scoring algorithm, no BUY/SELL/verdict
  field of any kind), its primitive-only `PerformanceRecord`/
  `PerformanceMetric` contracts (distinct from
  `analytics.performance_metrics.PerformanceMetrics`), and its Trade
  Journal/Coaching/Analytics/Memory integration points (Phase 66.5).
- `docs/ai/AI_STRATEGY.md` — `ai/strategy/`'s `StrategyRuntime`
  (CRUD-only, in-memory, no LLM/reasoning/inference, no BUY/SELL/
  verdict field of any kind), its primitive-only `StrategyRecord`
  contract (`StrategyStatus` distinct from the Trading-Core-LOCKed
  `strategies.lifecycle.strategy_status.StrategyStatus` -- import of
  `strategies/` forbidden outright by this phase's own Rule 1), and
  its Performance/Trade Journal/Memory integration points (Phase 66.6).
- `docs/ai/AI_PORTFOLIO.md` — `ai/portfolio/`'s `PortfolioRuntime`
  (CRUD-only, in-memory, no LLM/reasoning/inference, no lot-size/
  verdict field of any kind, no Risk Manager replacement), its
  primitive-only `PortfolioRecord` contract (no pre-existing Portfolio
  model found anywhere in the codebase), and its Performance/Strategy/
  Memory integration points, including the first `66.x` adapter to
  operate over a sequence of source records rather than a single one
  (Phase 66.7).
- `docs/ai/AI_TOOLS.md` — `ai/tools/`'s 5 advisory-only tools.
- `docs/ai/AI_RUNTIME.md` — current real Runtime state (Manager,
  Circuit Breaker, Event Bus, Metrics, Cost Protection).
- `docs/ai/AI_PROVIDER_SYSTEM.md` — the real provider roster and the
  `BaseAIProvider` contract they all implement.

## Related documents

- `docs/constitution/CONSTITUTION.md` — Articles 1/3/5 this structure
  must always satisfy.
- `docs/architecture/MODULE_DEPENDENCIES.md` — this same tree in the
  context of the full system dependency map.
- `docs/AI_RUNTIME_FLOW.md` — the detailed request-flow sequence
  through this package (Phase 61.7).
- `ai/README.md` — the package's own top-level README.
