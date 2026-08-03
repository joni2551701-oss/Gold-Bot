# ai/

## Purpose
Advisory-only AI evaluation layer. As of Phase 55, this is a
**foundation** for a future AI Assistant Core — no real AI/LLM call
happens anywhere in this directory.

## Flow
```
Signal Candidate + Context
      |
      v
AI Layer   -- advisory only, never approves/rejects itself
      |
      v
Decision Engine
```

## Responsibilities
- `ai_analyzer.py` — the production entry point `core/pipeline.py`
  calls. Currently a permanent-reject heuristic stub (documented,
  intentional — see the README's top-level Environment Variables
  table and `docs/AI_ARCHITECTURE.md`).
- `interfaces.py` — `AIAnalyzerInterface`/`MarketContext`/
  `UserContext`/`AIResponse`: the contract a future provider
  implements.
- `memory/`, `prompts/`, `profiles/`, `journal/`, `analyzer/` —
  Phase 55 foundation subpackages (memory, prompt templates, user
  profile model, trade journal, and a re-export of the canonical
  analyzer respectively). None are wired into the production pipeline.
- `learning_context.py` (Phase 60.6: Learning Loop Foundation, TASK 7;
  extended Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 6)
  — `LearningContext` + `build_learning_context()`: bundles
  already-computed `learning/` data (`recent_failures`/
  `successful_patterns`/`strategy_stats`, plus Phase 60.7's
  `patterns`/`failures`/`regimes`/`confidence`) into the Director's own
  AI-facing JSON shape. Generates no explanation/recommendation text
  itself — that is left to a future AI consumer, still bound by
  `AIAnalyzerInterface`'s advisory-only contract. See
  `docs/LEARNING_LOOP.md`.

## Input
`SignalCandidate` + `ContextSnapshot` (production `AIAnalyzer`); the
new foundation types (`MarketContext`/`UserContext`) for anything
built against `interfaces.py` in a future phase; an already-built
`Sequence[learning.models.LearningRecord]` for `learning_context.py`.

## Output
`AIAnalysisResult` (production); `AIResponse` (future interface
shape); `LearningContext` (`learning_context.py`).

