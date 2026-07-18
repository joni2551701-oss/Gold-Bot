"""
Media Layer — Content Integration Adapter (Phase 63.7, TASK 4).

One pure function reading `ai/content/`'s own already-public
`ContentResult` fields into a `MediaAsset` via `MediaManager.create_asset()`
-- never touches `ContentEngine`'s internal state. Per the Intelligence
Dependency Principle (Director Policy, `docs/policies/DIRECTOR_POLICY.md`),
`ai/content/` sits immediately upstream of `media/` in the Official
Intelligence Pipeline, so reading its contract is allowed -- `media/`
never imports `translation/` or `broadcast/` (both downstream/parallel).

`ContentResult` has no unique id field (Phase 61.5, LOCKed) -- its own
`content_type` string (e.g. "AI_MARKET_REPORT") is the closest stable
reference it exposes, so that is what populates `MediaAsset.content_id`
here.
"""

from typing import Optional

from ai.content.content_schema import ContentResult
from media.media_manager import MediaManager
from media.media_types import MediaType
from media.models import MediaAsset


def content_result_to_media_asset(
    result: ContentResult,
    manager: MediaManager,
    media_type: MediaType = MediaType.TEXT,
) -> Optional[MediaAsset]:
    """Never raises: a non-accepted ContentResult (every result today, per Phase 61.5's own foundation-only posture -- no AIService runtime mapping exists yet for any content capability) returns None rather than fabricating a media asset from a rejected or empty generation."""
    if not result.accepted or not result.body:
        return None
    return manager.create_asset(
        content_id=result.content_type,
        media_type=media_type,
        title=result.title,
        description=result.body,
        metadata=dict(result.metadata) if result.metadata else None,
    )
