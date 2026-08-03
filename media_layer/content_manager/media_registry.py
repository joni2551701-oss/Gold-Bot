"""
Media Layer — Media Registry (Phase 63.0: Senior Trading AI
Foundation, TASK 5; extended Phase 63.7: AI Media Intelligence
Foundation, TASK 2).

Static catalog, same "descriptor + build function" pattern
`ai/providers/provider_registry.py` and `media_layer/telegram_broadcast/provider_manager.py`
already established (Rule 8 — reuse the pattern). No processing logic
of any kind (Rule 3).

Phase 63.7 added `get()`/`exists()` (Article 9 — LOCKed since Phase
63.0, additive-only) — `register()` was deliberately not added: this
catalog is fixed by design (one descriptor per `MediaType` member, no
caller mutates it this phase), so a real `register()` would contradict
this module's own "no processing logic" posture. See
`docs/PHASE63_7_AUDIT.md` for the full naming resolution.
"""

from dataclasses import dataclass
from typing import List, Optional

from media_layer.content_manager.media_types import MediaType


@dataclass(frozen=True)
class MediaDescriptor:
    media_type: MediaType
    name: str
    description: str = ""


def build_media_registry() -> List[MediaDescriptor]:
    """Never raises. One descriptor per MediaType -- the fixed catalog this phase."""
    return [
        MediaDescriptor(media_type=MediaType.TEXT, name="text", description="Plain text output -- already real, produced by ai/content/, ai/explanation/."),
        MediaDescriptor(media_type=MediaType.VOICE, name="voice", description="Voice/TTS output (no synthesis this phase)."),
        MediaDescriptor(media_type=MediaType.IMAGE, name="image", description="Image output (no generation this phase)."),
        MediaDescriptor(media_type=MediaType.VIDEO, name="video", description="Video output (no processing this phase)."),
        MediaDescriptor(media_type=MediaType.LIVE, name="live", description="Live stream output (no streaming this phase)."),
    ]


def get(media_type: MediaType) -> Optional[MediaDescriptor]:
    """Never raises: a media_type with no descriptor (cannot happen today -- every MediaType member has exactly one) returns None."""
    for descriptor in build_media_registry():
        if descriptor.media_type == media_type:
            return descriptor
    return None


def exists(media_type: MediaType) -> bool:
    return get(media_type) is not None
