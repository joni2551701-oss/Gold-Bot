# AI_FILE_TREE.md — TASK-AI-000 Phase 1: Project Inventory

Status: **AUDIT ONLY**. No code was written or changed to produce this
document. Scope is `ai/` exclusively (not `assistant/`, `voice/`,
`knowledge/`, `learning/`, `broadcast/`, `media/`, `translation/` —
those are separate top-level packages, out of scope per the Director's
"Audit faqat ai/ moduli uchun" instruction).

Method: every `.py` file under `ai/` was read/AST-parsed directly (not
inferred from documentation). 182 `.py` files across 30 subpackages
plus 8 top-level module files.

## Cross-cutting finding #1 — every `__init__.py` under `ai/` is empty

All 30 subpackage `__init__.py` files, and the top-level `ai/__init__.py`,
contain zero bytes of real content — no imports, no `__all__`. Nothing
is exported at the package level anywhere in `ai/`; every consumer must
import the exact submodule path (e.g. `from ai.access.permissions
import AIRole`, never `from ai.access import AIRole`). "Public vs
private" in this codebase is a **module-level naming convention**
(single leading underscore) rather than an `__init__.py` re-export
list. Two top-level module files buck this pattern by defining their
own `__all__` as compatibility shims: `ai/analyzer/ai_analyzer.py` and
`ai_layer/knowledge_ai/knowledge_base/trade_journal.py`.

## Cross-cutting finding #2 — `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` is permanently unreachable

Both `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` (a compatibility-shim module) and
`ai/trade_journal/` (a real subpackage, Phase 66.2) exist side by side
with the same import name. CPython always resolves the package
directory over the sibling module of the same name, so
`import ai.trade_journal` **always** resolves to
`ai/trade_journal/__init__.py`; the shim file can be read but never
imported by any interpreter. See AI_RISK_REPORT.md and
AI_REFACTOR_RECOMMENDATIONS.md for follow-up.

---

## Top-level files directly under `ai/`

| File | Purpose | Classes | Module functions |
|---|---|---|---|
| `ai/__init__.py` | (empty) | — | — |
| `ai_layer/ai_engine/ai_analyzer.py` | Production entry point `core/pipeline.py` calls | `AIAnalysisResult` (frozen dataclass), `AIAnalyzer` (plain) | — |
| `ai_layer/ai_engine/ai_prompt.py` | Builds a prompt payload for a future LLM call (dead — see finding below) | `PromptPayload` (frozen dataclass) | `_summarize_context()` (private), `build_prompt()` |
| `ai_layer/confidence_ai/confidence_model.py` | Deterministic confidence scoring (dead — only consumer is `ai_prompt.py`) | `ScoringConfig`, `ConfidenceResult` (both frozen dataclass) | `evaluate_confidence()` |
| `ai_layer/ai_service/interfaces.py` | Future-provider contract (Phase 55) | `MarketContext`, `UserContext`, `AIResponse` (frozen dataclass), `AIAnalyzerInterface` (**ABC**) | — |
| `ai_layer/knowledge_ai/learning_context.py` | Bundles Learning data into AI-facing JSON shape (Phase 60.6/60.7) | `LearningContext` (frozen dataclass) | `_recent_failures()`, `_strategy_stats()`, `_pattern_condition()`, `_confidence_summaries()` (private), `build_learning_context()` |
| `ai_layer/ai_engine/intelligence_runtime.py` | Composition root for the Official Intelligence Pipeline (Phase 64.0) | `PipelineStage` (Enum), `PipelineStageResult`, `PipelineRun` (frozen dataclass), `IntelligenceRuntime` (plain) | — |
| `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` | Compatibility shim (Phase 55) — **unreachable, see finding #2** | none (re-exports only) | — |

---

## Subpackage inventory (30 subpackages, alphabetical)

