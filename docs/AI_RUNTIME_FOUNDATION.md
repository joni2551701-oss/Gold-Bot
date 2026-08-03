# AI Runtime Foundation (Phase 61.2)

The third v0.4 AI Core phase, and the first to build a real,
end-to-end AI request lifecycle — every prior phase (61.0/61.1/61.1.1)
built foundation pieces nothing actually called together. Full
isolation audit: `docs/PHASE61_2_RUNTIME_AUDIT.md`.

**AI Runtime, not AI Trading.** `ai/runtime/ai_service.py`'s
`AIService.ask()` answers a question and returns. It never imports
`decision/`, `risk/`, `execution/`, `strategies/`, or `signals/`
(confirmed by TASK 1's AST sweep, re-confirmed at the end of this
phase with zero new violations) — how or whether an answer reaches a
trade decision is entirely outside this module's knowledge.

## The flow

```
Access -> Capability -> Router -> Provider -> ProviderResult ->
Validator -> Cache -> Audit -> Response
```

`AIService.ask(RuntimeRequest) -> RuntimeResponse`:

1. **Access** — `ai.access.access_control.AccessControl.is_allowed(role, capability)`.
2. **Capability** — `ai.capabilities.capability_manager.CapabilityManager.is_enabled(capability)`.
3. **Prompt** — explicit `RuntimeRequest.prompt`, or derived via
   `ai.prompts.prompt_manager.PromptManager.get_market_analysis_prompt()`
   from `ai_context.market_context` when no explicit prompt is given.
4. **Router** — `ai.router.router.AIRouter.route(capability)` (Phase
   61.0/61.1, untouched this phase).
5. **Cache check** — `ai.cache.cache_policy.build_cache_key_from_context()`,
   now including `user_role` (TASK 7, see below) — a hit returns
   immediately, `from_cache=True`, no provider call.
