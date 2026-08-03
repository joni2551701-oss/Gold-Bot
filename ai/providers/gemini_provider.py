"""
AI Layer — Real Gemini Provider (Phase 61.2: AI Runtime Foundation,
TASK 3).

The first non-placeholder `BaseAIProvider` implementation. Starts with
Gemini specifically because `core/secrets.py` already has
`GEMINI_API_KEY` (reserved since Phase 55, read by the pre-existing
fundamental-intelligence prompt layer's own provider-readiness check)
and no other provider has a real key configured yet -- OpenAI/Claude/
Grok/Local LLM (`ai/providers/placeholder_providers.py`) stay stub
implementations this phase, per the brief's own "Boshlanish: Gemini
Provider" scoping.

Real HTTP call via `requests` (already a dependency, same library
`data/twelve_data_client.py` uses) directly against the Gemini REST
API -- no new SDK dependency added. The API key travels only in the
`x-goog-api-key` request header, never in the URL/query string, so it
can never appear in a logged URL (Rule 2: never logged).

Scope this phase: `analyze()`/`chat()`/`explain()` all route through
one real call (`_generate()`) -- Gemini's REST API has no separate
per-capability endpoint, so there is nothing to duplicate here.
`vision()`/`image()`/`voice()` raise `NotImplementedError`, exactly
matching `BaseAIProvider`'s own already-documented contract ("A
provider that cannot serve a given capability raises
NotImplementedError rather than silently returning a fabricated
answer") -- real multimodal support is out of this phase's scope.
Note this means `capabilities()`'s inherited default (declaring VISION
support, per `ai/providers/provider_capabilities.py`'s vendor-level
matrix) is broader than what this class actually implements yet;
`ai/runtime/ai_service.py` (TASK 6) is responsible for catching
`NotImplementedError` from a provider call the same way it catches
`ai.providers.runtime_errors.ProviderRuntimeError`.
"""

from typing import Optional

import requests

from ai.providers.base_provider import BaseAIProvider, ProviderResult
from ai.providers.runtime_errors import (
    ProviderInvalidResponseError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from core_layer.logger.logger import setup_logger
from core_layer.secrets import Secrets

logger = setup_logger("GeminiProvider")

_GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
_REQUEST_TIMEOUT_SECONDS = 15


class GeminiProvider(BaseAIProvider):
    """
    `session`/`secrets` are both injectable (same convention
    `data/providers/twelvedata_provider.py`'s `client` parameter and
    `data/twelve_data_client.py`'s own constructor use) so a test never
    performs a real network call or needs a real environment variable
    set -- see `tests/ai/providers/test_gemini_provider.py`.
    """

    def __init__(self, session=None, secrets: Optional[Secrets] = None) -> None:
        self._session = session or requests
        self._secrets = secrets or Secrets()
        try:
            self._api_key = self._secrets.GEMINI_API_KEY
        except Exception:
            # Missing/invalid key: fail gracefully, same posture as
            # data/twelve_data_client.py's own __init__ -- report
            # unavailability per-call (health_check()/_generate()),
            # never crash at construction time.
            self._api_key = None

    @property
    def name(self) -> str:
        return "gemini"

    def health_check(self) -> bool:
        """Overrides the base class's always-True default -- reports whether a usable API key is configured, without making a real network call."""
        return self._api_key is not None

    def _generate(self, prompt: str) -> ProviderResult:
        """
        The one real network call every text capability routes
        through. Raises `ai.providers.runtime_errors.ProviderRuntimeError`
        (never a raw `requests` exception, never the API key) on any
        failure -- `ai/runtime/ai_service.py` (TASK 6) is the layer
        that catches it, records health, and falls back to the next
        provider.
        """
        if self._api_key is None:
            raise ProviderUnavailableError(self.name, "GEMINI_API_KEY not configured")

        headers = {"x-goog-api-key": self._api_key, "Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = self._session.post(
                _GEMINI_ENDPOINT, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout as e:
            raise ProviderTimeoutError(self.name, "request timed out") from e
        except requests.exceptions.RequestException as e:
            raise ProviderUnavailableError(self.name, "network error") from e

        if response.status_code == 429:
            raise ProviderRateLimitError(self.name, "rate limited (HTTP 429)")
        if response.status_code >= 400:
            raise ProviderUnavailableError(self.name, f"HTTP {response.status_code}")

        try:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (ValueError, KeyError, IndexError, TypeError) as e:
            raise ProviderInvalidResponseError(self.name, "unexpected response shape") from e

        return ProviderResult(content=text, metadata={"provider": self.name})

    def analyze(self, prompt: str) -> ProviderResult:
        return self._generate(prompt)

    def chat(self, prompt: str) -> ProviderResult:
        return self._generate(prompt)

    def explain(self, prompt: str) -> ProviderResult:
        return self._generate(prompt)

    def vision(self, prompt: str, image_ref: Optional[str] = None) -> ProviderResult:
        raise NotImplementedError("GeminiProvider.vision() -- real multimodal support not implemented this phase")

    def image(self, prompt: str) -> ProviderResult:
        raise NotImplementedError("GeminiProvider.image() -- real image generation not implemented this phase")

    def voice(self, prompt: str) -> ProviderResult:
        raise NotImplementedError("GeminiProvider.voice() -- real voice support not implemented this phase")
