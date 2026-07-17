"""
Media Layer — Media Manager (Phase 63.0: Senior Trading AI Foundation,
TASK 5).

Owner-set ENABLED/DISABLED intent per `MediaType`, same shape
`broadcast.provider_manager.BroadcastProviderManager` already
established. `TEXT` starts `ENABLED` (the only media type this
codebase actually produces today, via `ai/content/`/`ai/explanation/`)
-- every other type starts `DISABLED` since no real processing exists
for any of them yet (Rule 3). No TTS/voice/image/video call anywhere
in this class.
"""

from typing import Dict, List, Optional

from media.media_registry import MediaDescriptor, build_media_registry
from media.media_types import MediaType
from core.logger import setup_logger

logger = setup_logger("MediaManager")


class MediaManager:
    def __init__(self) -> None:
        self._descriptors: Dict[MediaType, MediaDescriptor] = {
            d.media_type: d for d in build_media_registry()
        }
        self._enabled: Dict[MediaType, bool] = {
            media_type: (media_type == MediaType.TEXT) for media_type in self._descriptors
        }

    def list_types(self) -> List[MediaType]:
        return list(self._descriptors.keys())

    def descriptor_of(self, media_type: MediaType) -> Optional[MediaDescriptor]:
        return self._descriptors.get(media_type)

    def is_enabled(self, media_type: MediaType) -> bool:
        return self._enabled.get(media_type, False)

    def set_enabled(self, media_type: MediaType, enabled: bool) -> None:
        """Unknown media_type is silently ignored -- same fail-safe posture every other Phase 63.0 manager uses."""
        if media_type not in self._descriptors:
            logger.warning(f"set_enabled called for an unregistered media type: {media_type}")
            return
        self._enabled[media_type] = enabled
        logger.info(f"Media type {media_type.value} enabled set to {enabled}")