6. **Provider call** — the real `BaseAIProvider` method
   (`chat`/`analyze`/`explain`/`vision`/`image`/`voice`) for the
   selected provider. A `ProviderRuntimeError` (TASK 4) or
   `NotImplementedError` (a provider declaring a capability it hasn't
   really implemented, e.g. Gemini's `vision()` this phase) is caught,
   the failure is recorded (`ai.providers.runtime_errors.record_provider_failure()`
   updates `ProviderHealthTracker`), and the loop re-routes — the next
   `AIRouter.route()` call naturally skips the now-unhealthy provider.
   Bounded to one attempt per registered provider.
7. **Validator** — `ai.validation.response_validator.validate_response()`
   (TASK 5). A rejected response returns `accepted=False` with the
   validator's `errors` — never cached, never silently passed through.
8. **Cache write + Audit** — an accepted result is cached
   (`ai.cache.response_cache.ResponseCache.put()`) and both
   `ai.audit.request_log.RequestLog`/`ai.audit.response_log.ResponseLog`
   (TASK 8) are written on every attempt, success or failure — no API
   key in either.
9. **Response** — a `RuntimeResponse`, never a raised exception.

## Provider Preference vs Provider Health (worked example, unchanged this phase)

`ai/providers/provider_manager.py`'s owner-intent `ProviderStatus` and
`ai/providers/provider_status.py`'s observed-reality `HealthStatus`
stay the two independent axes `docs/AI_PROVIDER_FOUNDATION.md`
documented in Phase 61.1.1 — this phase is the first to actually
exercise the failure path live: in this sandbox (no `GEMINI_API_KEY`
configured), every real call to Gemini raises
`ProviderUnavailableError` immediately (no network attempt), health is
recorded `OFFLINE`, and `AIService` falls back to the next candidate
(e.g. `claude`) — confirmed by
`tests/ai/runtime/test_ai_service.py::test_real_provider_manager_default_never_crashes_without_any_api_key`.

## TASK 2 — Secrets Foundation Extension

`core/secrets.py` gained `OPENAI_API_KEY`/`CLAUDE_API_KEY`/
`GROK_API_KEY`/`LOCAL_LLM_CONFIG`, all optional (`get_optional()`,
returns `None` rather than raising) — `GEMINI_API_KEY`'s existing
raise-on-missing behavior is unchanged. `tests/security/test_secret_security.py`'s
own bulk-dump guard was updated to allow `get_optional` alongside
`get` (both take one explicit key, neither can dump every secret at
once — the property that test actually protects).

## TASK 3 — Real Gemini Provider

`ai/providers/gemini_provider.py`'s `GeminiProvider` is the first
non-placeholder `BaseAIProvider`. Real HTTP call via `requests`
(already a dependency) directly against the Gemini REST API — no new
SDK. **Rule 1**: the key is read only via `core/secrets.py`
(`Secrets.GEMINI_API_KEY`) — zero `os.getenv()` calls anywhere in
`ai/` (verified). **Rule 2**: the key travels only in the
`x-goog-api-key` request header, never the URL/query string, verified
directly by `tests/ai/providers/test_gemini_provider.py::test_api_key_travels_only_in_the_header_never_in_the_url`.
`analyze()`/`chat()`/`explain()` all route through one real call;
`vision()`/`image()`/`voice()` raise `NotImplementedError` (real
multimodal support is out of this phase's scope) — matching
`BaseAIProvider`'s own already-documented contract for a capability a
provider cannot serve. The placeholder `GeminiProvider` in
`ai/providers/placeholder_providers.py` was removed (replaced, not
duplicated) once the real one took over its registry slot.

`BaseAIProvider` gained `health_check()`/`capabilities()` as concrete
default methods (not abstract) — every existing placeholder provider
inherits them unchanged; `capabilities()` reuses
`ai.providers.provider_capabilities.capabilities_of()` directly.

## TASK 4 — Provider Runtime Error Handling

`ai/providers/runtime_errors.py`: `ProviderRuntimeError` and four
subclasses (`Timeout`/`RateLimit`/`InvalidResponse`/`Unavailable`),
`classify_provider_exception()` (never leaks a raw `requests`
exception upward), `record_provider_failure()` (maps an error to a
`HealthStatus` and calls `ProviderHealthTracker.record()`). **A real
circular import was found and fixed while building this**:
`provider_health.py` imports `provider_registry.py`, which (via
`gemini_provider.py`) would have imported `runtime_errors.py` — fixed
by making `runtime_errors.py`'s `ProviderHealthTracker` reference
`TYPE_CHECKING`-only (duck-typed at runtime), so health-tracking logic
lives here without a real import cycle.

## TASK 5 — Response Validator Foundation

`ai/validation/` (new package): `schemas.py` (`ResponseSchema` —
min content length, required metadata keys, confidence range),
`safety.py` (`check_safety()` — heuristic trade-directive-language and
leaked-API-key-pattern checks; a second, independent safety net beside
`ai/ai_prompt.py`'s existing system-prompt-level restriction),
`response_validator.py` (`validate_response()`, composing both).

## TASK 6/7/8 — AI Runtime Service Layer, Cache Integration, Audit Wiring

`ai/runtime/` (new package): `runtime_request.py`/`runtime_response.py`
(input/output shapes), `ai_service.py`'s `AIService` (the orchestrator
described above). TASK 7: `ai/cache/cache_policy.py`'s `CacheKey` grew
a seventh field, `user_role` — a lower-privileged role's cache lookup
must never return an entry a higher-privileged role's call produced
(or vice versa), a privilege-boundary concern independent of
`snapshot_id`'s freshness concern. `build_cache_key_from_context()`
now requires `user_role` explicitly.

## TASK 9 — Provider Metrics Wiring

`ai/audit/provider_stats.py` extended in place (no new module,
per the brief's own instruction) with `ProviderStats.failure_count`
(derived, not separately tracked). `AIService` is now this module's
real data source via `ResponseLog.record()`. **Observability only**:
`AIRouter.route()` has no import of `provider_stats` at all, and
`AIService.ask()` only *writes* `RequestLog`/`ResponseLog` — it never
reads `ProviderStats` back to influence selection.

## Not wired

`ai/runtime/`, `ai/validation/`, and the real `GeminiProvider` are not
called from `core/pipeline.py`, any live Telegram handler, or
`platform_layer/telegram/command_router.py` — foundation only, same posture as every
prior phase.

## Tests

`tests/ai/providers/test_gemini_provider.py` (17 tests, all network
calls faked via an injected session), `tests/ai/providers/test_runtime_errors.py`,
`tests/ai/validation/test_response_validator.py`,
`tests/ai/runtime/test_ai_service.py` (13 tests covering the full
flow: access denial, capability disabled/unmapped, missing prompt,
successful call, cache hit, validation rejection, provider failure +
fallback, health-tracker recording, every-provider-fails, and the
real, keyless `ProviderManager` default never crashing).

## Deferred to Phase 61.3 (per the Director's own brief)

AI Memory Runtime, Knowledge Base, real Tool Calling integration, AI
Assistant Layer.

## Operational layer (Phase 61.6)

This document describes the request *lifecycle* (`AIService.ask()`'s
own flow). The *operational* layer built on top of it — runtime
lifecycle state, a provider circuit breaker, runtime metrics, a
decoupled event bus, an Owner dashboard, Owner alerts, and named
configuration profiles — is documented separately in
`docs/AI_RUNTIME_OPERATIONS.md`.
