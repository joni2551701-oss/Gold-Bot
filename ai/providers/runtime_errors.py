"""
AI Layer — Provider Runtime Errors (Phase 61.2: AI Runtime Foundation,
TASK 4).

A real provider call (unlike every placeholder before this phase) can
genuinely fail -- timeout, rate limit, an unparseable response, or the
provider being unreachable entirely. `BaseAIProvider`'s own docstring
(Phase 61.0) already established the convention that a provider
"raises NotImplementedError rather than silently returning a
fabricated answer" for a capability it cannot serve; this module
extends that same "raise a structured, safe error, never fabricate an
answer" posture to real network failures.

**Never includes the API key** in any exception message (Rule 2) --
every constructor below takes only `provider_name` and a short,
human-written `reason`; a caller building the exception is responsible
for not passing key/header/token material as `reason`, and this
module's own use (`ai/providers/gemini_provider.py`) never does.

`classify_provider_exception()` maps a raw `requests` exception into
one of these -- the same "classify at the boundary, don't leak a raw
SDK/library exception upward" convention `data/api_error_classifier.py`
already established for market-data providers.
"""

from typing import TYPE_CHECKING

import requests

from ai.providers.provider_status import HealthStatus

if TYPE_CHECKING:
    # TYPE_CHECKING-only: provider_health.py imports provider_registry.py,
    # which (via gemini_provider.py, Phase 61.2 TASK 3) imports this
    # module -- a real (non-TYPE_CHECKING) import here would be a
    # circular import. record_provider_failure() below only calls
    # `.record(...)`, duck-typed, so no runtime import is needed.
    from ai.providers.provider_health import ProviderHealthTracker


class ProviderRuntimeError(Exception):
    """Base class -- a caller (ai/runtime/ai_service.py) catches this one type to cover every real-provider failure mode."""

    def __init__(self, provider_name: str, reason: str) -> None:
        self.provider_name = provider_name
        self.reason = reason
        super().__init__(f"[{provider_name}] {reason}")


class ProviderTimeoutError(ProviderRuntimeError):
    pass


class ProviderRateLimitError(ProviderRuntimeError):
    pass


class ProviderInvalidResponseError(ProviderRuntimeError):
    pass


class ProviderUnavailableError(ProviderRuntimeError):
    """Covers both 'no API key configured' and 'network/connection failure' -- both mean the same thing to a caller: this provider cannot serve the request right now."""
    pass


def classify_provider_exception(exc: Exception, provider_name: str) -> ProviderRuntimeError:
    """
    Never raises itself -- always returns a `ProviderRuntimeError`
    subclass, even for an exception type this function doesn't
    specifically recognize (falls back to `ProviderUnavailableError`).
    A caller is expected to `raise classify_provider_exception(e, name)
    from e` rather than re-raising `e` directly, so a raw `requests`
    exception (which could carry request headers, including the API
    key, in its own `__str__`) never propagates upward.
    """
    if isinstance(exc, requests.exceptions.Timeout):
        return ProviderTimeoutError(provider_name, "request timed out")
    if isinstance(exc, requests.exceptions.RequestException):
        return ProviderUnavailableError(provider_name, "network error")
    return ProviderUnavailableError(provider_name, "unclassified provider error")


# Flow (TASK 4's own brief): Provider Error -> ProviderHealthTracker ->
# Router fallback. This dict is the one place that mapping lives --
# ai/runtime/ai_service.py (TASK 6) calls record_provider_failure()
# rather than re-deriving which HealthStatus a given error implies.
_ERROR_HEALTH_STATUS = {
    ProviderTimeoutError: HealthStatus.OFFLINE,
    ProviderRateLimitError: HealthStatus.RATE_LIMITED,
    ProviderInvalidResponseError: HealthStatus.DEGRADED,
    ProviderUnavailableError: HealthStatus.OFFLINE,
}


def record_provider_failure(health_tracker: "ProviderHealthTracker", error: ProviderRuntimeError) -> None:
    """Translates a caught ProviderRuntimeError into a ProviderHealthTracker.record() call -- the router (ai/router/router.py, unmodified this phase) then naturally routes around this provider on its next call, exactly as Phase 61.1's health-check-in-selection logic already does."""
    status = _ERROR_HEALTH_STATUS.get(type(error), HealthStatus.OFFLINE)
    health_tracker.record(error.provider_name, status, reason=error.reason)
