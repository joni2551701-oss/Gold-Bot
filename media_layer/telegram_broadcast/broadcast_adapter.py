"""
Broadcast Layer — Content/Media/Persona Integration Adapter (Phase
63.8, TASK 6).

One pure function reading `ai/content/`'s `ContentResult`,
`media/`'s `MediaAsset`, and (optionally) `ai/persona/`'s `Persona` --
all their own already-public fields -- into a `BroadcastAsset` via
`BroadcastManager.create_broadcast()`. Never touches `ContentEngine`/
`MediaManager`/`PersonaManager`'s internal state.

Per the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`) and this phase's own Rule 3,
`broadcast/` may read `media/`, `ai/content/`, and `ai/` (type-only) --
it never imports `decision/`/`risk/`/`execution/`/`strategies/`/
`signals/`.

Per `docs/PHASE63_8_AUDIT.md`'s TASK 6 resolution, this adapter's
output *is* `BroadcastAsset` (TASK 1's own model) -- no second,
competing "BroadcastReady" dataclass is declared here;
`ai.content.broadcast_output.BroadcastReadyContent`/`prepare_broadcast()`
(Phase 61.5) remain untouched and continue to exist as the narrower,
Content-only path.
"""

from typing import Optional

from ai.content.content_schema import ContentResult
from ai.content_types import ContentType
from ai.persona.persona import Persona
from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
from media_layer.telegram_broadcast.models import BroadcastAsset
from media_layer.content_manager.models import MediaAsset


def broadcast_asset_from_content_and_media(
    content: ContentResult,
    media: MediaAsset,
    manager: BroadcastManager,
    broadcast_type: Optional[ContentType] = None,
    persona: Optional[Persona] = None,
) -> Optional[BroadcastAsset]:
    """
    Never raises: a non-accepted ContentResult (every result today, per
    Phase 61.5's own foundation-only posture) returns None rather than
    fabricating a broadcast asset from a rejected or empty generation.
    `broadcast_type` defaults to `ContentType.EXPLANATION` when the
    caller doesn't name one -- `content.content_type` is a raw
    `Capability` string (e.g. "AI_MARKET_REPORT"), not itself a
    `ContentType`, so it cannot be inferred automatically.
    """
    if not content.accepted or not content.body:
        return None
    return manager.create_broadcast(
        content_id=content.content_type,
        media_id=media.id,
        broadcast_type=broadcast_type or ContentType.EXPLANATION,
        persona_name=persona.name if persona else None,
        metadata=dict(content.metadata) if content.metadata else None,
    )
