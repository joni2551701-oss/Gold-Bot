"""
AI Layer — AI Runtime Service (Phase 61.2: AI Runtime Foundation,
TASK 6/7/8/9).

The first real orchestration in this entire AI Core arc — every prior
phase (61.0/61.1/61.1.1) built foundation pieces nothing actually
called end-to-end. `AIService.ask()` is that end-to-end call:

    Access -> Capability -> Router -> Provider -> ProviderResult ->
    Validator -> Cache -> Audit -> Response

Composes existing foundation types only -- reimplements none of them:
`ai.access.access_control.AccessControl`, `ai.capabilities.capability_manager.CapabilityManager`,
`ai.router.router.AIRouter`, `ai.providers.provider_manager.ProviderManager`,
`ai.providers.provider_health.ProviderHealthTracker`,
`ai.providers.runtime_errors` (TASK 4), `ai.validation.response_validator`
(TASK 5), `ai.cache.cache_policy`/`ai.cache.response_cache` (TASK 7),
`ai.audit.request_log`/`ai.audit.response_log` (TASK 8),
`ai.prompts.prompt_manager.PromptManager`.

**AI Isolation (Rule 4, TASK 1 of this same phase's brief)**: this
module imports nothing from `decision/`, `risk/`, `execution/`,
`strategies/`, or `signals/`. It answers a question and returns --
whether/how that answer reaches a trade decision is entirely outside
this module's own knowledge or responsibility, exactly as
`ai/interfaces.py`'s `AIAnalyzerInterface` has always required.

Retry/fallback (TASK 4's own flow: "Provider Error -> ProviderHealthTracker
-> Router fallback"): on a `ProviderRuntimeError` or `NotImplementedError`
from a provider call, this method records the failure (health, for a
real error) and re-routes -- `AIRouter.route()` naturally skips a
provider `ProviderHealthTracker` now reports unavailable. Bounded to
one attempt per registered provider so a request can never loop
forever.

Cache key correction (Phase 61.3: AI Intelligence Layer, TASK 5): the
cache key's `context_hash` is now the resolved prompt's own SHA-256,
passed via `build_cache_key_from_context()`'s existing (Phase 61.1.1)
`context_hash` override parameter -- not a new parameter, not a new
`CacheKey` field. Necessary once `ai/conversation/conversation_engine.py`
became the first real caller supplying distinct explicit `request.prompt`
values (different user chat messages) against the *same* `AIContext`:
`context_hash` previously defaulted to `ai_context.snapshot_id` alone,
so two different questions about the same market snapshot would have
collided on one cache entry and returned the first question's answer
to the second question. Hashing the resolved prompt instead still
produces an identical key across two calls with identical resolved
prompts (the market-analysis-template path, where `PromptManager`
templates are a pure deterministic function of `MarketContext` -- no
timestamp interpolation), so every pre-existing cache-hit test keeps
passing; it additionally now distinguishes any two calls whose
resolved prompt text actually differs, which `ai_context.snapshot_id`
alone could never do.

Event publication (Phase 61.6: AI Operations & Reliability Foundation,
TASK 5): `event_bus` is an optional, injectable dependency (defaults
to a fresh, throwaway `EventBus` when omitted -- same convention every
other constructor argument here already uses). `ask()`'s own control
flow is unchanged; it only gains `event_bus.publish(...)` calls at
four points that already existed (cache hit, cache miss, a provider
failure/`NotImplementedError`, a validation rejection) plus one new
observation (the router selecting a different provider than the
previous attempt within the same call, i.e. a failover). No new
orchestration logic, no change to what `ask()` returns or when it
returns it -- publishing is fire-and-forget and `EventBus.publish()`
itself never raises.

Platform Stabilization & Integration (Phase 61.7): every foundation
piece Phase 61.6 built real-but-standalone now actually drives this
method. Full detail: `docs/PHASE61_7_INTEGRATION_AUDIT.md`,
`docs/AI_PLATFORM_STABILIZATION.md`.

Production Wiring (Phase 62.2): three real gaps found by re-auditing
this already-integrated flow against `docs/PHASE62_2_RUNTIME_AUDIT.md`'s
own TASK 0/1 (the flow itself needed no rebuild -- Phase 61.7 already
built it). (1) The runtime-unhealthy rejection (`is_healthy()` gate)
now writes a `request_log`/`response_log` entry (`status=
"RUNTIME_UNAVAILABLE"`) -- previously the one `_execute()` rejection
path with zero audit trail. (2) A retry attempt (`is_retry`) now waits
`2 ** (len(attempted) - 2)` seconds via the injectable `sleep_fn`
(defaults to `time.sleep`) before the next attempt -- the same
exponential-backoff formula `data/twelve_data_client.py` already uses,
reused rather than reinvented; tests inject a no-op `sleep_fn` so the
suite never blocks. (3) `PROVIDER_FAILED`'s payload now carries a
structured `error_type` (`TIMEOUT`/`RATE_LIMIT`/`INVALID_RESPONSE`/
`UNAVAILABLE`) -- see `event_bus.py`'s own docstring for why this is
not a new event type. (4) AI Cost Protection (TASK 8):
`daily_cost_limit`/`daily_token_limit` (both optional, default `None`
= disabled) gate a check run after every successful response -- see
`_check_cost_protection()`'s own docstring for the full design,
including its one honest limitation (every real `response_log` entry
currently logs `cost=0.0, tokens=0`, so this only actually trips today
against injected test data, not live traffic, exactly like
`ai_cost_handler()`'s own "$0.00").

- **`runtime_manager`** (TASK 2, optional, defaults to a fresh
  `RuntimeManager(event_bus=self._event_bus)`): `ask()`'s very first
  check is `runtime_manager.is_healthy()` -- the Director's own
  "Runtime READY?" gate, implemented as the existing, already-tested
  `is_healthy()` (READY/BUSY/DEGRADED serve; FAILED/SHUTDOWN/
  INITIALIZING reject) rather than a stricter literal `== READY`
  equality, which would contradict that method's own Phase 61.6
  contract. A rejection here returns an unaccepted `RuntimeResponse`
  exactly like every other rejection path -- never raises.
- **`circuit_breaker`** (TASK 3, optional, defaults to a fresh
  `ProviderCircuitBreaker(health_tracker=self._health_tracker,
  event_bus=self._event_bus)` -- same tracker instance, so a breaker
  transition is immediately visible to `self._router`, which is never
  itself modified): `_sync_circuit_breakers()` ticks `allow_request()`
  for every registered provider once per `ask()` call, before routing
  -- the only code path that ever moves a tripped breaker
  `OPEN -> HALF_OPEN` once its recovery timeout elapses, so a provider
  `AIRouter.route()` would otherwise never re-offer stays reachable.
  A second `allow_request()` gate sits right before the real provider
  call (after the cache-hit check -- a cache hit never touches the
  live provider, so circuit state must never block it). A successful,
  validated response calls `record_success()`; a `ProviderRuntimeError`
  always calls `record_failure()`. The pre-existing (Phase 61.2)
  `record_provider_failure()` call now fires **only** for
  `ProviderRateLimitError`/`ProviderInvalidResponseError` (their own
  distinct `RATE_LIMITED`/`DEGRADED` statuses, which the breaker's
  three-state model doesn't capture) -- **not** for
  `ProviderTimeoutError`/`ProviderUnavailableError`, both of which
  already map to `HealthStatus.OFFLINE`, exactly what the breaker
  itself writes once it actually trips. Writing that status on the
  very first timeout, as the pre-Phase-61.7 code did, would mark the
  provider `OFFLINE` immediately and make it invisible to
  `AIRouter.route()` before the breaker could ever accumulate a second
  failure -- its 5-strikes threshold could never be reached through
  real, repeated attempts, contradicting this phase's own worked
  example ("Gemini times out 5 times -> circuit opens"). This is an
  intentional behavior change from Phase 61.2 -- a single timeout no
  longer immediately marks a provider `OFFLINE`; five consecutive
  ones do, via the breaker.
- **`runtime_profile`** (TASK 4, optional, `None` by default -- `None`
  means every behavior below is byte-for-byte identical to Phase 61.6):
  when supplied, `validate_response(result, schema=runtime_profile.validation_schema)`
  (that function's own pre-existing optional parameter, unchanged),
  the constructor builds `ResponseCache(policy=runtime_profile.to_cache_policy())`
  when no explicit `response_cache` was injected, and the per-request
  attempt budget becomes `min(max_attempts, runtime_profile.max_retries)`.
  `timeout_seconds` is intentionally **not** wired -- no real provider
  exposes an injectable per-call timeout yet (see the integration
  audit doc for why that is out of this task's scope).
- **`REQUEST_STARTED`/`REQUEST_COMPLETED`** (TASK 5): `ask()` is now a
  thin wrapper around the method that holds this entire flow
  (`_execute()`) -- it publishes `REQUEST_STARTED` before calling
  `_execute()` and `REQUEST_COMPLETED` (with the resulting
  `accepted`/`provider_name`/`reason`) after, bracketing every
  rejection and success path in exactly two publish calls rather than
  one at every individual `return` site.
"""

