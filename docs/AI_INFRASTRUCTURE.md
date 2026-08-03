# AI Infrastructure (Phase 61.0: AI Infrastructure Foundation)

The first v0.4 AI Core phase, built directly on top of the frozen
Foundation Layer (`docs/FOUNDATION_FREEZE_v0.4.md`). Eight new,
provider-agnostic and capability-agnostic `ai/` subpackages — no real
AI/LLM API call anywhere in this phase, no change to
`core/pipeline.py`, `strategies/`, `signals/`, `decision/`, `risk/`,
`execution/`, or `lifecycle/`. Full reuse audit:
`docs/PHASE61_AI_FOUNDATION_AUDIT.md`.

AI stays advisory-only, exactly as `ai_layer/ai_service/interfaces.py`'s
`AIAnalyzerInterface` and `docs/FOUNDATION_FREEZE_v0.4.md`'s "AI
Optional" principle already establish. Nothing built this phase
approves/rejects a trade, calls `risk_layer.risk_engine.risk_manager.RiskManager`,
bypasses `decision_layer.decision_engine.decision_engine.DecisionEngine`, or generates a
signal.

## Why eight packages

TASK 1's reuse audit found no existing module already provides a
capability toggle, a multi-vendor provider abstraction, a
capability-to-provider router, a bundled AI-facing context type, a
role-based AI entitlement matrix, a temporary conversation session, an
AI-facing tool interface, or an AI-call audit trail. Each package below
composes existing `ai/` types (`MarketContext`, `LearningContext`,
`AIUserProfile`, `TradeJournalEntry`) rather than duplicating their
logic — see the audit doc's per-module table for the full reasoning.

## `ai/capabilities/`

`Capability` (CHAT/ANALYSIS/EXPLANATION/SUMMARY/MEMORY/EDUCATION/
TOOL_CALLING/VISION/IMAGE/VIDEO/VOICE/DOCUMENT) names *what* the AI
layer can be asked to do — it never knows *which vendor* answers it.
`CapabilityManager` tracks a live enabled/disabled state per
capability, seeded from `capability_registry.py`'s defaults (the six
nearer-term capabilities default enabled; the remaining six default
disabled, declared for a stable future name).

## `ai/providers/`

`BaseAIProvider` is the contract every vendor implementation
satisfies (`analyze`/`chat`/`explain`/`vision`/`image`/`voice`, each
returning a `ProviderResult`). Five placeholder providers
(`OpenAIProvider`/`GeminiProvider`/`ClaudeProvider`/`GrokProvider`/
`LocalLLMProvider`) implement it with fixed stub responses — no real
network call. `ProviderManager` owns Preferred -> Fallback -> Disabled
selection (`ProviderStatus`) over `provider_registry.py`'s static
catalog; every provider defaults to FALLBACK.

## `ai/router/`

`AIRouter.route(capability)` returns a `RoutingResult` naming the
selected provider, or `None` with a reason if none is available.
Selection is entirely data-driven: `routing_rules.py`'s `ROUTING_RULES`
dict maps each `Capability` to an ordered tuple of candidate provider
names (e.g. `EXPLANATION -> ("gemini", "openai", "claude")`,
`IMAGE -> ("openai",)`) — adding or reordering a candidate is a
one-line data edit, never a change to `router.py`'s own selection
logic ("Hardcode YO'Q"). The router walks the candidate list and
returns the first one `ProviderManager` reports as registered and not
DISABLED; it optionally also checks a `CapabilityManager` first, if one
is supplied.

## `ai/context/`

`AIContext` bundles the five inputs the brief names — Market Context
(`ai_layer.ai_service.interfaces.MarketContext`, sanitized through
`context_adapter.sanitize_market_context()` to strip any accidental
raw-candle metadata key), Signal Schema (`signal_layer.signal_builder.schema.SignalSchema`),
User Profile (`ai_layer.personal_ai.user_profile.user_profile.AIUserProfile`), Trade History
(`ai_layer.knowledge_ai.knowledge_base.journal.trade_journal.TradeJournalEntry` list), and Learning
Context (`ai_layer.knowledge_ai.learning_context.LearningContext`). `build_ai_context()`
is pure composition: every input is optional, none is fetched or
computed by this package. **AI never receives raw market data** — no
`data/` type is imported anywhere in `ai/context/`.

## `ai/access/`

`AIRole` (OWNER/ADMIN/VIP/PREMIUM/FREE) is deliberately distinct from
`platform_layer/telegram/owner/owner_roles.py`'s `OwnerRole` and
`platform_layer/telegram/permissions.py`'s `PermissionLevel` — see the audit doc for
why reusing either would conflate admin-console access with
subscription-tier AI entitlement. `AccessControl.is_allowed(role,
capability)` answers a *capability* permission question, never a
global AI on/off switch. `UsageLimiter` is a separate, in-memory
per-(user, capability) daily call ceiling, keyed by `AIRole`.

## `ai/session/`

`SessionManager` creates/fetches/ends a `ConversationState` — a
**temporary** conversation ("Session != Memory, Session vaqtinchalik"),
explicitly distinct from `ai/memory/context_memory.py`'s longer-lived,
arbitrary per-key `ContextMemory`. `ContextWindow` trims a session's
turn history to the most recent N turns. No persistence, no background
expiry job — `is_expired()`/`purge_expired()` take an explicit `now`.

## `ai/tools/`

`BaseAITool` is the shared contract for four placeholder tools
(`MarketTool`/`NewsTool`/`AnalyticsTool`/`EducationTool`), each
returning a fixed stub `ToolResult`. **No tool calls `database/` or
`core/pipeline.py`** — every `run()` is interface-only this phase.
`ToolRegistry`/`build_default_tool_registry()` catalog them.

## `ai/audit/`

`RequestLog`/`ResponseLog` record an AI call attempt and its outcome
(provider/latency/token/cost/status/capability) in memory —
deliberately not wired to `database_layer/audit_log/audit_log_repository.py` this
phase (that repository is scoped to Infrastructure/Trading-control
actions; see the audit doc). `provider_stats.compute_provider_stats()`
aggregates an already-recorded response history into per-provider
`ProviderStats` (call count, success rate, average latency, tokens,
cost) — pure aggregation, no new data collection.

## Not wired

Every module in this document is foundation only — none is imported by
`core/pipeline.py`, any live Telegram handler, or
`platform_layer/telegram/command_router.py`. A future integration phase connects
these pieces to a real caller, following the same "foundation, not
live-wired" posture every Phase 59-60 module used before its own
integration phase.

## Tests

`tests/ai/capabilities/`, `tests/ai/providers/`, `tests/ai/router/`,
`tests/ai/context/`, `tests/ai/access/`, `tests/ai/session/`,
`tests/ai/tools/`, `tests/ai/audit/` — one test module per package
(plus a dedicated placeholder-provider test file), covering
construction, default state, and the one piece of real logic each
package has (capability toggling, provider selection order, routing
rule lookup, context sanitization, permission matrix, session
expiry/trimming, tool registration, stats aggregation).
