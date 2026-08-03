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

### Provider Preference vs Provider Health (Phase 61.1.1 TASK 4 correction)

Two independent concepts, easy to conflate, so stated explicitly here:

- **`ProviderStatus`** (`provider_manager.py`) = **owner intent** —
  PREFERRED/FALLBACK/DISABLED, set only by an explicit `set_status()`
  call. Nothing in this codebase changes it automatically.
- **`ProviderHealth`** (`provider_status.py`/`provider_health.py`) =
  **observed runtime reality** — ONLINE/DEGRADED/RATE_LIMITED/OFFLINE/
  DISABLED, set only by an explicit `record()`/`mark_recovered()` call
  (no real health check exists yet — that is future, out-of-scope
  work).

Worked example, the exact sequence a real outage/recovery would
produce:

```
gemini: ProviderStatus.PREFERRED, HealthStatus.ONLINE
  -> gemini goes down; caller records HealthStatus.OFFLINE
gemini: ProviderStatus.PREFERRED (unchanged), HealthStatus.OFFLINE
  -> router.route() skips gemini (unhealthy), selects openai instead
  -> caller later calls tracker.mark_recovered("gemini")
gemini: ProviderStatus.PREFERRED (still unchanged), HealthStatus.ONLINE
  -> router.route() selects gemini again -- automatically, because
     ProviderStatus was never touched during the outage
```

**No demotion happens.** `ProviderStatus` is never automatically
changed by a health observation, in either direction — an owner's
PREFERRED/FALLBACK/DISABLED configuration survives an outage exactly
as it was set. This is why recovery-to-PREFERRED looks automatic: it
is automatic only in the sense that nothing ever took PREFERRED away.
If a real outage-response policy ever needs actual demotion (e.g.
auto-DISABLE after N consecutive OFFLINE observations), that is new
behavior for a future phase to add explicitly, not something either
class does today.

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

### `ai/prompts/` — Prompt Registry + Lifecycle (TASK 5; lifecycle added Phase 61.1.1 TASK 3)

`prompt_registry.PromptRegistry` adds version/active/rollback
bookkeeping (`register()`, `set_active()`, `rollback()`,
`list_versions()`) for named prompts (e.g. `"market_analysis"` v1/v2/
v3). `PromptManager` itself is unmodified — this is a new sibling
module inside the same package, not a replacement.

Phase 61.1.1 adds `PromptLifecycleState` (ACTIVE/DEPRECATED/ARCHIVED)
on `PromptVersionRecord`, defaulting to ACTIVE at registration.
`deprecate()`/`archive()` change a version's state without touching
which version is currently active. `set_active()` and `rollback()`
both refuse to select a DEPRECATED or ARCHIVED version — it stays
visible in `list_versions()` (history is never deleted) but can never
again become the active one through either path.

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

### `ai/cache/` — Response Cache Foundation (TASK 9; freshness corrected Phase 61.1.1 TASK 2)

`cache_policy.CacheKey` is a six-field dataclass (Capability + Context
Version + Provider + Prompt Version + Context Hash + **Snapshot ID**)
— structurally forbidding a bare-prompt-text cache key, the same
"enforce the rule in the type" posture `ai/context/context_adapter.py`
already uses.

**Freshness chain: Snapshot identity -> Cache freshness -> TTL.**
`snapshot_id` is produced exclusively by
`ai_layer.ai_engine.context.context_builder.build_ai_context()` — never by a caller,
never via `datetime.now()`/`uuid.uuid4()` at cache-key-construction
time. It is a deterministic SHA-256 (via `compute_context_hash()`)
over the built `AIContext`'s own content with `built_at` excluded:
identical inputs always produce the identical `snapshot_id` (a
legitimate cache hit is possible), different inputs always produce a
different one (a stale answer can never be served for genuinely
different content). `build_cache_key_from_context(ai_context, ...)`
is the blessed way to build a `CacheKey` — it pulls `snapshot_id`
straight off an already-built `AIContext` and raises `ValueError` if
that `AIContext` was never built through `build_ai_context()` (i.e.
`snapshot_id` is `None`), rather than silently falling back to a
caller-invented value.

`CachePolicy.default_ttl_seconds` (300s default) is the second,
independent layer: even a snapshot whose content hasn't changed (a
quiet market between provider polls) stops being served from cache
once the TTL elapses — content-identity alone never grants permanent
freshness. `response_cache.ResponseCache` evicts an expired entry on
the next `get()`. Not wired into any provider call this phase.

## Not wired

Every module in this document is foundation only — none is imported by
`core/pipeline.py`, any live Telegram handler, or
`platform_layer/telegram/command_router.py`. `core/`, `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/` are unchanged.

## Tests

`tests/ai/providers/test_ai_provider_health.py`,
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
versioning, and cache key/TTL/expiry behavior. Phase 61.1.1 adds
snapshot-identity cache hit/miss tests and prompt-lifecycle selection
tests — see `docs/PHASE61_1_1_FOUNDATION_CORRECTIONS.md`.

## Deferred to Phase 61.2

Per this phase's own brief: Workflow Engine, real Provider API
integration, streaming, Conversation Engine, AI Explanation Runtime,
and traffic-based provider auto-selection.
