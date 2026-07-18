"""
Voice Layer — Voice Runtime (Phase 65.0, TASK 8).

A thin façade over `VoiceManager` -- every method below delegates
directly to `VoiceManager` (or assembles a `VoiceRequest`/`VoiceResult`
from already-computed primitive values); it computes nothing
`VoiceManager` doesn't already compute. Same "no duplicate logic"
resolution `docs/PHASE65_0_AUDIT.md`'s TASK 3/4/8 section already
decided. No network call, no SDK, no audio library import (Rule 3).
"""

from typing import Optional

from voice.manager import VoiceManager
from voice.models import (
    VoiceProfile,
    VoiceProvider,
    VoiceProviderType,
    VoiceRequest,
    VoiceResult,
    VoiceResultStatus,
    VoiceSettings,
)

class VoiceRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-64.0 runtime/manager."""

    def __init__(self, manager: Optional[VoiceManager] = None) -> None:
        self._manager = manager or VoiceManager()

    def resolve_profile(self, name: str) -> Optional[VoiceProfile]:
        return self._manager.get_profile(name)

    def resolve_provider(self, provider_type: VoiceProviderType) -> Optional[VoiceProvider]:
        return self._manager.get_provider(provider_type)

    def validate(self, request: VoiceRequest) -> bool:
        return self._manager.validate(request)

    def build_request(
        self,
        request_id: str,
        profile_name: str,
        provider_type: VoiceProviderType,
        text: str,
        settings: Optional[VoiceSettings] = None,
        requested_at: str = "",
    ) -> VoiceRequest:
        """Pure construction -- no validation here, matching every other Phase 63.x-64.0 'build_*' method (validation is a separate, explicit step via validate())."""
        return VoiceRequest(
            id=request_id,
            profile_name=profile_name,
            provider_type=provider_type,
            text=text,
            settings=settings if settings is not None else VoiceSettings(),
            requested_at=requested_at,
        )

    def build_result(self, request: VoiceRequest, ok: bool, reason: str = "", generated_at: str = "") -> VoiceResult:
        """Pure construction from an already-computed ok flag -- never re-runs validate() itself, so the caller's own validate()/prepare_voice() call is the single source of truth for ok."""
        return VoiceResult(
            request_id=request.id,
            status=VoiceResultStatus.READY if ok else VoiceResultStatus.REJECTED,
            reason=reason,
            generated_at=generated_at,
        )

    def prepare_voice(self, request: VoiceRequest, generated_at: str = "") -> VoiceResult:
        """Composes validate() + build_result() into the one full-lifecycle call -- the only method here that calls two of this class's own methods rather than just VoiceManager."""
        ok = self.validate(request)
        reason = "" if ok else "profile/provider unresolved, provider disabled, or empty text"
        return self.build_result(request, ok, reason=reason, generated_at=generated_at)
