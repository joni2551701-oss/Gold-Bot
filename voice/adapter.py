"""
Voice Layer — Content Integration Adapter (Phase 65.0, TASK 7).

One pure function reading `ai/content/`'s own already-public
`ContentResult` fields into a `VoiceRequest` via `VoiceManager` --
never touches `ContentEngine`'s internal state. Mirrors
`media/media_adapter.py`'s `content_result_to_media_asset()` exactly.
Per the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`), `ai/content/` sits upstream of
`voice/` in the Official Intelligence Pipeline, so reading its
contract is allowed -- `voice/` never imports `media/` or `broadcast/`
this phase (per `docs/PHASE65_0_AUDIT.md`'s own dependency-compliance
decision).

`ContentResult` has no unique id field (Phase 61.5, LOCKed) -- its own
`content_type` string is the closest stable reference it exposes, same
choice `media/media_adapter.py` already made for `MediaAsset.content_id`.
"""

from typing import Optional

from ai.content.content_schema import ContentResult
from voice.manager import VoiceManager
from voice.models import VoiceProviderType, VoiceRequest, VoiceSettings


def content_result_to_voice_request(
    result: ContentResult,
    manager: VoiceManager,
    profile_name: str,
    provider_type: VoiceProviderType,
    settings: Optional[VoiceSettings] = None,
) -> Optional[VoiceRequest]:
    """Never raises: a non-accepted or empty-body ContentResult, or an unknown profile_name/provider_type, returns None rather than fabricating a voice request. Existence is checked here (via `manager`); enablement is VoiceManager.validate()'s own separate job, called by whoever consumes the returned request."""
    if not result.accepted or not result.body:
        return None
    if manager.get_profile(profile_name) is None or manager.get_provider(provider_type) is None:
        return None
    return VoiceRequest(
        id=result.content_type,
        profile_name=profile_name,
        provider_type=provider_type,
        text=result.body,
        settings=settings if settings is not None else VoiceSettings(),
        requested_at=result.generated_at,
    )
