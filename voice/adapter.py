"""
Voice Layer — Content/Media/Broadcast/Conversation Integration Adapter
(Phase 65.0 TASK 7: Content; extended Phase 65.1 TASK 9: Media,
Broadcast, Conversation).

Four pure functions, each reading one upstream package's own
already-public fields into a `VoiceRequest` via `VoiceManager` --
never touching any upstream engine's internal state. Mirrors
`media/media_adapter.py`'s `content_result_to_media_asset()` shape
exactly, applied to three more upstream types this phase.

Per the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`), extended this phase per this
brief's own pipeline diagram (`Content -> Media -> Broadcast -> Voice
Narration`) to place Voice as the terminal narrating layer downstream
of Content, Media, Broadcast, and Conversation. Phase 65.0's own audit
explicitly deferred `media`/`broadcast` imports "to a future phase" --
`docs/PHASE65_1_AUDIT.md`'s own Dependency Compliance section is that
deferral being exercised, not a violation: nothing in `media/`,
`broadcast/`, or `ai/conversation/` imports `voice/` back, so the
dependency still flows one direction only.

`ContentResult` has no unique id field (Phase 61.5, LOCKed) -- its own
`content_type` string is the closest stable reference it exposes, same
choice `media/media_adapter.py` already made for `MediaAsset.content_id`.
"""

from typing import Optional

from ai.content.content_schema import ContentResult
from ai.session.conversation_state import ConversationTurn
from broadcast.models import BroadcastAsset, BroadcastStatus
from media.models import MediaAsset, MediaAssetStatus
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


def media_asset_to_voice_request(
    asset: MediaAsset,
    manager: VoiceManager,
    profile_name: str,
    provider_type: VoiceProviderType,
    settings: Optional[VoiceSettings] = None,
) -> Optional[VoiceRequest]:
    """Never raises: a non-READY or empty-description MediaAsset, or an unknown profile_name/provider_type, returns None. `asset.description` is the closest thing to narratable text a MediaAsset carries (Phase 63.7, LOCKed) -- `asset.title` is not used as the narration body, only as a future caller's own concern."""
    if asset.status != MediaAssetStatus.READY or not asset.description:
        return None
    if manager.get_profile(profile_name) is None or manager.get_provider(provider_type) is None:
        return None
    return VoiceRequest(
        id=asset.id,
        profile_name=profile_name,
        provider_type=provider_type,
        text=asset.description,
        settings=settings if settings is not None else VoiceSettings(),
        requested_at=asset.created_at,
    )


def broadcast_asset_to_voice_request(
    asset: BroadcastAsset,
    text: str,
    manager: VoiceManager,
    profile_name: str,
    provider_type: VoiceProviderType,
    settings: Optional[VoiceSettings] = None,
) -> Optional[VoiceRequest]:
    """
    Never raises: a non-READY/PUBLISHED BroadcastAsset, an empty
    `text`, or an unknown profile_name/provider_type returns None.
    `BroadcastAsset` (Phase 63.8, LOCKed) carries no narration text of
    its own -- only free-text `content_id`/`media_id` references (see
    its own docstring's "never carry another package's object graph"
    posture) -- so `text` is an explicit parameter here rather than a
    fabricated read from a field that does not exist.
    """
    if asset.status not in (BroadcastStatus.READY, BroadcastStatus.PUBLISHED) or not text:
        return None
    if manager.get_profile(profile_name) is None or manager.get_provider(provider_type) is None:
        return None
    return VoiceRequest(
        id=asset.id,
        profile_name=profile_name,
        provider_type=provider_type,
        text=text,
        settings=settings if settings is not None else VoiceSettings(),
        requested_at=asset.created_at,
    )


def conversation_turn_to_voice_request(
    turn: ConversationTurn,
    manager: VoiceManager,
    profile_name: str,
    provider_type: VoiceProviderType,
    settings: Optional[VoiceSettings] = None,
) -> Optional[VoiceRequest]:
    """Never raises: a user turn (never narrate the user's own message), an empty-content turn, or an unknown profile_name/provider_type returns None. `ConversationTurn` (Phase 61.0, LOCKed) has no id field of its own -- `turn.at`'s own ISO timestamp is the closest stable reference it exposes."""
    if turn.role != "assistant" or not turn.content:
        return None
    if manager.get_profile(profile_name) is None or manager.get_provider(provider_type) is None:
        return None
    return VoiceRequest(
        id=turn.at.isoformat(),
        profile_name=profile_name,
        provider_type=provider_type,
        text=turn.content,
        settings=settings if settings is not None else VoiceSettings(),
        requested_at=turn.at.isoformat(),
    )
