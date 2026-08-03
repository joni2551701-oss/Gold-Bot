"""
Voice Layer — STT Manager (Phase 65.2, TASK 1/2).

Adapter registry plus single active-provider selection -- unlike
`VoiceManager`'s *per-profile* provider selection (Phase 65.1, correct
for TTS since different Voice Profiles may want different vendors),
STT has no "profile" concept: one active provider transcribes every
request this phase, mirroring `ai/providers/provider_manager.py`'s
single-selection `ProviderManager` shape more closely than
`VoiceManager`'s. No network call, no SDK import in this file itself
(Rule 1) -- the real HTTP call lives one layer down, in whichever
`STTProviderContract` adapter is registered.
"""

from typing import Dict, List, Optional

from core_layer.logger.logger import setup_logger
from ai_layer.voice_ai.stt.contract import STTProviderContract, STTProviderError
from ai_layer.voice_ai.stt.models import STTRequest, STTResult, STTResultStatus

logger = setup_logger("STTManager")


class STTManager:
    """Every dependency is injectable, same convention as every other Phase 61.x-65.x manager."""

    def __init__(self) -> None:
        self._adapters: Dict[str, STTProviderContract] = {}
        self._active_provider_name: Optional[str] = None

    def register_adapter(self, adapter: STTProviderContract) -> None:
        """Registers/replaces an adapter by its own `provider_name`. Registering an adapter does not itself make it active -- `set_active_provider()` owns that separately."""
        self._adapters[adapter.provider_name] = adapter

    def get_adapter(self, provider_name: str) -> Optional[STTProviderContract]:
        """Never raises: an unregistered provider_name returns None rather than a fabricated adapter."""
        return self._adapters.get(provider_name)

    def list_adapters(self) -> List[str]:
        return list(self._adapters.keys())

    def set_active_provider(self, provider_name: str) -> bool:
        """Never raises: an unknown provider_name is rejected (returns False), same fail-safe posture ai/providers/provider_manager.py's set_status() already uses."""
        if provider_name not in self._adapters:
            logger.warning(f"set_active_provider called for an unregistered STT provider: {provider_name}")
            return False
        self._active_provider_name = provider_name
        return True

    def active_provider(self) -> Optional[STTProviderContract]:
        if self._active_provider_name is None:
            return None
        return self._adapters.get(self._active_provider_name)

    def transcribe(self, request: STTRequest) -> STTResult:
        """Never raises: no active provider, or an STTProviderError from the active adapter, becomes a REJECTED STTResult -- never fabricates a READY result."""
        adapter = self.active_provider()
        if adapter is None:
            return STTResult(request_id=request.id, status=STTResultStatus.REJECTED, reason="no active STT provider")

        try:
            return adapter.transcribe(request)
        except STTProviderError as e:
            return STTResult(request_id=request.id, status=STTResultStatus.REJECTED, reason=str(e))
