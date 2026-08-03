"""
Voice Layer — STT Provider Contract (Phase 65.2, TASK 1).

`STTProviderContract` mirrors `ai_layer/voice_ai/provider_contract.py`'s
`VoiceProviderContract` shape exactly, applied to the opposite
direction: `transcribe(request) -> STTResult` (abstract),
`validate()`/`health_check()` (concrete, overridable defaults). Not an
extension of `VoiceProviderContract` itself -- that contract's one
abstract method (`generate_audio`) is text-in/audio-out shaped, the
wrong direction for this contract's audio-in/text-out shape; sharing a
single ABC across both would force one of the two directions to
implement an irrelevant method. `STTProviderError` (and its
`STTProviderTimeoutError`/`STTProviderUnavailableError`/
`STTProviderInvalidResponseError` subclasses) mirrors
`VoiceProviderError`'s shape without importing it -- each contract
stays self-contained, same posture Phase 65.1 already chose over
importing `ai/providers/runtime_errors.py`.
"""

from abc import ABC, abstractmethod

from ai_layer.voice_ai.stt.models import STTRequest, STTResult


class STTProviderError(Exception):
    """Base class every real adapter raises on failure -- never a raw `requests`/SDK exception, never the API key."""

    def __init__(self, provider_name: str, reason: str) -> None:
        self.provider_name = provider_name
        self.reason = reason
        super().__init__(f"[{provider_name}] {reason}")


class STTProviderTimeoutError(STTProviderError):
    pass


class STTProviderUnavailableError(STTProviderError):
    """Covers both 'no API key configured' and 'network/connection failure'."""
    pass


class STTProviderInvalidResponseError(STTProviderError):
    pass


class STTProviderContract(ABC):
    """Contract every STT adapter implements. A provider that cannot serve a request raises an `STTProviderError` subclass rather than fabricating an `STTResult`."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Stable provider identity, e.g. "openai" -- used by STTManager's adapter registry."""
        raise NotImplementedError

    @abstractmethod
    def transcribe(self, request: STTRequest) -> STTResult:
        """Raises an `STTProviderError` subclass on any failure -- never returns a fabricated READY result."""
        raise NotImplementedError

    def validate(self) -> bool:
        """Default: always valid. A real adapter overrides this to report whether it currently has usable configuration, without making a real network call."""
        return True

    def health_check(self) -> bool:
        """Default: delegates to validate()."""
        return self.validate()
