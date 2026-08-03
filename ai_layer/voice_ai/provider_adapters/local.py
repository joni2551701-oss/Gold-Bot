"""
Voice Layer — Local Voice Provider Adapter Skeleton (Phase 65.1, TASK 5).

No real local inference is wired this phase (Rule 1: "Real model shart
emas... Kelajak uchun" -- not required, for a future phase), mirroring
`ai/providers/placeholder_providers.py`'s `LocalLLMProvider` stub
posture: the interface is ready, `validate()` reports `False` (not
configured), `generate_audio()` raises rather than fabricating a
`VoiceResult` -- never a silent fake success.
"""

from ai_layer.voice_ai.models import VoiceRequest, VoiceResult
from ai_layer.voice_ai.provider_contract import VoiceProviderContract, VoiceProviderUnavailableError


class LocalVoiceProvider(VoiceProviderContract):
    """Skeleton only -- no local inference backend exists yet. A future phase replaces `generate_audio()`'s body with a real local model call, the same way `ai/providers/gemini_provider.py` replaced its own placeholder in Phase 61.2."""

    @property
    def provider_name(self) -> str:
        return "local"

    def validate(self) -> bool:
        return False

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        raise VoiceProviderUnavailableError(self.provider_name, "no local voice backend wired yet")
