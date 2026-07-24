# Phase 61.1 — AI Provider Reliability Foundation: Reuse Audit

TASK 1 of the Phase 61.1 Worker Brief. Audits `ai/providers/`,
`ai/router/`, `ai/prompts/`, `ai/audit/`, `ai/access/` — the five
packages this phase's TASK 2-9 touch — before any code is written.
Same discipline as Phase 61.0's TASK 1
(`docs/PHASE61_AI_FOUNDATION_AUDIT.md`): Already exists / Can extend /
Cannot reuse, with a reason.

## `ai/providers/`

| Module | Status | Reason |
|---|---|---|
| `provider_manager.py` (`ProviderManager`, `ProviderStatus`: PREFERRED/FALLBACK/DISABLED) | Can extend | `ProviderStatus` is a manually-set, owner-driven state with no notion of *why* a provider is unavailable or whether it might recover. TASK 2's health states (ONLINE/DEGRADED/RATE_LIMITED/OFFLINE/DISABLED) are a distinct, orthogonal axis — a provider can be `ProviderStatus.PREFERRED` (owner's intent) while `ONLINE`/`DEGRADED`/`OFFLINE` (observed reality) varies underneath it. TASK 2 adds `provider_health.py`/`provider_status.py`/`provider_failover.py` *inside* `ai/providers/` rather than replacing `ProviderManager` — `select_provider()`'s existing Preferred/Fallback/Disabled contract is untouched; health becomes a second signal `router.py` consults (TASK 4), not a replacement for the first. |
| `provider_registry.py` (`ProviderDescriptor`, `build_provider_registry()`) | Can extend | Already the static catalog of the five placeholder providers (openai/gemini/claude/grok/local_llm). TASK 3's `provider_capabilities.py` reads these same five names as its keys rather than inventing a new provider list — no second registry of provider identities. |
| `base_provider.py` (`BaseAIProvider`, `ProviderResult`) | Already exists, unmodified | Defines the six capability-shaped methods (`analyze`/`chat`/`explain`/`vision`/`image`/`voice`). TASK 3's capability matrix is *declarative data* about which of these six a given provider is meant to answer for — it does not change the interface itself; every placeholder provider still implements all six methods (Phase 61.0's stub posture), the matrix just tells the router which of those implementations are meaningful to route to. |
| `placeholder_providers.py` (5 stub classes) | Already exists, unmodified | No real API behavior to reflect health/capability against yet — TASK 2/3 build declarative foundation only, no placeholder provider method changes. |

## `ai/router/`

| Module | Status | Reason |
|---|---|---|
| `router.py` (`AIRouter.route()`) | Can extend | Already composes `routing_rules.py` + `ProviderManager.status_of()` + optionally `CapabilityManager`. TASK 4 adds two more checks to the same `route()` method's existing walk-the-candidates loop — capability-matrix support (TASK 3) and health status (TASK 2) — rather than a second router class. "Hardcode YO'Q" is already this module's own founding constraint (Phase 61.0 TASK 4's docstring); TASK 4 keeps it. |
| `routing_rules.py` (`ROUTING_RULES` dict) | Already exists, unmodified | Still the ordered-candidate-list data table. TASK 4 does not change its shape — it changes what `router.py` checks *after* reading a candidate name from this table. |
| `routing_result.py` (`RoutingResult`) | Can extend | TASK 8 (metrics visibility) may want `RoutingResult.reason` to be able to name a health/capability rejection specifically (e.g. "excluded: DEGRADED" vs "excluded: capability not supported") — additive detail in the existing `reason` string field, not a new dataclass field required. |

## `ai/prompts/`

| Module | Status | Reason |
|---|---|---|
| `prompt_manager.py` (`PromptManager`, static template methods) | Can extend | Phase 61.0's own TASK 1 audit already flagged this as "Can extend (future phase)" for exactly this reason. TASK 5 adds registry/versioning *around* `PromptManager` (a new module inside `ai/prompts/`, e.g. `prompt_registry.py`) — `PromptManager`'s existing methods (`get_market_analysis_prompt()`, etc.) are not renamed, removed, or replaced. The brief's own instruction ("PromptManager almashtirilmaydi. Faqat extend.") matches what TASK 1 already found the right shape to be. |

## `ai/audit/`

| Module | Status | Reason |
|---|---|---|
| `provider_stats.py` (`ProviderStats`, `compute_provider_stats()`) | Reused as-is, not modified | TASK 8's brief is explicit: no new metrics module, reuse this one. `compute_provider_stats()` already aggregates success rate, avg latency, tokens, and cost per provider from an already-recorded `ResponseLog` history — exactly the "Success Rate / Latency / Failures" TASK 8 asks the router to read. TASK 8's only change is a caller: `router.py` (or a thin adapter it owns) calls `compute_provider_stats()` and exposes the result for inspection — it does not feed back into `route()`'s selection logic this phase ("Hech qanday avtomatik optimizatsiya qilmaydi. Faqat o'qiydi."). |
| `request_log.py` / `response_log.py` | Already exists, unmodified | The data `provider_stats.py` aggregates. No change needed for read-only consultation. |

## `ai/access/`

| Module | Status | Reason |
|---|---|---|
| `access_control.py` (`AccessControl`, Role × Capability matrix) | Can extend | TASK 6's Role × Tool matrix is a second, independent dimension over the same `AIRole` enum — not a replacement for the Capability matrix. Extending `access_control.py` with a second matrix (or a sibling method on the same class) keeps both permission concerns in one place rather than splitting `ai/access/` into two disconnected authorities. A new `tool_permissions.py` module inside `ai/access/` (same package, new file) is the chosen shape — matches this same package's existing internal split (`permissions.py` for the enum, `access_control.py` for capability entitlement, `usage_limits.py` for rate ceilings): one more file for one more entitlement axis, not a new top-level package. |
| `permissions.py` (`AIRole`) | Already exists, reused directly | TASK 6's Tool matrix is keyed by the same `AIRole` values — no new role vocabulary needed. |
| `usage_limits.py` (`UsageLimiter`) | Already exists, unmodified | Out of scope for this phase's tool-permission work (a yes/no entitlement question, not a rate ceiling). |

## New packages this phase

- **`ai/cache/`** (TASK 9) — genuinely new. No existing module caches an AI response; `ai/memory/context_memory.py` (Phase 55) and `ai/session/` (Phase 61.0) are both per-user conversational state, not a shared response cache keyed on (capability, context version, provider, prompt version, context hash). Confirmed no collision with `data/`'s `SmartDataCache` (a market-data cache, different domain entirely, never imported by `ai/`).

## Summary

Seven of Phase 61.1's ten tasks extend an existing module in place
(`ai/providers/`, `ai/router/`, `ai/prompts/`, `ai/access/`,
`ai/context/`); one task is explicitly reuse-only with no new module
(`ai/audit/`, TASK 8); one task is a genuinely new package
(`ai/cache/`, TASK 9, justified above); TASK 10 is documentation/tests.
No existing module's current public contract changes in a
backward-incompatible way — `ProviderManager.select_provider()`,
`AIRouter.route()`'s signature, `PromptManager`'s existing methods,
and `AccessControl.is_allowed()` all keep their Phase 61.0 shape.
