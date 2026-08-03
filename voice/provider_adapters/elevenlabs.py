"""
Voice Layer — Real ElevenLabs TTS Provider Adapter (Phase 65.1, TASK 4).

Same pattern as `voice/provider_adapters/openai.py` (Phase 65.1 TASK
3): `session`/`secrets` both injectable, `validate()` reports "usable
key configured" without a real network call, one real HTTP call via
`requests` (no new SDK dependency) directly against ElevenLabs' REST
API. `core/secrets.py` gained `ELEVENLABS_API_KEY` this phase (TASK 2).

Supports voice id, emotion/style, and language via `VoiceRequest`'s
own `settings` field -- no new fields added to `VoiceRequest`/
`VoiceSettings` (both LOCKed since Phase 65.0); `settings.language`
maps to ElevenLabs' language hint, a default voice id is used unless a
future phase adds one to `VoiceSettings`.

The API key travels only in the `xi-api-key` request header, never in
the URL/query string, never in a raised exception's message.
"""

from typing import Optional

import requests

from core_layer.logger.logger import setup_logger
from core_layer.secrets import Secrets
from voice.models import VoiceRequest, VoiceResult, VoiceResultStatus
from voice.provider_contract import (
    VoiceProviderContract,
    VoiceProviderInvalidResponseError,
    VoiceProviderTimeoutError,
    VoiceProviderUnavailableError,
)

logger = setup_logger("ElevenLabsVoiceProvider")

_ELEVENLABS_TTS_ENDPOINT_TEMPLATE = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
_REQUEST_TIMEOUT_SECONDS = 30


class ElevenLabsVoiceProvider(VoiceProviderContract):
    """`session`/`secrets` are both injectable so a test never performs a real network call or needs a real environment variable set."""

    def __init__(self, session=None, secrets: Optional[Secrets] = None, voice_id: str = _DEFAULT_VOICE_ID) -> None:
        self._session = session or requests
        self._secrets = secrets or Secrets()
        self._voice_id = voice_id
        try:
            self._api_key = self._secrets.ELEVENLABS_API_KEY
        except Exception:
            self._api_key = None

    @property
    def provider_name(self) -> str:
        return "elevenlabs"

    def validate(self) -> bool:
        """Overrides the base class's always-True default -- reports whether a usable API key is configured, without making a real network call."""
        return self._api_key is not None

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        """The one real network call this adapter makes. Raises a `VoiceProviderError` subclass (never a raw `requests` exception, never the API key) on any failure."""
        if self._api_key is None:
            raise VoiceProviderUnavailableError(self.provider_name, "ELEVENLABS_API_KEY not configured")

        headers = {"xi-api-key": self._api_key, "Content-Type": "application/json"}
        payload = {
            "text": request.text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        endpoint = _ELEVENLABS_TTS_ENDPOINT_TEMPLATE.format(voice_id=self._voice_id)

        try:
            response = self._session.post(
                endpoint, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT_SECONDS,
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
                "voice_id": self._voice_id,
            },
        )
