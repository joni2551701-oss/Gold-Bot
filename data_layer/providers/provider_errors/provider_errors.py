"""
Data Layer — Provider Error Contract (TASK-CORE-003).

A single, raisable exception hierarchy every market-data provider in
data_layer/providers/ standardises on, so a caller catches one family of
errors regardless of which provider (TwelveData, Bitget, Keynorq,
Binance, MT5) produced it.

MODULE REUSE NOTE (CLAUDE.md Module Reuse Principle, steps 1-3):
1. Does a raisable provider-error hierarchy already exist for THIS
   (market-data) layer? No. data_layer/providers/api_error_classifier.py exists, but
   it CONSTRUCTS a core_layer.errors.exceptions.ExternalAPIError for logging
   only -- it is never itself raised and does not give providers a
   raise-able contract (see its own docstring: "this function is never
   itself raised, only constructed and logged").
2. Can an existing hierarchy be extended? ai/providers/runtime_errors.py
   has a parallel family (ProviderRuntimeError/…), but it is the AI/LLM
   provider domain and is out of this task's scope (the task edits only
   data_layer/providers/). Reusing it would couple the market-data layer to
   the AI layer -- exactly the cross-layer import CLAUDE.md forbids.
3. Therefore a new, market-data-domain error module is created here,
   and this note records why 1 and 2 were both "no".

SECURITY (CLAUDE.md Trading Safety / task Security rules): an error
carries only the provider's own name and a human-readable message.
Callers MUST NOT put an API key, a full request URL (which may embed a
key), or any credential into the message -- the provider adapters in
this package never do (they pass short, fixed reasons). repr()/str()
render only "provider: message", so a credential cannot leak through a
traceback as long as callers honour that contract.

These errors are raised by a provider's *data-fetch* path when it
chooses to signal a failure as an exception. get_market_status() still
must NEVER raise (base_provider.py's contract) -- it returns a
ProviderStatus(available=False, reason=…) instead. This module is for
the get_candles()/get_latest_price() paths of a *real* provider once
one makes live calls; the current stubs raise NotImplementedError,
which is intentionally distinct from these ("not built yet" vs "built,
but the upstream call failed").
"""

from typing import Optional


class ProviderError(Exception):
    """
    Base for every market-data provider error. Holds the provider's
    stable name (e.g. "twelvedata") and a short human message. Never
    embeds a credential -- see the module docstring's SECURITY note.
    """

    def __init__(self, provider: str, message: str = "") -> None:
        self.provider = provider
        self.message = message
        super().__init__(f"{provider}: {message}" if message else provider)


class ProviderAuthError(ProviderError):
    """Authentication/authorization failure -- HTTP 401 or 403 (bad/missing/again-rejected key). The key value is never included."""


class ProviderTimeoutError(ProviderError):
    """The upstream request exceeded its timeout before any response arrived."""


class ProviderRateLimitError(ProviderError):
    """The provider is throttling us -- HTTP 429 (too many requests)."""


class ProviderResponseError(ProviderError):
    """
    A response arrived but could not be used -- HTTP 404 (endpoint/
    symbol not found), invalid JSON, a missing required field, or an
    otherwise malformed body.
    """


class ProviderUnavailableError(ProviderError):
    """The provider itself is down/unreachable -- HTTP 5xx, a network error, or a provider with no live implementation configured."""


# Ordered map from HTTP status -> the specific error class. 401/403 ->
# auth, 404 -> response (not-found), 429 -> rate limit, 5xx ->
# unavailable. Anything else 4xx -> response error (a bad request we
# sent), matching the task's own error-handling table.
def provider_error_for_status(
    provider: str, status_code: int, message: str = "", cause: Optional[BaseException] = None
) -> ProviderError:
    """
    Map an HTTP status code to the right ProviderError subclass. A pure
    classifier -- it CONSTRUCTS and returns the error (mirroring
    data_layer/providers/api_error_classifier.py's non-raising style); the caller
    decides whether to raise it. Never raises itself. `message` must
    not contain a credential (see module SECURITY note); `cause` is an
    optional underlying exception for chaining (`raise err from cause`).
    """
    if status_code in (401, 403):
        error: ProviderError = ProviderAuthError(provider, message or f"HTTP {status_code}")
    elif status_code == 429:
        error = ProviderRateLimitError(provider, message or "rate limited (HTTP 429)")
    elif status_code == 404:
        error = ProviderResponseError(provider, message or "HTTP 404 (not found)")
    elif 500 <= status_code <= 599:
        error = ProviderUnavailableError(provider, message or f"HTTP {status_code}")
    elif 400 <= status_code <= 499:
        error = ProviderResponseError(provider, message or f"HTTP {status_code}")
    else:
        error = ProviderError(provider, message or f"HTTP {status_code}")
    if cause is not None:
        error.__cause__ = cause
    return error
