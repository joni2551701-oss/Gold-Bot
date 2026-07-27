# AI_FOUNDATION_READINESS.md — TASK-AI-000 Phase 5: AI Readiness

Status: **AUDIT ONLY**. No code changed. Determined from actual code
(class definitions, grep results), not from assumption — every
"missing" verdict below is backed by a zero-hit grep across the whole
repository.

| Component | Status | Evidence |
|---|---|---|
| **AI Manager** | **PARTIAL** | No class literally named `AIManager` exists anywhere (`grep -rn "AIManager"` → 0 hits). Instead, several domain-scoped managers each own one narrow slice: `ProviderManager` (`ai/providers/provider_manager.py:30`), `CapabilityManager` (`ai/capabilities/capability_manager.py:28`), `SessionManager` (`ai/session/session_manager.py:23`), `PromptManager` (`ai/prompts/prompt_manager.py:63`), `PersonaManager` (`ai/persona/persona_manager.py:16`), `TrialManager` (`ai/access/trial_manager.py:71`), `RuntimeManager` (`ai/runtime/runtime_manager.py:53`, operational lifecycle only). The closest thing to a top-level orchestrator is `ai/intelligence_runtime.py`'s `IntelligenceRuntime` (explicitly "the one composition root for the Official Intelligence Pipeline," documented as filling a gap where "no orchestrator existed anywhere in the codebase before this phase" per `docs/PHASE64_0_AUDIT.md`) and `ai/runtime/ai_service.py`'s `AIService` (request-scoped orchestrator: Access→Capability→Router→Provider→Validator→Cache→Audit→Response). |
| **AI Registry** | **EXISTS / functional, per-subsystem** | Multiple instances of the same "descriptor + build function" shape: `provider_registry.py:39 build_provider_registry()`, `capability_registry.py` (modeled explicitly on `configuration/feature_registry.py`'s pattern), `tool_registry.py:48 class ToolRegistry` (register/get/list_tools), plus `persona_registry.py`, `memory_registry.py`, `prompt_registry.py`, `reasoning_registry.py`. No single registry spans providers+capabilities+tools in one object — each subsystem has its own. |
| **Factory** | **PARTIAL** | No class literally named `*Factory` exists (`grep -rn "class.*Factory"` → 0 hits in `ai/`). The functional equivalent is the registry build functions: `provider_registry.py:39 build_provider_registry()` directly constructs `OpenAIProvider()`/`GeminiProvider()`/`ClaudeProvider()`/`GrokProvider()`/`LocalLLMProvider()`; `tool_registry.py:64 build_default_tool_registry()` does the same for tools; `session_manager.py:28 SessionManager.create_session()` constructs `ConversationState` on demand. Factory-shaped, not Factory-named. |
| **Session** | **READY / functional** | `ai/session/session_manager.py:23 SessionManager` — `create_session()`, `get_session()`, `end_session()`, `is_expired()`, `purge_expired()`. Backed by `ConversationState` (`session_id`, `telegram_id`, `created_at`, `last_activity`). In-memory only, 30-minute default TTL, no persistence, no background expiry job. |
| **Context** | **READY / functional** | `ai/context/context_builder.py:44 build_ai_context()` — composes Market Context/Signal Schema/User Profile/Trade History/Learning Context into one bundle; AI never receives raw market data. `context_snapshot.py`'s `AIContext` carries `snapshot_id`/`context_version` for deterministic cache-key identity (added Phase 61.1.1). `context_adapter.py`'s `market_context_from_snapshot()` is the AI-side adapter over the trading-side `context/` layer's snapshot. |
| **Lifecycle** | **READY / functional, scoped to `ai/runtime/`** | `ai/runtime/runtime_manager.py:53 RuntimeManager` — transition-validating state machine over `RuntimeState` (INITIALIZING/READY/BUSY/DEGRADED/FAILED/SHUTDOWN), with `transition()`, `is_healthy()`, a recorded `_history` of lifecycle events. Real, load-bearing: `AIService.ask()`'s first action is a health gate via `is_healthy()` (Phase 61.7). Companion: `ProviderCircuitBreaker` (CLOSED/OPEN/HALF_OPEN). Explicitly **not** wired into `core/pipeline.py`/`decision/`/`risk/`/`execution/` by design. Scoped only to `ai/runtime/`'s own operational self-awareness — no lifecycle exists for `ai/` as a whole, or for `assistant/` (which is documented as "in-memory only, no persistence, no background job"). |
| **Interfaces** | **READY / functional** | Three formal ABC-based contracts: `ai/interfaces.py:65 AIAnalyzerInterface` (abstract `evaluate()`, documented as a contract for a *future* AI Assistant Core that production `ai/ai_analyzer.py`'s `AIAnalyzer` does **not** currently implement); `ai/providers/base_provider.py:28 BaseAIProvider` (the contract every vendor provider implements, with `health_check()`/`capabilities()` as concrete defaults); `ai/tools/tool_registry.py:32 BaseAITool` (name/description/run contract for the 5 tools). No use of `typing.Protocol` anywhere in `ai/` — ABC is the exclusive interface mechanism. |

## Summary

| # | Component | Status |
|---|---|---|
| 1 | AI Manager | PARTIAL |
| 2 | AI Registry | EXISTS (per-subsystem, not unified) |
| 3 | Factory | PARTIAL |
| 4 | Session | READY |
| 5 | Context | READY |
| 6 | Lifecycle | READY (scoped to `ai/runtime/`) |
| 7 | Interfaces | READY |

**Bottom line**: the foundation is more built than a first glance
suggests — 4 of 7 components are fully functional, and the 3
"partial" verdicts (Manager, Registry-unification, Factory) are gaps
in *naming and unification*, not gaps in underlying capability. Every
piece a unified `AIManager` would need to orchestrate already exists
somewhere in `ai/`; nothing currently ties them into one top-level
entry point by that name. See `AI_GAP_ANALYSIS.md` for what closing
that gap would concretely require.
