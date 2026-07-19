"""
Voice Layer — Real OpenAI STT Provider Adapter (Phase 65.2, TASK 2).

Follows `voice/provider_adapters/openai.py`'s exact pattern (Phase
65.1): `session`/`secrets` both injectable, `validate()` reports
"usable key configured" without a real network call, one real HTTP
call via `requests` (no new SDK dependency) directly against OpenAI's
Whisper REST API. Reuses the existing `OPENAI_API_KEY` secret (Phase
61.2) -- STT and TTS share one OpenAI account, no new secret needed.

The API key travels only in the `Authorization` request header, never
in the URL/query string, never in a raised exception's message.
"""

from typing import Optional

import requests

from core.logger import setup_logger
from core.secrets import Secrets
from voice.stt.contract import (
    STTProviderContract,
    STTProviderInvalidResponseError,
    STTProviderTimeoutError,
    STTProviderUnavailableError,
)
from voice.stt.models import STTRequest, STTResult, STTResultStatus

logger = setup_logger("OpenAISTTProvider")

_OPENAI_STT_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"
_OPENAI_STT_MODEL = "whisper-1"
_REQUEST_TIMEOUT_SECONDS = 30


class OpenAISTTProvider(STTProviderContract):
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

    def transcribe(self, request: STTRequest) -> STTResult:
        """The one real network call this adapter makes. Raises an `STTProviderError` subclass (never a raw `requests` exception, never the API key) on any failure."""
        if self._api_key is None:
            raise STTProviderUnavailableError(self.provider_name, "OPENAI_API_KEY not configured")

        headers = {"Authorization": f"Bearer {self._api_key}"}
        data = {"model": _OPENAI_STT_MODEL, "language": request.language}
        files = {"file": ("audio.wav", request.audio, "audio/wav")}

        try:
            response = self._session.post(
                _OPENAI_STT_ENDPOINT, headers=headers, data=data, files=files, timeout=_REQUEST_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout as e:
            raise STTProviderTimeoutError(self.provider_name, "request timed out") from e
        except requests.exceptions.RequestException as e:
            raise STTProviderUnavailableError(self.provider_name, "network error") from e

        if response.status_code >= 400:
            raise STTProviderUnavailableError(self.provider_name, f"HTTP {response.status_code}")

        try:
            payload = response.json()
            text = payload["text"]
        except (ValueError, KeyError, TypeError) as e:
            raise STTProviderInvalidResponseError(self.provider_name, "unexpected response shape") from e

        if not text:
            raise STTProviderInvalidResponseError(self.provider_name, "empty transcription")

        return STTResult(
            request_id=request.id,
            status=STTResultStatus.READY,
            text=text,
            metadata={"provider": self.provider_name},
        )