import hashlib
import time
from typing import Callable, Dict, Optional

from ai.access.access_control import AccessControl
from ai.audit.provider_stats import compute_daily_usage, evaluate_cost_protection
from ai.audit.request_log import RequestLog
from ai.audit.response_log import ResponseLog
from ai.cache.cache_policy import build_cache_key_from_context
from ai.cache.response_cache import ResponseCache
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.prompts.prompt_manager import PromptManager
from ai.providers.circuit_breaker import ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.providers.runtime_errors import (
    ProviderInvalidResponseError,
    ProviderRateLimitError,
    ProviderRuntimeError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    record_provider_failure,
)
from ai.router.router import AIRouter
from ai.runtime.event_bus import EventBus, EventType, RuntimeEvent
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_state import RuntimeState
from ai.runtime.runtime_profiles import RuntimeProfile
from ai.runtime.runtime_request import RuntimeRequest
from ai.runtime.runtime_response import RuntimeResponse
from ai.validation.response_validator import validate_response
from core.logger import setup_logger

logger = setup_logger("AIService")

_PROMPT_VERSION = "v1"

# Capability -> BaseAIProvider method name. Only the six capabilities
# with a real BaseAIProvider method (Phase 61.0) are dispatchable;
# SUMMARY/MEMORY/EDUCATION/TOOL_CALLING/VIDEO/DOCUMENT have no
# corresponding provider method yet (a pre-existing gap, not
# introduced this phase) -- ask() reports a clean rejection for those
# rather than guessing a mapping.
_CAPABILITY_METHOD: Dict[Capability, str] = {
    Capability.CHAT: "chat",
    Capability.ANALYSIS: "analyze",
    Capability.EXPLANATION: "explain",
    Capability.VISION: "vision",
    Capability.IMAGE: "image",
    Capability.VOICE: "voice",
}

