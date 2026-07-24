"""
Voice Layer — Custom Voice Provider Adapter Skeleton (Phase 65.1, TASK 5).

Extensibility point for a future deployment-specific voice backend
(self-hosted TTS, an in-house model, etc.) -- same skeleton posture as
`voice/provider_adapters/local.py`. No real backend exists yet;
`generate_audio()` raises rather than fabricating a `VoiceResult`.
"""

from voice.models import VoiceRequest, VoiceResult
from voice.provider_contract import VoiceProviderContract, VoiceProviderUnavailableError


class CustomVoiceProvider(VoiceProviderContract):
    """Skeleton only -- a future deployment wires a real backend into `generate_audio()`'s body without changing this class's public shape (Article 9)."""

    @property
    def provider_name(self) -> str:
        return "custom"

    def validate(self) -> bool:
        return False

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        raise VoiceProviderUnavailableError(self.provider_name, "no custom voice backend configured")
