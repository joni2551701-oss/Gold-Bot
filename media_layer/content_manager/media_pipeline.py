"""
Media Layer — Media Pipeline Foundation (Phase 63.7, TASK 5).

Composes the two pieces this phase already built --
`media_adapter.content_result_to_media_asset()` (TASK 4) and
`MediaManager.prepare_asset()` (TASK 3) -- into the one-call flow the
brief names:

    ExplanationOutput -> ContentResult -> MediaPreparation -> MediaAsset -> (future provider)

`ExplanationOutput -> ContentResult` is already `ai/content/`'s own
job (`ai/content/content_adapters.py`, Phase 63.6) -- this module never
duplicates that step, it starts from an already-produced
`ContentResult`. No provider call, no rendering, no upload -- the
"future provider" step is deliberately absent this phase (Rule: no
real media generation).
"""

from typing import Optional

from ai.content.content_schema import ContentResult
from media_layer.content_manager.media_adapter import content_result_to_media_asset
from media_layer.content_manager.media_manager import MediaManager
from media_layer.content_manager.media_types import MediaType
from media_layer.content_manager.models import MediaAsset


def prepare_media_from_content(
    result: ContentResult,
    manager: MediaManager,
    media_type: MediaType = MediaType.TEXT,
) -> Optional[MediaAsset]:
    """Never raises: a non-accepted ContentResult returns None (same posture content_result_to_media_asset() already has) -- otherwise returns the asset after validate/prepare (READY or REJECTED, never left PENDING)."""
    asset = content_result_to_media_asset(result, manager, media_type=media_type)
    if asset is None:
        return None
    return manager.prepare_asset(asset)