# Phase 62.2 TASK 6: PROVIDER_FAILED's payload now carries a structured
# error_type label -- the Director's own "PROVIDER_TIMEOUT" resolved
# the same way ai/providers/circuit_breaker.py already resolved
# "ProviderDown" (see that module's docstring): reuse the existing
# EventType, add a distinguishing payload key, not a fourth near-
# duplicate "provider went wrong" event type.
_ERROR_TYPE_LABEL: Dict[type, str] = {
    ProviderTimeoutError: "TIMEOUT",
    ProviderRateLimitError: "RATE_LIMIT",
    ProviderInvalidResponseError: "INVALID_RESPONSE",
    ProviderUnavailableError: "UNAVAILABLE",
}


class _AttemptScopedHealthTracker:
    """
    A read-only view over the one real, shared `ProviderHealthTracker`
    that additionally treats provider names already attempted *this*
    `ask()` call as unavailable. Introduces no new provider-state store
    (Rule 4): `attempted` is a plain local `set`, already scoped to a
    single `ask()` call, never persisted or written anywhere; this
    class is never itself written to -- every real health transition
    still goes through the one real, shared tracker only, unchanged.

    Needed because `AIRouter.route()` always returns the single
    best-ranked candidate for a capability, with no "exclude these
    names" parameter, and (Phase 61.7 TASK 3) a provider that fails
    once no longer immediately becomes tracker-`OFFLINE` -- the
    circuit breaker's 5-strikes threshold now owns that. Without this
    view, a provider that just failed within this call would keep
    being re-offered as "best" for every remaining attempt, so
    failover to a different, healthy candidate could never happen
    inside one request.
    """

    def __init__(self, health_tracker: ProviderHealthTracker, attempted: set) -> None:
        self._health_tracker = health_tracker
        self._attempted = attempted

    def is_available(self, provider_name: str) -> bool:
        return provider_name not in self._attempted and self._health_tracker.is_available(provider_name)


