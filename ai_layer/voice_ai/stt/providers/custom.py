"""
Voice Layer — Custom STT Provider Adapter Skeleton (Phase 65.2, TASK 2).

Extensibility point for a future deployment-specific STT backend --
same skeleton posture as `voice/provider_adapters/custom.py`.
"""

from ai_layer.voice_ai.stt.contract import STTProviderContract, STTProviderUnavailableError
from ai_layer.voice_ai.stt.models import STTRequest, STTResult


class CustomSTTProvider(STTProviderContract):
    """Skeleton only -- a future deployment wires a real backend into `transcribe()`'s body without changing this class's public shape (Article 9)."""

    @property
    def provider_name(self) -> str:
        return "custom"

    def validate(self) -> bool:
        return False

    def transcribe(self, request: STTRequest) -> STTResult:
        raise STTProviderUnavailableError(self.provider_name, "no custom STT backend configured")
