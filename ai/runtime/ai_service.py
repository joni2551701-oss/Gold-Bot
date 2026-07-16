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
"""

import hashlib
import time
from typing import Dict, Optional

from ai.access.access_control import AccessControl
from ai.audit.request_log import RequestLog
from ai.audit.response_log import ResponseLog
from ai.cache.cache_policy import build_cache_key_from_context
from ai.cache.response_cache import ResponseCache
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.prompts.prompt_manager import PromptManager
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.providers.runtime_errors import ProviderRuntimeError, record_provider_failure
from ai.router.router import AIRouter
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
    ) -> None:
        self._capability_manager = capability_manager or CapabilityManager()
        self._access_control = access_control or AccessControl()
        self._provider_manager = provider_manager or ProviderManager()
        self._health_tracker = health_tracker or ProviderHealthTracker()
        self._router = router or AIRouter(
            self._provider_manager, capability_manager=self._capability_manager, health_tracker=self._health_tracker,
        )
        self._response_cache = response_cache or ResponseCache()
        self._request_log = request_log or RequestLog()
        self._response_log = response_log or ResponseLog()
        self._prompt_manager = prompt_manager or PromptManager()

    def _resolve_prompt(self, request: RuntimeRequest) -> Optional[str]:
        """Reuses PromptManager.get_market_analysis_prompt() when a market context is available -- never builds prompt text itself. Returns None (never raises) when neither an explicit prompt nor a market context was supplied."""
        if request.prompt is not None:
            return request.prompt
        if request.ai_context.market_context is not None:
            return self._prompt_manager.get_market_analysis_prompt(request.ai_context.market_context)
        return None

    def ask(self, request: RuntimeRequest) -> RuntimeResponse:
        """Never raises: every rejection path (access/capability/prompt/provider/validation) returns an unaccepted RuntimeResponse instead."""
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

        attempted = set()
        max_attempts = max(len(self._provider_manager.list_providers()), 1)

        for _ in range(max_attempts):
            routing_result = self._router.route(request.capability)
            provider_name = routing_result.provider_name
            if provider_name is None:
                return RuntimeResponse(accepted=False, content=None, provider_name=None, reason=routing_result.reason)
            if provider_name in attempted:
                break
            attempted.add(provider_name)

            cache_key = build_cache_key_from_context(
                request.ai_context, request.capability, provider_name, _PROMPT_VERSION, request.role.value,
                context_hash=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            )
            cached_entry = self._response_cache.get(cache_key)
            if cached_entry is not None:
                return RuntimeResponse(
                    accepted=True, content=cached_entry.content, provider_name=provider_name,
                    reason="cache hit", from_cache=True, metadata=dict(cached_entry.metadata),
                )

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
                logger.info(f"Provider {provider_name} does not implement {method_name}() -- trying next provider")
                continue
            except ProviderRuntimeError as e:
                record_provider_failure(self._health_tracker, e)
                self._response_log.record(
                    request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                    latency_ms=(time.monotonic() - started_at) * 1000, tokens=0, cost=0.0, status="FAILED",
                )
                logger.warning(f"Provider {provider_name} failed: {e.reason} -- trying next provider")
                continue

            latency_ms = (time.monotonic() - started_at) * 1000
            validation = validate_response(result)

            if not validation.accepted:
                self._response_log.record(
                    request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                    latency_ms=latency_ms, tokens=0, cost=0.0, status="REJECTED",
                )
                return RuntimeResponse(
                    accepted=False, content=None, provider_name=provider_name,
                    reason="response failed validation", errors=validation.errors,
                    request_id=request_record.request_id,
                )

            self._response_log.record(
                request_id=request_record.request_id, capability=request.capability, provider_name=provider_name,
                latency_ms=latency_ms, tokens=0, cost=0.0, status="SUCCESS",
            )
            self._response_cache.put(cache_key, result.content, metadata=result.metadata)

            return RuntimeResponse(
                accepted=True, content=result.content, provider_name=provider_name,
                reason="provider call succeeded", metadata=result.metadata,
                request_id=request_record.request_id,
            )

        return RuntimeResponse(
            accepted=False, content=None, provider_name=None,
            reason=f"every available provider failed for capability {request.capability.value}",
        )
