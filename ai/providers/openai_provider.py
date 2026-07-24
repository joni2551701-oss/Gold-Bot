"""
AI Layer — Real OpenAI Provider (Phase 61.5: AI Production Integration
Foundation, TASK 1).

Second non-placeholder `BaseAIProvider` implementation, following
`ai/providers/gemini_provider.py`'s exact pattern (Phase 61.2 TASK 3):
`session`/`secrets` both injectable, `health_check()` reports "usable
key configured" without a real network call, one private `_generate()`
every text capability routes through, `vision()`/`image()`/`voice()`
raise `NotImplementedError`. `core/secrets.py` already carries
`OPENAI_API_KEY` as an optional secret (Phase 61.2 TASK 2) — no
secrets change needed for this task.

Real HTTP call via `requests` (no new SDK dependency) directly against
OpenAI's REST API. The API key travels only in the `Authorization`
request header, never in the URL/query string.
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
from core.logger import setup_logger
from core.secrets import Secrets

logger = setup_logger("OpenAIProvider")

_OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
_OPENAI_MODEL = "gpt-4o-mini"
_REQUEST_TIMEOUT_SECONDS = 15


class OpenAIProvider(BaseAIProvider):
    """`session`/`secrets` are both injectable so a test never performs a real network call or needs a real environment variable set -- see `tests/ai/providers/test_openai_provider.py`."""

    def __init__(self, session=None, secrets: Optional[Secrets] = None) -> None:
        self._session = session or requests
        self._secrets = secrets or Secrets()
        try:
            self._api_key = self._secrets.OPENAI_API_KEY
        except Exception:
            self._api_key = None

    @property
    def name(self) -> str:
        return "openai"

    def health_check(self) -> bool:
        """Overrides the base class's always-True default -- reports whether a usable API key is configured, without making a real network call."""
        return self._api_key is not None

    def _generate(self, prompt: str) -> ProviderResult:
        """The one real network call every text capability routes through. Raises `ai.providers.runtime_errors.ProviderRuntimeError` (never a raw `requests` exception, never the API key) on any failure."""
        if self._api_key is None:
            raise ProviderUnavailableError(self.name, "OPENAI_API_KEY not configured")

        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        payload = {"model": _OPENAI_MODEL, "messages": [{"role": "user", "content": prompt}]}

        try:
            response = self._session.post(
                _OPENAI_ENDPOINT, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT_SECONDS,
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
            text = data["choices"][0]["message"]["content"]
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
        raise NotImplementedError("OpenAIProvider.vision() -- real multimodal support not implemented this phase")

    def image(self, prompt: str) -> ProviderResult:
        raise NotImplementedError("OpenAIProvider.image() -- real image generation not implemented this phase")

    def voice(self, prompt: str) -> ProviderResult:
        raise NotImplementedError("OpenAIProvider.voice() -- real voice support not implemented this phase")