class AIService:
    """Every dependency is injectable (same convention as every other Phase 61.x foundation class) -- a caller/test never needs the real Gemini network path to exercise this orchestration."""

    def __init__(
        self,
        capability_manager: Optional[CapabilityManager] = None,
        access_control: Optional[AccessControl] = None,
        provider_manager: Optional[ProviderManager] = None,
        health_tracker: Optional[ProviderHealthTracker] = None,
        router: Optional[AIRouter] = None,
        response_cache: Optional[ResponseCache] = None,
        request_log: Optional[RequestLog] = None,
        response_log: Optional[ResponseLog] = None,
        prompt_manager: Optional[PromptManager] = None,
        event_bus: Optional[EventBus] = None,
        runtime_manager: Optional[RuntimeManager] = None,
        circuit_breaker: Optional[ProviderCircuitBreaker] = None,
        runtime_profile: Optional[RuntimeProfile] = None,
        sleep_fn: Optional[Callable[[float], None]] = None,
        daily_cost_limit: Optional[float] = None,
        daily_token_limit: Optional[int] = None,
    ) -> None:
        self._capability_manager = capability_manager or CapabilityManager()
        self._access_control = access_control or AccessControl()
        self._provider_manager = provider_manager or ProviderManager()
        self._health_tracker = health_tracker or ProviderHealthTracker()
        self._router = router or AIRouter(
            self._provider_manager, capability_manager=self._capability_manager, health_tracker=self._health_tracker,
        )
        self._runtime_profile = runtime_profile
        if response_cache is not None:
            self._response_cache = response_cache
        elif runtime_profile is not None:
            self._response_cache = ResponseCache(policy=runtime_profile.to_cache_policy())
        else:
            self._response_cache = ResponseCache()
        self._request_log = request_log or RequestLog()
        self._response_log = response_log or ResponseLog()
        self._prompt_manager = prompt_manager or PromptManager()
        self._event_bus = event_bus or EventBus()
        self._runtime_manager = runtime_manager or RuntimeManager(event_bus=self._event_bus)
        self._circuit_breaker = circuit_breaker or ProviderCircuitBreaker(
            health_tracker=self._health_tracker, event_bus=self._event_bus,
        )
        self._sleep_fn = sleep_fn or time.sleep
        self._daily_cost_limit = daily_cost_limit
        self._daily_token_limit = daily_token_limit

    def _check_cost_protection(self) -> None:
        """
        Phase 62.2 TASK 8. No-op when neither `daily_cost_limit` nor
        `daily_token_limit` was configured (both default `None`) --
        same "off unless a caller explicitly asks" posture every other
        optional knob in this class already uses. When configured,
        compares `compute_daily_usage(self._response_log.all())`
        against the limit(s); a breach transitions the runtime to
        `RuntimeState.DEGRADED` (never FAILED -- a cost breach means
        "slow down," not "stop entirely") with a reason string prefixed
        `"cost protection: "` so `telegram/owner/runtime_notifications.py`'s
        `RuntimeNotifier` can distinguish this cause from any other
        `DEGRADED` transition without a new EventType (Rule 5).
        A runtime already DEGRADED/FAILED/SHUTDOWN is left alone --
        `RuntimeManager.transition()` itself would reject a redundant
        or invalid transition anyway, this just avoids the noise of
        calling it every single successful request once already tripped.

        Honest limitation: every `response_log.record()` call in this
        class today logs `tokens=0, cost=0.0` (no real provider reports
        usage back via `ProviderResult.metadata` yet -- the same gap
        `telegram/owner/ai_commands.py`'s `ai_cost_handler()` already
        documents with its own honest "$0.00"). This check is real,
        wired, and provably correct against injected data with nonzero
        cost/tokens (see `tests/ai/runtime/test_ai_service_integration.py`);
        it will not actually trip from live traffic until a future,
        separately-scoped phase makes a real provider report token/cost
        usage.
        """
        if self._daily_cost_limit is None and self._daily_token_limit is None:
            return
        if not self._runtime_manager.is_healthy():
            return

        usage = compute_daily_usage(self._response_log.all())
        breach_reason = evaluate_cost_protection(usage, self._daily_cost_limit, self._daily_token_limit)
        if breach_reason is not None:
            self._runtime_manager.transition(RuntimeState.DEGRADED, reason=f"cost protection: {breach_reason}")

    def _sync_circuit_breakers(self) -> None:
        """Ticks allow_request() for every registered provider -- the only code path that ever moves a tripped breaker OPEN -> HALF_OPEN once its recovery timeout elapses. Without this, AIRouter.route() would never re-offer a still-OFFLINE-per-tracker provider as a candidate, so ask() would never get a chance to call allow_request() on it again -- a permanent deadlock this tick breaks. Idempotent and side-effect-free for CLOSED/HALF_OPEN providers."""
        for provider_name in self._provider_manager.list_providers():
            self._circuit_breaker.allow_request(provider_name)

    def _route(self, capability: Capability, attempted: set):
        """
        Delegates to `self._router.route()` unmodified for the first
        attempt (`attempted` empty -- identical to every prior phase's
        behavior). For a retry (TASK 3's own fix -- see
        `_AttemptScopedHealthTracker`'s docstring for why this is
        needed), routes through a freshly-constructed `AIRouter` built
        from this service's own `provider_manager`/`capability_manager`
        (the exact same objects the default router already uses) and
        an attempt-scoped tracker view -- `AIRouter.route()`'s own
        selection logic (capability-matrix support, provider status,
        health) is completely unmodified; only which names count as
        "healthy" for this one retry differs.
        """
        if not attempted:
            return self._router.route(capability)
        scoped_tracker = _AttemptScopedHealthTracker(self._health_tracker, attempted)
        scoped_router = AIRouter(
            self._provider_manager, capability_manager=self._capability_manager, health_tracker=scoped_tracker,
        )
        return scoped_router.route(capability)

    def _resolve_prompt(self, request: RuntimeRequest) -> Optional[str]:
        """Reuses PromptManager.get_market_analysis_prompt() when a market context is available -- never builds prompt text itself. Returns None (never raises) when neither an explicit prompt nor a market context was supplied."""
        if request.prompt is not None:
            return request.prompt
        if request.ai_context.market_context is not None:
            return self._prompt_manager.get_market_analysis_prompt(request.ai_context.market_context)
        return None

    def ask(self, request: RuntimeRequest) -> RuntimeResponse:
        """Publishes REQUEST_STARTED/REQUEST_COMPLETED bracketing _execute() -- never raises itself, since _execute() itself never raises."""
        self._event_bus.publish(RuntimeEvent(
            event_type=EventType.REQUEST_STARTED,
            payload={"capability": request.capability.value, "role": request.role.value},
        ))
        response = self._execute(request)
        self._event_bus.publish(RuntimeEvent(
            event_type=EventType.REQUEST_COMPLETED,
            payload={
                "capability": request.capability.value, "accepted": response.accepted,
                "provider_name": response.provider_name, "reason": response.reason,
            },
        ))
        if not response.accepted:
            self._event_bus.publish(RuntimeEvent(
                event_type=EventType.REQUEST_FAILED,
                payload={"capability": request.capability.value, "reason": response.reason},
            ))
        return response

    def _execute(self, request: RuntimeRequest) -> RuntimeResponse:
        """Never raises: every rejection path (runtime/access/capability/prompt/provider/validation) returns an unaccepted RuntimeResponse instead."""
        if not self._runtime_manager.is_healthy():
            reason = f"runtime unavailable: state={self._runtime_manager.current_state().value}"
            # Phase 62.2 TASK 3: the one _execute() rejection path with no
            # audit trail before this phase -- every other rejection/
            # success path already calls request_log/response_log.record().
            request_record = self._request_log.record(request.capability, None, telegram_id=request.telegram_id)
            self._response_log.record(
                request_id=request_record.request_id, capability=request.capability, provider_name=None,
                latency_ms=0.0, tokens=0, cost=0.0, status="RUNTIME_UNAVAILABLE",
            )
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason=reason, request_id=request_record.request_id,
            )

        if not self._access_control.is_allowed(request.role, request.capability):
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason=f"access denied for role {request.role.value} on capability {request.capability.value}",
            )

        if not self._capability_manager.is_enabled(request.capability):
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason=f"capability {request.capability.value} is disabled",
            )

        method_name = _CAPABILITY_METHOD.get(request.capability)
        if method_name is None:
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason=f"capability {request.capability.value} has no runtime method mapping yet",
            )

        prompt = self._resolve_prompt(request)
        if prompt is None:
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason="no prompt available -- request.prompt was None and ai_context.market_context is None",
            )

        self._sync_circuit_breakers()

        attempted = set()
        previous_provider_name: Optional[str] = None
        max_attempts = max(len(self._provider_manager.list_providers()), 1)
        if self._runtime_profile is not None:
            max_attempts = min(max_attempts, self._runtime_profile.max_retries)

        for _ in range(max_attempts):
            routing_result = self._route(request.capability, attempted)
            provider_name = routing_result.provider_name
            if provider_name is None:
                return RuntimeResponse(accepted=False, content=None, provider_name=None, reason=routing_result.reason)
            if provider_name in attempted:
                break
            attempted.add(provider_name)
            is_retry = len(attempted) > 1
            if is_retry:
                # Phase 62.2 TASK 5: exponential backoff before a retry
                # attempt, same 2 ** attempt formula data/twelve_data_client.py's
                # fetch_candles() already uses for the identical "wait
                # before trying again" purpose (Reuse Principle: reuse the
                # existing formula). len(attempted) - 2 is 0 for the first
                # retry (second overall attempt), 1 for the second retry,
                # etc. sleep_fn is injectable so tests never actually block.
                self._sleep_fn(2 ** (len(attempted) - 2))
                self._event_bus.publish(RuntimeEvent(
                    event_type=EventType.RETRY_STARTED,
                    payload={"attempt_number": len(attempted), "provider_name": provider_name},
                ))

            if previous_provider_name is not None and provider_name != previous_provider_name:
                self._event_bus.publish(RuntimeEvent(
                    event_type=EventType.PROVIDER_CHANGED,
                    payload={"from": previous_provider_name, "to": provider_name},
                ))
            previous_provider_name = provider_name

            cache_key = build_cache_key_from_context(
                request.ai_context, request.capability, provider_name, _PROMPT_VERSION, request.role.value,
                context_hash=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            )
            cached_entry = self._response_cache.get(cache_key)
            if cached_entry is not None:
                self._event_bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT, payload={"provider_name": provider_name}))
                return RuntimeResponse(
                    accepted=True, content=cached_entry.content, provider_name=provider_name,
                    reason="cache hit", from_cache=True, metadata=dict(cached_entry.metadata),
                )
            self._event_bus.publish(RuntimeEvent(event_type=EventType.CACHE_MISS, payload={"provider_name": provider_name}))

            if not self._circuit_breaker.allow_request(provider_name):
                logger.info(f"Provider {provider_name} circuit is OPEN -- skipping, trying next provider")
                continue

            provider = self._provider_manager.get_provider(provider_name)
            if provider is None:
                continue

            request_record = self._request_log.record(request.capability, provider_name, telegram_id=request.telegram_id)
            started_at = time.monotonic()

            try:
                result = getattr(provider, method_name)(prompt)
            except NotImplementedError:
                self._response_log.record(
                    request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                    latency_ms=(time.monotonic() - started_at) * 1000, tokens=0, cost=0.0, status="NOT_IMPLEMENTED",
                )
                if is_retry:
                    self._event_bus.publish(RuntimeEvent(
                        event_type=EventType.RETRY_COMPLETED,
                        payload={"attempt_number": len(attempted), "provider_name": provider_name, "success": False},
                    ))
                logger.info(f"Provider {provider_name} does not implement {method_name}() -- trying next provider")
                continue
            except ProviderRuntimeError as e:
                if not isinstance(e, (ProviderTimeoutError, ProviderUnavailableError)):
                    # Timeout/Unavailable both already map to HealthStatus.OFFLINE (runtime_errors.py's
                    # own _ERROR_HEALTH_STATUS) -- exactly the status the circuit breaker itself writes
                    # once it actually trips. Writing it here too, on the very first failure, would mark
                    # the provider OFFLINE immediately and make it invisible to AIRouter.route() before
                    # the breaker could ever accumulate a second failure -- its 5-strikes threshold could
                    # never be reached through real, repeated attempts. RateLimit/InvalidResponse convey
                    # a genuinely different signal (RATE_LIMITED/DEGRADED) the breaker's own three-state
                    # model doesn't capture, so those still get an immediate, precise write.
                    record_provider_failure(self._health_tracker, e)
                self._circuit_breaker.record_failure(provider_name)
                self._response_log.record(
                    request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                    latency_ms=(time.monotonic() - started_at) * 1000, tokens=0, cost=0.0, status="FAILED",
                )
                self._event_bus.publish(RuntimeEvent(
                    event_type=EventType.PROVIDER_FAILED,
                    payload={
                        "provider_name": provider_name, "reason": e.reason,
                        "error_type": _ERROR_TYPE_LABEL.get(type(e), "UNKNOWN"),
                    },
                ))
                if is_retry:
                    self._event_bus.publish(RuntimeEvent(
                        event_type=EventType.RETRY_COMPLETED,
                        payload={"attempt_number": len(attempted), "provider_name": provider_name, "success": False},
                    ))
                logger.warning(f"Provider {provider_name} failed: {e.reason} -- trying next provider")
                continue

            latency_ms = (time.monotonic() - started_at) * 1000
            validation_schema = self._runtime_profile.validation_schema if self._runtime_profile is not None else None
            validation = validate_response(result, schema=validation_schema)

            if not validation.accepted:
                self._response_log.record(
                    request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                    latency_ms=latency_ms, tokens=0, cost=0.0, status="REJECTED",
                )
                self._event_bus.publish(RuntimeEvent(event_type=EventType.VALIDATION_FAILED, payload={"provider_name": provider_name, "errors": validation.errors}))
                if is_retry:
                    self._event_bus.publish(RuntimeEvent(
                        event_type=EventType.RETRY_COMPLETED,
                        payload={"attempt_number": len(attempted), "provider_name": provider_name, "success": False},
                    ))
                return RuntimeResponse(
                    accepted=False, content=None, provider_name=provider_name,
                    reason="response failed validation", errors=validation.errors,
                    request_id=request_record.request_id,
                )

            # Provider -> Circuit Breaker -> Provider call -> Validation are all above; from here: Cache -> Audit -> Cost Protection -> (Events published by ask()'s own wrapper) -> Response.
            self._response_cache.put(cache_key, result.content, metadata=result.metadata)
            self._response_log.record(
                request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                latency_ms=latency_ms, tokens=0, cost=0.0, status="SUCCESS",
            )
            self._circuit_breaker.record_success(provider_name)
            self._check_cost_protection()
            if is_retry:
                self._event_bus.publish(RuntimeEvent(
                    event_type=EventType.RETRY_COMPLETED,
                    payload={"attempt_number": len(attempted), "provider_name": provider_name, "success": True},
                ))

            return RuntimeResponse(
                accepted=True, content=result.content, provider_name=provider_name,
                reason="provider call succeeded", metadata=result.metadata,
                request_id=request_record.request_id,
            )

        return RuntimeResponse(
            accepted=False, content=None, provider_name=None,
            reason=f"every available provider failed for capability {request.capability.value}",
        )