Each entry: purpose (from README/docstring), file → classes/functions.
`__init__.py` is empty for every subpackage below (finding #1) — not
repeated per-entry.

### `ai/access/` — Access control, roles, usage limits (Phase 61.0/61.1/61.4)
- `access_control.py` — `AccessControl` (plain)
- `identity_checker.py` — `is_phone_reused_by_another_account()`
- `permission_service.py` — `resolve_ai_role()`
- `permissions.py` — `AIRole` (Enum: OWNER/ADMIN/VIP/PREMIUM/FREE)
- `subscription_policy.py` — `plan_to_ai_role()`
- `tool_permissions.py` — `ToolPermissions` (plain)
- `trial_manager.py` — `TrialEligibilityResult`, `TrialStatus` (frozen dataclass), `TrialManager` (plain); `trial_status_from_started_at()`
- `usage_limits.py` — `UsageCheckResult` (frozen dataclass), `UsageLimiter` (plain)
- `user_capability.py` — `UserCapability` (frozen dataclass), `UserCapabilityService` (plain)

### `ai/analyzer/` — Canonical-analyzer re-export (Phase 55, dead code)
- `ai_analyzer.py` — pure re-export of `ai_layer.ai_engine.ai_analyzer`; defines its own `__all__`

### `ai/audit/` — In-memory AI call audit trail (Phase 61.0/61.3/61.4/61.6)
- `provider_stats.py` — `ProviderStats`, `DailyUsage`, `RuntimeMetrics` (frozen dataclass), `RuntimeMetricsCollector` (plain); `compute_provider_stats()`, `rank_providers()`, `compute_requests_per_minute()`, `compute_daily_usage()`, `evaluate_cost_protection()`
- `request_log.py` — `AIRequestLogEntry` (frozen dataclass), `RequestLog` (plain)
- `response_log.py` — `AIResponseLogEntry` (frozen dataclass), `ResponseLog` (plain)
- `trace.py` — `RuntimeTrace` (frozen dataclass); `trace_request()`
- `usage_accounting.py` — `UserUsageStats` (frozen dataclass); `compute_user_usage()`

### `ai/cache/` — TTL response cache (Phase 61.1, corrected 61.1.1)
- `cache_policy.py` — `CacheKey`, `CachePolicy` (frozen dataclass); `compute_context_hash()`, `build_cache_key_from_context()`
- `response_cache.py` — `CacheEntry` (frozen dataclass), `ResponseCache` (plain)

### `ai/capabilities/` — Capability vocabulary + toggles (Phase 61.0)
- `capability.py` — `Capability` (Enum)
- `capability_manager.py` — `CapabilityManager` (plain); `get_capability_manager()` (singleton accessor)
- `capability_registry.py` — `CapabilityDescriptor` (frozen dataclass); `build_capability_registry()`

### `ai/chart_intelligence/` — Chart interpretation pipeline (Phase 66.1)
- `access.py` — `is_chart_intelligence_enabled_for()`
- `chart_runtime.py` — `ChartRuntime` (plain); `_confidence_to_unit_scale()` (private)
- `content_adapter.py` — `chart_analysis_to_content_body()`, `prepare_content()`
- `models.py` — `ChartImageType`, `ChartAnalysisType` (Enum), `ChartContext`, `ChartAnalysisInput`, `ChartAnalysis` (frozen dataclass); `has_minimum_context()`, `generate_chart_id()`
- `trading_analyst_adapter.py` — `combined_explanation()`
- `vision_provider_types.py` — `ChartVisionProviderType` (Enum, future vendor vocabulary only)

### `ai/coaching/` — Coaching recommendations from Learning/Journal (Phase 66.4)
- `access.py` — `is_coaching_intelligence_enabled_for()`
- `coaching_runtime.py` — `CoachingRuntime` (plain)
- `journal_adapter.py` — `journal_entry_to_coaching_input()`
- `learning_adapter.py` — `learning_record_to_coaching_input()`
- `models.py` — `CoachingTopic`, `CoachingPriority`, `CoachingType`, `CoachingStatus` (Enum), `CoachingRecommendation` (frozen dataclass); `generate_coach_id()`

### `ai/content/` — Content generation contract (Phase 61.5/63.6)
- `broadcast_output.py` — `BroadcastReadyContent` (frozen dataclass); `prepare_broadcast()`
- `content_adapter.py` — `ContentEngine` (plain, wraps `AIService.ask()`); `_build_prompt()` (private)
- `content_adapters.py` — `content_context_from_explanation()`, `content_context_from_conversation()`
- `content_schema.py` — `ContentRequest`, `ContentResult` (frozen dataclass)
- `content_types.py` — `ContentType` (Enum); `is_content_capability()`, `content_title()`
- `models.py` — `ContentMode` (Enum), `ContentMetadata`, `ContentContext` (frozen dataclass)

### `ai/context/` — AI Context composition (Phase 61.0/61.1.1/61.3)
- `context_adapter.py` — `sanitize_market_context()`, `market_context_from_snapshot()`
- `context_builder.py` — `build_ai_context()`
- `context_snapshot.py` — `AIContext` (frozen dataclass)

### `ai/conversation/` — Conversation engine (Phase 61.3/63.5)
- `conversation_adapters.py` — `knowledge_key_from_entry()`, `memory_key_from_entry()`, `reasoning_key_from_result()`, `conversation_context_to_explanation_fields()`
- `conversation_engine.py` — `ConversationResult` (frozen dataclass), `ConversationEngine` (plain); `_format_prompt()` (private)
- `models.py` — `ConversationMode` (Enum), `ConversationContext` (frozen dataclass)

### `ai/explanation/` — Explanation Engine (Phase 61.3/63.0/63.1)
- `explanation_builder.py` — `ExplanationBuilder` (plain); `_confidence_to_unit_scale()`, `_title_for()`, `_summary_for()` (private)
- `explanation_content_adapter.py` — `explanation_to_broadcast_ready()`
- `explanation_engine.py` — `ExplanationEngine` (plain); `_format_signal_explanation()` (private)
- `explanation_input.py` — `ExplanationMode` (Enum), `ExplanationInput` (frozen dataclass)
- `explanation_output.py` — `ExplanationOutput` (frozen dataclass)
- `explanation_templates.py` — `_or_not_specified()` (private); `build_trade_explanation()`, `build_no_trade_explanation()`, `build_education_explanation()`

### `ai/journal/` — Trade journal foundation (Phase 55/59)
- `failure_analysis.py` — `FailureAnalysisEntry` (frozen dataclass); `create_failure_analysis_entry()`
- `trade_journal.py` — `TradeOutcome`, `DecisionType` (Enum), `TradeJournalEntry` (frozen dataclass — **name collides with `ai/trade_journal/models.py`'s unrelated class of the same name**); `create_journal_entry()`

### `ai/learning/` — Per-topic mastery tracking (Phase 66.3)
- `access.py` — `is_learning_intelligence_enabled_for()`
- `journal_adapter.py` — `journal_entry_to_learning_input()`
- `learning_runtime.py` — `LearningRuntime` (plain)
- `memory_adapter.py` — `memory_reference_key()`
- `models.py` — `LearningTopic`, `LearningLevel`, `LearningSource`, `LearningStatus` (Enum), `LearningRecord` (frozen dataclass); `generate_learning_id()`

*(Distinct from the sibling top-level `learning/` package outside `ai/`, which is out of scope for this inventory.)*

### `ai/memory/` — In-process memory foundation (Phase 55/61.3/63.3)
- `context_memory.py` — `ContextMemory` (plain)
- `memory_registry.py` — `MemoryScopeDescriptor` (frozen dataclass); `build_memory_scope_registry()`, `describe()`
- `memory_runtime.py` — `MemoryLayer` (Enum), `MemoryRuntime` (plain, 5-layer facade)
- `models.py` — `MemoryType`, `MemoryPriority`, `MemoryScope` (Enum), `MemoryEntry` (frozen dataclass)

### `ai/performance/` — Per-trade performance observations (Phase 66.5)
- `access.py` — `is_performance_intelligence_enabled_for()`
- `analytics_adapter.py` — `performance_records_to_win_rate_metric()`
- `coaching_adapter.py` — `performance_record_to_coaching_input()`
- `journal_adapter.py` — `journal_entry_to_performance_input()`
- `memory_adapter.py` — `performance_memory_key()`
- `models.py` — `PerformanceCategory` (Enum), `PerformanceRecord`, `PerformanceMetric` (frozen dataclass); `generate_performance_id()`
- `performance_runtime.py` — `PerformanceRuntime` (plain)

### `ai/persona/` — AI voice identity (Phase 63.0)
- `persona.py` — `Persona` (frozen dataclass)
- `persona_manager.py` — `PersonaManager` (plain)
- `persona_registry.py` — `build_persona_registry()`

### `ai/portfolio/` — Portfolio-shaped metadata (Phase 66.7)
- `access.py` — `is_portfolio_intelligence_enabled_for()`
- `memory_adapter.py` — `portfolio_reference_key()`
- `models.py` — `PortfolioStatus`, `PortfolioRiskLevel`, `PortfolioHealth` (Enum), `PortfolioRecord` (frozen dataclass); `generate_portfolio_id()`
- `performance_adapter.py` — `performance_record_to_portfolio_input()`
- `portfolio_runtime.py` — `PortfolioRuntime` (plain)
- `strategy_adapter.py` — `strategy_records_to_portfolio_input()`

### `ai/profiles/` — User profile model (Phase 55)
- `user_profile.py` — `AIUserProfile` (frozen dataclass — pure data, no DB access)

### `ai/prompts/` — Prompt template management (Phase 55/61.1/61.1.1)
- `prompt_manager.py` — `PromptManager` (plain — static template registry)
- `prompt_registry.py` — `PromptLifecycleState` (Enum: ACTIVE/DEPRECATED/ARCHIVED), `PromptVersionRecord` (frozen dataclass), `PromptRegistry` (plain)

### `ai/providers/` — Provider contract + implementations (Phase 61.0/61.1/61.2/61.5/61.6) — largest subpackage, 14 files
- `base_provider.py` — `ProviderResult` (frozen dataclass), `BaseAIProvider` (**ABC**)
- `circuit_breaker.py` — `CircuitState` (Enum), `CircuitBreakerConfig` (frozen dataclass), `ProviderCircuitBreaker` (plain)
- `claude_provider.py` — `ClaudeProvider` (real implementation)
- `gemini_provider.py` — `GeminiProvider` (real implementation, live REST calls)
- `grok_provider.py` — `GrokProvider` (real implementation)
- `openai_provider.py` — `OpenAIProvider` (real implementation)
- `placeholder_providers.py` — `_StubProviderMixin` (private), `LocalLLMProvider` (the one remaining placeholder)
- `provider_capabilities.py` — `supports()`, `capabilities_of()`
- `provider_failover.py` — `select_available()`
- `provider_health.py` — `ProviderHealthRecord` (frozen dataclass), `ProviderHealthTracker` (plain)
- `provider_manager.py` — `ProviderStatus` (Enum), `ProviderManager` (plain)
- `provider_registry.py` — `ProviderDescriptor` (frozen dataclass); `build_provider_registry()`
- `provider_status.py` — `HealthStatus` (Enum)
- `runtime_errors.py` — `ProviderRuntimeError(Exception)` + 4 subclasses; `classify_provider_exception()`, `record_provider_failure()`

### `ai/reasoning/` — Structured reasoning foundation (Phase 63.4)
- `models.py` — `ReasoningMode`, `ReasoningType`, `ReasoningPriority` (Enum), `ReasoningStep`, `ReasoningResult` (frozen dataclass)
- `reasoning_adapters.py` — `step_from_knowledge_entry()`, `step_from_memory_entry()`, `reasoning_result_to_explanation_fields()`
- `reasoning_registry.py` — `ReasoningTypeDescriptor` (frozen dataclass); `build_reasoning_type_registry()`, `describe()`
- `reasoning_runtime.py` — `ReasoningRuntime` (plain)

### `ai/research/` — Scientific layer, final 66.x foundation (Phase 66.8)
- `access.py` — `is_research_intelligence_enabled_for()`
- `memory_adapter.py` — `research_reference_key()`
- `models.py` — `ResearchStatus`, `ResearchPriority`, `ResearchCategory` (Enum), `ResearchRecord` (frozen dataclass); `generate_research_id()`
- `performance_adapter.py` — `performance_record_to_research_input()`
- `portfolio_adapter.py` — `portfolio_record_to_research_input()`
- `research_runtime.py` — `ResearchRuntime` (plain)
- `strategy_adapter.py` — `strategy_record_to_research_input()`

### `ai/router/` — Capability → Provider routing (Phase 61.0/61.5)
- `provider_score.py` — `ProviderScore` (frozen dataclass); `_health_component()`, `_latency_component()`, `_cost_component()` (private), `score_provider()`, `score_providers()` — recommendation/analytics only, `AIRouter.route()` does not consume it
- `router.py` — `AIRouter` (plain)
- `routing_result.py` — `RoutingResult` (frozen dataclass)
- `routing_rules.py` — `get_candidate_providers()`

### `ai/runtime/` — AI Service orchestration + lifecycle (Phase 61.2/61.6/61.7) — largest subpackage by responsibility
- `ai_service.py` — `_AttemptScopedHealthTracker` (private), `AIService` (plain — `ask()`: Access→Capability→Router→Provider→Validator→Cache→Audit→Response)
- `event_bus.py` — `EventType` (Enum), `RuntimeEvent` (frozen dataclass), `EventBus` (plain)
- `runtime_events.py` — `RuntimeLifecycleEvent` (frozen dataclass); `create_lifecycle_event()`
- `runtime_manager.py` — `RuntimeManager` (plain — transition-validating state machine)
- `runtime_profiles.py` — `RuntimeProfile` (frozen dataclass); `resolve_profile()`, `apply_provider_priority()`
- `runtime_request.py` / `runtime_response.py` — `RuntimeRequest`, `RuntimeResponse` (frozen dataclass)
- `runtime_state.py` — `RuntimeState` (Enum: INITIALIZING/READY/BUSY/DEGRADED/FAILED/SHUTDOWN), `RuntimeStateRecord` (frozen dataclass); `is_valid_transition()`
- `self_check.py` — `CheckStatus` (Enum), `SelfCheckResult`, `RuntimeSelfCheckReport` (frozen dataclass); 7 private `_check_*` probes, `run_self_check()`

### `ai/session/` — Temporary conversation session (Phase 61.0)
- `context_window.py` — `ContextWindow` (plain — caps turn pairs, not tokens)
- `conversation_state.py` — `ConversationTurn` (frozen dataclass), `ConversationState` (**mutable dataclass — the one exception to this codebase's frozen-dataclass convention**)
- `session_manager.py` — `SessionManager` (plain)

### `ai/strategy/` — Strategy-shaped metadata (Phase 66.6)
- `access.py` — `is_strategy_intelligence_enabled_for()`
- `journal_adapter.py` — `journal_entry_to_strategy_input()`
- `memory_adapter.py` — `strategy_reference_key()`
- `models.py` — `StrategyType`, `StrategyStatus`, `StrategyConfidence` (Enum), `StrategyRecord` (frozen dataclass); `generate_strategy_id()`
- `performance_adapter.py` — `performance_record_to_strategy_input()`
- `strategy_runtime.py` — `StrategyRuntime` (plain)

### `ai/tools/` — AI Tool contract + 5 tools (Phase 61.0/61.3)
- `analytics_tool.py`, `education_tool.py`, `learning_tool.py`, `market_tool.py`, `news_tool.py` — one `*Tool` class each, all base `BaseAITool`
- `tool_registry.py` — `ToolResult` (frozen dataclass), `BaseAITool` (**ABC**, defined here), `ToolRegistry` (plain); `build_default_tool_registry()` (lazy-imports the 5 tools to avoid a module-level cycle)

### `ai/trade_journal/` — Trade journal, narrative record (Phase 66.2)
**Name collision with top-level `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` — see cross-cutting finding #2.**
- `access.py` — `is_trade_journal_enabled_for()`
- `journal_runtime.py` — `TradeJournalRuntime` (plain)
- `memory_adapter.py` — `memory_reference_key()`
- `models.py` — `TradeJournalEntry` (frozen dataclass — **same class name, different type, as `ai/journal/trade_journal.py`'s `TradeJournalEntry`**, self-documented in this file), `ReplayContext` (frozen dataclass); `generate_journal_id()`
- `trading_analyst_adapter.py` — `journal_entry_from_trading_and_chart()`

### `ai/trading_analyst/` — First 66.x subpackage (Phase 66.0)
- `access.py` — `is_trading_analyst_enabled_for()`
- `analyst_runtime.py` — `TradingAnalystRuntime` (plain); `_confidence_to_unit_scale()`, `_recommendation_for()` (private)
- `content_adapter.py` — `trading_analysis_to_content_body()`, `prepare_content()`
- `models.py` — `TradingRiskLevel` (Enum), `TradingAnalysisInput`, `TradingAnalysis` (frozen dataclass)

### `ai/validation/` — Response validation (Phase 61.2)
- `response_validator.py` — `ValidationResult` (frozen dataclass); `validate_response()`
- `safety.py` — `check_safety()`
- `schemas.py` — `ResponseSchema` (frozen dataclass)

---

## Summary tallies

- **30 subpackages**, all with completely empty `__init__.py`.
- **182 total `.py` files** (including 30 empty `__init__.py` + 8 top-level `ai/*.py` modules).
- **~115 top-level classes**. By shape:
  - Majority: `@dataclass(frozen=True)` value/result objects — the dominant idiom.
  - **Enums**: ~35 (`AIRole`, `Capability`, `RuntimeState`, `CircuitState`, `MemoryType/Priority/Scope/Layer`, per-66.x-subpackage Status/Priority/Type enums, etc.)
  - **`ABC`/interface classes**: exactly 3 — `AIAnalyzerInterface`, `BaseAIProvider`, `BaseAITool`.
  - **Exception hierarchy**: `ProviderRuntimeError(Exception)` + 4 subclasses.
  - **Plain classes**: the "Manager"/"Runtime"/"Registry"/"Service"/"Engine" family, one per subpackage.
  - Exactly **one mutable dataclass** in the entire tree: `ai/session/conversation_state.py:ConversationState`.
- **Module-level functions**: dominated by `is_X_enabled_for(role, flags)` gates (one per 66.x subpackage), `generate_X_id()` UUID4 factories, and `*_adapter.py` pure-transform functions with no shared base class.

See `AI_DEPENDENCY_GRAPH.md` for the import graph built from this
inventory, and `AI_RESPONSIBILITY_MATRIX.md` for the per-module
Purpose/Responsibilities/API breakdown.
