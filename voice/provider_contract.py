"""
Voice Layer — Voice Provider Contract (Phase 65.1, TASK 1).

The one interface every real voice-synthesis adapter
(`voice/provider_adapters/*.py`) implements: `generate_audio()`/
`validate()`/`health_check()`, matching the brief's own TASK 1
interface literally. Deliberately not an extension of
`ai/providers/base_provider.py`'s `BaseAIProvider` -- that contract is
LLM-chat-shaped (`analyze`/`chat`/`explain`/`vision`/`image`/`voice`,
all returning one `str`-based `ProviderResult`), a different domain
from TTS synthesis; see `docs/PHASE65_1_AUDIT.md`'s own resolution.
Reuses `BaseAIProvider`'s *pattern* only (injectable `session`/
`secrets`, concrete overridable `health_check()` default, typed
runtime errors) -- no import from `ai/providers/` anywhere in this
package.

Contract only this task -- no real API call lives here (Rule 1's own
TASK 1 instruction: "Faqat contract. Real API yo'q.").
"""

from abc import ABC, abstractmethod

from voice.models import VoiceRequest, VoiceResult


class VoiceProviderError(Exception):
    """
    Base class every real adapter raises on failure -- never a raw
    `requests`/SDK exception, never the API key. Mirrors
    `ai/providers/runtime_errors.py`'s `ProviderRuntimeError` shape
    (`provider_name`/`reason`) without importing that module, keeping
    `voice/` self-contained.
    """

    def __init__(self, provider_name: str, reason: str) -> None:
        self.provider_name = provider_name
        self.reason = reason
        super().__init__(f"[{provider_name}] {reason}")


class VoiceProviderTimeoutError(VoiceProviderError):
    pass


class VoiceProviderUnavailableError(VoiceProviderError):
    """Covers both 'no API key configured' and 'network/connection failure' -- both mean the same thing to a caller: this provider cannot serve the request right now."""
    pass


class VoiceProviderInvalidResponseError(VoiceProviderError):
    pass


class VoiceProviderContract(ABC):
    """
    Contract every voice-synthesis adapter implements. A provider that
    cannot serve a request raises a `VoiceProviderError` subclass
    rather than silently returning a fabricated `VoiceResult` -- same
    "never fabricate" convention `BaseAIProvider` and every other
    Phase 61.x-65.x contract in this codebase already uses.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Stable provider identity, e.g. "openai" -- used by VoiceManager's adapter registry."""
        raise NotImplementedError

    @abstractmethod
    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        """Raises a `VoiceProviderError` subclass on any failure -- never returns a fabricated READY result."""
        raise NotImplementedError

    def validate(self) -> bool:
        """Default: always valid. A real adapter overrides this to report whether it currently has usable configuration (e.g. an API key), without making a real network call -- same posture as `BaseAIProvider.health_check()`'s own default."""
        return True

    def health_check(self) -> bool:
        """Default: delegates to validate() -- a real adapter's "healthy" and "configured" checks are the same question this phase (no live network probe exists yet)."""
        return self.validate()
