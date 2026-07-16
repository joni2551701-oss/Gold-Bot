# AI Provider Reliability Foundation (Phase 61.1)

The second v0.4 AI Core phase, scoped narrower than Phase 61.0 on
purpose — a "Provider Foundation" pass over the five packages Phase
61.0 already built (`ai/providers/`, `ai/router/`, `ai/prompts/`,
`ai/audit/`, `ai/access/`), plus one genuinely new package
(`ai/cache/`). No real AI/LLM API call anywhere. AI still does not
connect to `core/pipeline.py`, still never opens a trade, still
advisory-only. Full reuse audit: `docs/PHASE61_1_PROVIDER_AUDIT.md`.

## What changed

### `ai/providers/` — Health, Failover, Capability Matrix (TASK 2/3)

`provider_status.py`'s `HealthStatus` (ONLINE/DEGRADED/RATE_LIMITED/
OFFLINE/DISABLED) is a second, *observed* axis alongside
`provider_manager.ProviderStatus`'s *owner-intent* axis
(PREFERRED/FALLBACK/DISABLED) — a provider can be PREFERRED while its
health degrades underneath it. `provider_health.ProviderHealthTracker`
holds live per-provider health (seeded ONLINE for all five
placeholders); `provider_failover.select_available()` is the one pure
function that walks an ordered candidate list and returns the first
one the tracker reports available (ONLINE or DEGRADED).

`provider_capabilities.py`'s `PROVIDER_CAPABILITIES` declares which
`Capability` each of the five placeholder providers actually supports
— derived directly from `routing_rules.ROUTING_RULES`'s existing
candidate lists, so it narrows nothing Phase 61.0 already routed.
`supports(provider_name, capability)` lets the router reject a
candidate the routing table names but the provider never declared.

### `ai/router/` — Router Safety + Metrics (TASK 4/8)

`AIRouter.route()`'s selection walk now checks, per candidate, in
order: capability-matrix support, `ProviderManager` status, and
(if a `ProviderHealthTracker` was supplied) health — still zero
hardcoded per-provider branches, every check is a lookup against a
declarative table/tracker. `health_tracker` is optional; omitting it
reproduces Phase 61.0's exact selection behavior.

`AIRouter.provider_metrics()` is a **read-only** addition: it reuses
`ai/audit/provider_stats.compute_provider_stats()` directly (no new
metrics module, per TASK 8's own instruction) over an optional
`response_log`. `route()` never calls or is influenced by this method
— no automatic optimization.

### `ai/prompts/` — Prompt Registry (TASK 5)

`prompt_registry.PromptRegistry` adds version/active/rollback
bookkeeping (`register()`, `set_active()`, `rollback()`,
`list_versions()`) for named prompts (e.g. `"market_analysis"` v1/v2/
v3). `PromptManager` itself is unmodified — this is a new sibling
module inside the same package, not a replacement.

### `ai/access/` — Tool Permission Matrix (TASK 6)

`tool_permissions.ToolPermissions` adds a second entitlement axis
(Role × Tool name, e.g. `"news_tool"`) alongside `access_control.py`'s
existing Role × Capability matrix — same package, new file, same
`AIRole` enum reused.

### `ai/context/` — Context Versioning (TASK 7)

`AIContext` gains `schema_version`/`context_version` (both default
`"1.0"`), additive with safe defaults — every Phase 61.0 caller of
`build_ai_context()` keeps working unchanged. `built_at` already
served the brief's "created_at" purpose and was not duplicated.

### `ai/cache/` — Response Cache Foundation (TASK 9, new package)

`cache_policy.CacheKey` is a five-field dataclass (Capability +
Context Version + Provider + Prompt Version + Context Hash) —
structurally forbidding a bare-prompt-text cache key, the same
"enforce the rule in the type" posture `ai/context/context_adapter.py`
already uses. `compute_context_hash()` is a deterministic SHA-256 over
a JSON-serializable payload (e.g. `AIContext.to_dict()`).
`response_cache.ResponseCache` is a TTL-bound, in-memory store
(`CachePolicy.default_ttl_seconds`, 300s default) — an expired entry
is evicted on the next `get()`. Not wired into any provider call this
phase.

## Not wired

Every module in this document is foundation only — none is imported by
`core/pipeline.py`, any live Telegram handler, or
`telegram/command_router.py`. `core/`, `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/` are unchanged.

## Tests

`tests/ai/providers/test_provider_health.py`,
`tests/ai/providers/test_provider_capabilities.py`,
`tests/ai/router/test_router_reliability.py`,
`tests/ai/test_prompt_registry.py`,
`tests/ai/access/test_tool_permissions.py`,
`tests/ai/context/test_context_versioning.py`,
`tests/ai/cache/test_response_cache.py` — covering health state
transitions, failover selection, capability-matrix gating, router
backward-compatibility (Phase 61.0 behavior unchanged when no health
tracker is supplied), read-only metrics (never influencing selection),
prompt version/rollback, tool permission matrix, additive context
versioning, and cache key/TTL/expiry behavior.

## Deferred to Phase 61.2

Per this phase's own brief: Workflow Engine, real Provider API
integration, streaming, Conversation Engine, AI Explanation Runtime,
and traffic-based provider auto-selection.