## Dependencies
`context/` and `signals/` for the production/interface path. No
dependency on `database/` or `telegram/` — an AI provider must never
reach either directly (see `CLAUDE.md`'s Trading Safety rules).
`learning_context.py` (Phase 60.6, extended 60.7) additionally imports
`analytics.strategy_report.compute_win_rate`,
`learning.models`/`learning.pattern_detector`, and
`learning.confidence.compute_pattern_confidence` — read-only, no
trading-decision logic, and still no `database/`/`telegram/`
dependency.

## AI Infrastructure Foundation (Phase 61.0)

Eight new subpackages, built on top of the frozen Foundation Layer,
none wired into the production pipeline — see `docs/AI_INFRASTRUCTURE.md`
for the full picture and `docs/PHASE61_AI_FOUNDATION_AUDIT.md` for the
reuse audit that justified each one:

- `capabilities/` — `Capability` enum + `CapabilityManager`: what the
  AI layer can be asked to do, independently toggleable, never
  provider-aware.
- `providers/` — `BaseAIProvider` contract + five placeholder vendor
  stubs (OpenAI/Gemini/Claude/Grok/Local LLM, no real API call) +
  `ProviderManager`'s Preferred/Fallback/Disabled selection.
- `router/` — `AIRouter`: Capability -> Provider -> Return, via a
  data-driven `routing_rules.py` table, never a hardcoded branch.
- `context/` — `AIContext` + `build_ai_context()`: composes Market
  Context/Signal Schema/User Profile/Trade History/Learning Context
  into one bundle; AI never receives raw market data.
- `access/` — `AIRole` (OWNER/ADMIN/VIP/PREMIUM/FREE) x `Capability`
  permission matrix (`AccessControl`) + `UsageLimiter` daily ceilings.
- `session/` — `SessionManager`/`ConversationState`/`ContextWindow`: a
  temporary conversation, distinct from `memory/`'s longer-lived store.
- `tools/` — `BaseAITool` + four placeholder tools (market/news/
  analytics/education), interface only, no database/pipeline call.
- `audit/` — `RequestLog`/`ResponseLog`/`provider_stats`: in-memory AI
  call audit trail (provider/latency/token/cost/status/capability).

## AI Provider Reliability Foundation (Phase 61.1)

A narrower "Provider Foundation" pass over five Phase 61.0 packages,
plus a new `ai/cache/` package — see `docs/AI_PROVIDER_FOUNDATION.md`
and `docs/PHASE61_1_PROVIDER_AUDIT.md` (reuse audit):

- `providers/provider_health.py` + `provider_status.py` +
  `provider_failover.py` — observed health (ONLINE/DEGRADED/
  RATE_LIMITED/OFFLINE/DISABLED), separate from `ProviderManager`'s
  owner-intent status; `select_available()` picks the first healthy
  candidate.
- `providers/provider_capabilities.py` — which `Capability` each
  provider actually declares support for; the router now checks this
  before selecting.
- `router/router.py` — extended selection order (capability matrix ->
  provider status -> health) + read-only `provider_metrics()` reusing
  `audit/provider_stats.py` (no new metrics module).
- `prompts/prompt_registry.py` — Version/Active/Rollback over
  `PromptManager`'s existing templates; `PromptManager` itself
  unmodified.
- `access/tool_permissions.py` — Role x Tool matrix, a second axis
  beside the existing Role x Capability matrix.
- `context/context_snapshot.py` — `+schema_version`/`context_version`,
  additive, backwards compatible.
- `cache/` (new) — `response_cache.py` + `cache_policy.py`: a TTL
  cache whose key structurally requires Capability + Context Version +
  Provider + Prompt Version + Context Hash (never bare prompt text).

## AI Foundation Corrections (Phase 61.1.1)

Small, corrections-only pass, no new package — see
`docs/PHASE61_1_1_FOUNDATION_CORRECTIONS.md`:

- `context/context_builder.py` + `context/context_snapshot.py` —
  `AIContext.snapshot_id`, a deterministic, content-derived identity
  (never time/random-derived), computed only by `build_ai_context()`.
- `cache/cache_policy.py` — `CacheKey` gained `snapshot_id` as a sixth,
  required field; `build_cache_key_from_context()` is the blessed
  constructor, pulling it from an `AIContext` rather than letting a
  caller invent one.
- `prompts/prompt_registry.py` — `PromptLifecycleState`
  (ACTIVE/DEPRECATED/ARCHIVED); `set_active()`/`rollback()` refuse to
  select a non-ACTIVE version.
- `docs/AI_PROVIDER_FOUNDATION.md` — documentation-only "Provider
  Preference vs Provider Health" correction, no code change.

## AI Runtime Foundation (Phase 61.2)

The first real, end-to-end AI request lifecycle — see
`docs/AI_RUNTIME_FOUNDATION.md` and `docs/PHASE61_2_RUNTIME_AUDIT.md`
(AI Isolation Audit):

- `providers/gemini_provider.py` — the first non-placeholder
  `BaseAIProvider`; real Gemini REST calls via `requests`, key read
  only through `core_layer/secrets/secrets.py`, never in a URL. Replaced the
  placeholder Gemini entry in `placeholder_providers.py`/
  `provider_registry.py`.
- `providers/runtime_errors.py` — `ProviderRuntimeError` hierarchy +
  `record_provider_failure()` (error -> `ProviderHealthTracker` ->
  router fallback).
- `validation/` (new) — `response_validator.py`/`schemas.py`/
  `safety.py`: format/confidence/safety checks on every real
  provider response before it is cached or returned.
- `runtime/` (new) — `ai_service.py`'s `AIService.ask()`: the first
  real orchestration (Access -> Capability -> Router -> Provider ->
  Validator -> Cache -> Audit -> Response). Never imports `decision/`,
  `risk/`, `execution/`, `strategies/`, or `signals/`.
- `cache/cache_policy.py` — `CacheKey` gained a seventh field,
  `user_role` (a privilege-boundary concern independent of
  `snapshot_id`'s freshness concern).
- `audit/provider_stats.py` — `ProviderStats.failure_count` added;
  now fed by real `AIService` calls, still observability-only (the
  router never reads it back).
- `core_layer/secrets/secrets.py` — `OPENAI_API_KEY`/`CLAUDE_API_KEY`/
  `GROK_API_KEY`/`LOCAL_LLM_CONFIG`, all optional.

## AI Intelligence Layer (Phase 61.3)

Makes the Phase 61.2 runtime lifecycle usable — see
`docs/AI_INTELLIGENCE_LAYER.md` and
`docs/PHASE61_3_INTELLIGENCE_AUDIT.md` (reuse audit):

- `context/context_adapter.py` — `market_context_from_snapshot()`, the
  `ContextSnapshotSchema -> MarketContext` adapter, `TYPE_CHECKING`-only.
- `knowledge/` (new top-level package, sibling to `ai/`, zero
  dependencies) — static SMC/Wyckoff/Risk/Psychology/Examples/FAQ
  entries + `registry.py` lookup.
- `tools/*.py` — all five tools (`market_tool`/`news_tool`/
  `analytics_tool`/`education_tool`/`learning_tool`, new) given real,
  read-only logic over already-built input objects (never a direct
  `database/` read).
- `conversation/conversation_engine.py` — `ConversationEngine`, the
  first real caller of `session/` and `runtime/ai_service.py`.
- `memory/memory_runtime.py` — `MemoryRuntime`, a 5-layer facade over
  `memory/context_memory.py`'s `ContextMemory` (unmodified).
- `explanation/explanation_engine.py` — `ExplanationEngine`, wraps
  `AIService` for EXPLANATION/SUMMARY/EDUCATION/ANALYSIS.
- `runtime/runtime_response.py` — `RuntimeResponse.request_id`;
  `audit/trace.py` (new) — `trace_request()` joins `RequestLog`/
  `ResponseLog`.
- `audit/provider_stats.py` — `rank_providers()`, extended in place.

## AI Product & Control Layer (Phase 61.4)

The real access-control and owner-control layer around the AI Core —
see `docs/AI_PRODUCT_CONTROL_LAYER.md` and
`docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md` (reuse audit):

- `access/permission_service.py`/`subscription_policy.py`/
  `user_capability.py` — the real `telegram_id -> AIRole` resolver.
  Accepts already-resolved identity facts (`is_owner`/`is_admin`/
  `plan`) from the caller; never imports `telegram/`/`database/`
  itself.
- `access/tool_permissions.py` — corrected in place (`"learning_tool"`
  was missing from every role's set).
- `access/usage_limits.py` — `set_limit()` added; `__init__` now
  copies its default limits dict instead of aliasing it (a real bug
  fix — the alias could have let one instance's `set_limit()` mutate
  every other instance's defaults).
- `access/identity_checker.py`/`trial_manager.py` — "1 phone = 1
  trial" enforcement; a pure phone-reuse check plus an in-memory
  7-day trial window.
- `audit/usage_accounting.py` — `compute_user_usage()`, a per-user
  cost/token aggregation generalizing `audit/trace.py`'s existing
  join.
- `core/phone_hash.py` (outside `ai/`) — salted phone-number hashing;
  the raw phone number is never stored.
- `telegram/owner/ai_commands.py` (outside `ai/`) — `/ai_status`,
  `/ai_provider`, `/ai_disable`, `/ai_enable`, `/ai_limit`,
  `/ai_cost`, `/ai_usage`, foundation only.

## AI Production Integration Foundation (Phase 61.5)

The first phase in the entire 61.x arc with real live-wiring — see
`docs/AI_PRODUCTION_INTEGRATION.md` and
`docs/PHASE61_5_PRODUCTION_INTEGRATION_AUDIT.md` (reuse audit):

- `providers/openai_provider.py`/`claude_provider.py`/`grok_provider.py`
  — real, non-placeholder `BaseAIProvider` implementations, replacing
  the corresponding placeholders in `provider_registry.py`, exact same
  pattern as `providers/gemini_provider.py` (Phase 61.2). `local_llm`
  stays the one remaining placeholder.
- `router/provider_score.py` — `ProviderScore`/`score_providers()`,
  recommendation/analytics only. `AIRouter.route()` is unmodified and
  does not consume this — no auto-switching, per the Director's own
  explicit constraint this phase.
- `telegram/owner/ai_commands.py` (outside `ai/`) — **live-wired**:
  `/ai_status`, `/ai_provider`, `/ai_cost`, `/ai_usage`, and the new
  `/ai_health` are now real Telegram commands, ADMIN+OWNER for the
  five read-only ones (`telegram/commands.py`'s `OWNER_COMMANDS` and
  `ADMIN_COMMANDS`, `telegram/handlers.py`'s `{command}_handler`
  functions) — the first live callers this module has ever had.
  `ai_health()` shows per-provider Latency/Success/Requests/Tokens/
  Cost/Failures (Addendum, per Director review). Two new public
  helpers, `ai_runtime_online()`/`current_provider_for()`, de-duplicate
  logic `ai_status()`/`ai_provider()` already had inline and are
  reused by `telegram/owner/dashboard.py`'s new `/owner` command
  (`get_owner_summary()`) and `/doctor` (`get_doctor_report()`,
  OWNER-only self-diagnostic).
- `telegram/user_service.py`'s `register_phone()` (outside `ai/`) —
  **live-wired**: the real `/start` → Phone Share Button → Phone Hash
  → `UserRecord` → Trial Check → FREE account flow.
  `access/identity_checker.py`/`trial_manager.py` (Phase 61.4) are now
  real callers' dependencies rather than untested foundation.
  `trial_manager.py` gained `trial_status_from_started_at()`, a
  stateless extraction of `TrialManager.status_of()`'s own math so a
  database-persisted caller (`UserRecord.trial_started_at`, a new
  additive column) can share it instead of duplicating it.
- `capabilities/capability.py` gained four content capabilities
  (`AI_MARKET_REPORT`/`AI_WEEKLY_OUTLOOK`/`AI_NEWS_ANALYSIS`/
  `AI_SCRIPT_GENERATION`) — extended in place, not a duplicate
  "ContentType" enum.
- `content/` (new) — `content_schema.py`/`content_types.py`/
  `content_adapter.py`/`broadcast_output.py`: `ContentEngine` wraps
  `runtime/ai_service.py`'s `AIService.ask()` unmodified, same pattern
  as `explanation/explanation_engine.py`. Foundation only: none of the
  four content capabilities has a runtime method mapping in
  `ai_service.py`'s `_CAPABILITY_METHOD` yet, so every `generate()`
  call is cleanly rejected today, same "correctly-shaped, not yet
  wired" posture `SUMMARY`/`EDUCATION` have had since Phase 61.3.
  `broadcast_output.py` is a contract-only adapter
  (`ContentResult` → `BroadcastReadyContent`) — no real
  streaming/voice/video/scheduling/send logic.

## AI Operations & Reliability Foundation (Phase 61.6)

Full detail in `docs/AI_RUNTIME_OPERATIONS.md`; reuse audit in
`docs/PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md`. Does not extend AI
Core's capability surface (frozen at the end of Phase 61.5) — makes
the existing AI Core observable, self-aware, and resilient:

- `runtime/runtime_state.py`/`runtime_manager.py`/`runtime_events.py`
  (new) — `RuntimeManager`, a transition-validating lifecycle state
  machine (`INITIALIZING`/`READY`/`BUSY`/`DEGRADED`/`FAILED`/
  `SHUTDOWN`), same shape as `core/emergency/emergency_manager.py`'s
  `EmergencyManager`.
- `providers/circuit_breaker.py` (new) — `ProviderCircuitBreaker`
  (`CLOSED`/`OPEN`/`HALF_OPEN`). Writes every transition into the
  existing `providers/provider_health.py`'s `ProviderHealthTracker` —
  no new provider-state store (Rule 4); `router/router.py` needs zero
  change for the router to automatically respect a tripped breaker.
- `runtime/event_bus.py` (new) — `EventBus`, in-memory decoupled
  pub/sub, nine event types (Phase 61.7 added five more — see below).
  `runtime/ai_service.py` (extended, not rewritten), `runtime/
  runtime_manager.py`, and `providers/circuit_breaker.py` each
  publish; `audit/provider_stats.py`'s `RuntimeMetricsCollector` and
  `telegram/owner/runtime_notifications.py`'s `RuntimeNotifier` each
  subscribe — no module in this list imports another.
- `audit/provider_stats.py` (extended, not new) —
  `compute_requests_per_minute()`, `RuntimeMetrics`,
  `RuntimeMetricsCollector`.
- `runtime/runtime_profiles.py` (new) — `RuntimeProfile`
  (Development/Testing/Production), reusing `cache/cache_policy.py`'s
  `CachePolicy` and `validation/schemas.py`'s `ResponseSchema` rather
  than inventing parallel config types.
- `telegram/owner/runtime_commands.py` / `runtime_notifications.py`
  (new) — `/runtime`, `/runtime_events`, `/runtime_metrics` (pull) and
  Owner-only Provider DOWN/RECOVERED/Runtime FAILED/High Cost/Cache
  Disabled alerts (push).

Trading Pipeline (`core/pipeline.py`/`decision/`/`execution/`/`risk/`/
`strategies/`/`signals/`) has zero diff from this phase.

## AI Platform Stabilization & Integration (Phase 61.7)

Full detail in `docs/PHASE61_7_RUNTIME_INTEGRATION.md`; request flow
in `docs/AI_RUNTIME_FLOW.md`; reuse audit in
`docs/PHASE61_7_INTEGRATION_AUDIT.md`. Closes the gap Phase 61.6
deliberately left open — `RuntimeManager`/`ProviderCircuitBreaker`/
`RuntimeProfile`/`EventBus` are now real, load-bearing parts of
`runtime/ai_service.py`'s own `ask()` flow, not standalone-but-unused
foundation:

- `RuntimeManager` — `ask()`'s first action is a health gate
  (`is_healthy()`).
- `ProviderCircuitBreaker` — gates every real provider call
  (`allow_request()`) and records the outcome (`record_success()`/
  `record_failure()`); a per-request tick lets a tripped breaker move
  `OPEN → HALF_OPEN` once its recovery timeout elapses.
- `RuntimeProfile` — drives `validate_response()`'s schema,
  `ResponseCache`'s TTL policy, and the per-request attempt budget
  when one is injected; `None` reproduces Phase 61.6 exactly.
- `EventBus` gained five more event types this phase
  (`RequestStarted`/`RequestCompleted`/`RequestFailed`/
  `RuntimeStateChanged`/`RetryStarted`/`RetryCompleted`), all
  published from real `ask()`/`RuntimeManager.transition()` control
  flow.
- `runtime/self_check.py` (new) — `run_self_check()`, seven
  independently-wrapped PASS/WARNING/FAILED checks over Provider/
  Runtime/Validation/Cache/Audit/EventBus/CircuitBreaker.
- `telegram/owner/runtime_commands.py` gained `runtime_full_status()`
  (`/runtime_status`) and `runtime_check()` (`/runtime_check`).

**A discovered, intentional behavior change**: a single provider
timeout/unavailable error no longer immediately marks that provider
fully offline — `record_provider_failure()`'s immediate write is now
skipped for those two error types specifically, since the circuit
breaker's 5-consecutive-failure threshold owns that decision instead
(writing OFFLINE on failure 1 would make the breaker's own threshold
unreachable through real usage — found via a real integration test).
A small, local, read-only `_AttemptScopedHealthTracker` in
`ai_service.py` preserves correct same-request failover to a
different, healthy provider without adding a new provider-state store
(Rule 4) or touching `router/router.py`.

`core/pipeline.py`/`decision/`/`execution/`/`risk/`/`strategies/`/
`signals/`, and `ai/router/router.py` itself: zero diff. 2166 tests
passing.

## Future Roadmap
Full audit and folder-structure rationale in `docs/AI_ARCHITECTURE.md`.
The real work — replacing the permanent-reject stub with actual
heuristic/model scoring — is still out of scope (`ai/ai_analyzer.py`
is a separate, live production module this phase does not touch).
Real content generation (a runtime method mapping for the four
`AI_*` capabilities), real Router Intelligence auto-switching, real
Broadcast delivery, `RuntimeProfile.timeout_seconds` enforcement (no
real provider exposes an injectable per-call HTTP timeout yet), and a
persistent, process-wide `AIService` instance in the running bot (every
Telegram command still constructs fresh objects per call) are all
still out of scope — see `docs/PHASE61_7_FREEZE.md`'s "What is still
not wired" section for what comes next. AI Core is now effectively
frozen; the next major directions are v0.5 Business Layer, Owner
Control Center, Broadcast Foundation, Web Dashboard, and an Academy/
Education Platform.
