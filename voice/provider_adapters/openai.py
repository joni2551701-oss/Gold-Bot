"""
Voice Layer — Real OpenAI TTS Provider Adapter (Phase 65.1, TASK 3).

Follows `ai/providers/openai_provider.py`/`gemini_provider.py`'s exact
pattern (Phase 61.2/61.5): `session`/`secrets` both injectable,
`validate()` reports "usable key configured" without a real network
call, one real HTTP call via `requests` (no new SDK dependency)
directly against OpenAI's REST API. `core/secrets.py` already carries
`OPENAI_API_KEY` (Phase 61.2) -- reused as-is, no secrets change
needed for this adapter.

The API key travels only in the `Authorization` request header, never
in the URL/query string, never in a raised exception's message (same
convention `voice/provider_contract.py`'s `VoiceProviderError`
enforces).
"""

from typing import Optional

import requests

from core.logger import setup_logger
from core_layer.secrets import Secrets
from voice.models import VoiceRequest, VoiceResult, VoiceResultStatus
from voice.provider_contract import (
    VoiceProviderContract,
    VoiceProviderInvalidResponseError,
    VoiceProviderTimeoutError,
    VoiceProviderUnavailableError,
)

logger = setup_logger("OpenAIVoiceProvider")

_OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"
_OPENAI_TTS_MODEL = "tts-1"
_REQUEST_TIMEOUT_SECONDS = 30


class OpenAIVoiceProvider(VoiceProviderContract):
    """`session`/`secrets` are both injectable so a test never performs a real network call or needs a real environment variable set."""

    def __init__(self, session=None, secrets: Optional[Secrets] = None) -> None:
        self._session = session or requests
        self._secrets = secrets or Secrets()
        try:
            self._api_key = self._secrets.OPENAI_API_KEY
        except Exception:
            self._api_key = None

    @property
    def provider_name(self) -> str:
        return "openai"

    def validate(self) -> bool:
        """Overrides the base class's always-True default -- reports whether a usable API key is configured, without making a real network call."""
        return self._api_key is not None

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        """The one real network call this adapter makes. Raises a `VoiceProviderError` subclass (never a raw `requests` exception, never the API key) on any failure."""
        if self._api_key is None:
            raise VoiceProviderUnavailableError(self.provider_name, "OPENAI_API_KEY not configured")

        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        payload = {
            "model": _OPENAI_TTS_MODEL,
            "input": request.text,
            "voice": "alloy",
            "response_format": "mp3",
        }

        try:
            response = self._session.post(
                _OPENAI_TTS_ENDPOINT, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout as e:
            raise VoiceProviderTimeoutError(self.provider_name, "request timed out") from e
        except requests.exceptions.RequestException as e:
            raise VoiceProviderUnavailableError(self.provider_name, "network error") from e

        if response.status_code >= 400:
            raise VoiceProviderUnavailableError(self.provider_name, f"HTTP {response.status_code}")

        audio_bytes = response.content
        if not audio_bytes:
            raise VoiceProviderInvalidResponseError(self.provider_name, "empty audio response")

        return VoiceResult(
            request_id=request.id,
            status=VoiceResultStatus.READY,
            reason="",
            metadata={
                "provider": self.provider_name,
                "content_type": response.headers.get("Content-Type", "audio/mpeg"),
                "byte_length": len(audio_bytes),
            },
        )
