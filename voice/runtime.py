"""
Voice Layer — Voice Runtime (Phase 65.0, TASK 8; extended Phase 65.1,
TASK 7/8 -- provider resolution, real generation, and fallback).

A thin façade over `VoiceManager` -- every method below delegates
directly to `VoiceManager` (or assembles a `VoiceRequest`/`VoiceResult`
from already-computed primitive values); it computes nothing
`VoiceManager` doesn't already compute. Same "no duplicate logic"
resolution `docs/PHASE65_0_AUDIT.md`'s TASK 3/4/8 section already
decided. This class itself still makes no network call and imports no
SDK/audio library directly -- `generate_audio()`/`generate_with_fallback()`
(TASK 7/8) delegate the one real network call to whichever
`VoiceProviderContract` adapter `VoiceManager.get_adapter()` returns,
the same "runtime orchestrates, the real call lives one layer down"
posture `ai/runtime/ai_service.py` already uses for LLM providers.
"""

from typing import List, Optional

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
from voice.provider_contract import VoiceProviderError


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

    # --- Provider resolution + real generation (Phase 65.1 TASK 7) ---

    def resolve_provider_for_profile(self, profile_name: str) -> Optional[VoiceProviderType]:
        """Delegates to VoiceManager.provider_for_profile() -- explicit override first, else the profile's own default_provider."""
        return self._manager.provider_for_profile(profile_name)

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        """
        The one full real-generation call: validate() first (never
        skips the Phase 65.0 profile/provider/status/text check), then
        delegates to whichever `VoiceProviderContract` adapter
        `VoiceManager.get_adapter()` returns for `request.provider_type`.
        Never raises -- a `VoiceProviderError` from the adapter (or no
        adapter registered at all) becomes a REJECTED `VoiceResult`,
        the same "never fabricate a READY result" convention every
        other Phase 61.x-65.0 result/asset builder already uses.
        """
        if not self.validate(request):
            return self.build_result(request, ok=False, reason="profile/provider unresolved, provider disabled, or empty text")

        adapter = self._manager.get_adapter(request.provider_type)
        if adapter is None:
            return self.build_result(request, ok=False, reason=f"no adapter registered for provider {request.provider_type.value}")

        try:
            return adapter.generate_audio(request)
        except VoiceProviderError as e:
            return self.build_result(request, ok=False, reason=str(e))

    # --- Fallback handling (Phase 65.1 TASK 8) ---

    def generate_with_fallback(self, request: VoiceRequest, fallback_providers: Optional[List[VoiceProviderType]] = None) -> VoiceResult:
        """
        Tries `request.provider_type` first, then each provider in
        `fallback_providers` in order (each attempt reuses the same
        id/profile_name/text/settings, only `provider_type` changes),
        returning the first READY `VoiceResult`. If every attempt is
        REJECTED, returns the *last* attempt's `VoiceResult` (its
        `reason` reflects the final provider tried) rather than
        raising -- never leaves a caller without some `VoiceResult`.
        """
        result = self.generate_audio(request)
        if result.status == VoiceResultStatus.READY:
            return result

        for provider_type in (fallback_providers or []):
            fallback_request = self.build_request(
                request.id, request.profile_name, provider_type, request.text,
                settings=request.settings, requested_at=request.requested_at,
            )
            result = self.generate_audio(fallback_request)
            if result.status == VoiceResultStatus.READY:
                return result

        return result
