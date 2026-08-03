"""
Voice Layer — Local STT Provider Adapter Skeleton (Phase 65.2, TASK 2).

No real local inference is wired this phase, mirroring
`voice/provider_adapters/local.py`'s stub posture: the interface is
ready, `validate()` reports `False`, `transcribe()` raises rather than
fabricating an `STTResult`.
"""

from ai_layer.voice_ai.stt.contract import STTProviderContract, STTProviderUnavailableError
from ai_layer.voice_ai.stt.models import STTRequest, STTResult


class LocalSTTProvider(STTProviderContract):
    """Skeleton only -- no local STT backend exists yet."""

    @property
    def provider_name(self) -> str:
        return "local"

    def validate(self) -> bool:
        return False

    def transcribe(self, request: STTRequest) -> STTResult:
        raise STTProviderUnavailableError(self.provider_name, "no local STT backend wired yet")
