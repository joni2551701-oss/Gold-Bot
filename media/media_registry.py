"""
Media Layer — Media Registry (Phase 63.0: Senior Trading AI
Foundation, TASK 5).

Static catalog, same "descriptor + build function" pattern
`ai/providers/provider_registry.py` and `broadcast/provider_manager.py`
already established (Rule 8 — reuse the pattern). No processing logic
of any kind (Rule 3).
"""

from dataclasses import dataclass
from typing import List

from media.media_types import MediaType


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
