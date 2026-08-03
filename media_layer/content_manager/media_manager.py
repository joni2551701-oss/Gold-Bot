"""
Media Layer — Media Manager (Phase 63.0: Senior Trading AI Foundation,
TASK 5; extended Phase 63.7: AI Media Intelligence Foundation, TASK 3).

Owner-set ENABLED/DISABLED intent per `MediaType`, same shape
`media_layer.telegram_broadcast.provider_manager.BroadcastProviderManager` already
established. `TEXT` starts `ENABLED` (the only media type this
codebase actually produces today, via `ai/content/`/`ai/explanation/`)
-- every other type starts `DISABLED` since no real processing exists
for any of them yet (Rule 3). No TTS/voice/image/video call anywhere
in this class.

Phase 63.7 added a second, deterministic surface on this same class,
alongside the original `list_types()`/`descriptor_of()`/`is_enabled()`/
`set_enabled()` (Article 9 -- LOCKed since Phase 63.0, additive-only):
`create_asset()`/`validate_asset()`/`prepare_asset()`/`get_asset()`.
Per `docs/PHASE63_7_AUDIT.md`'s own finding, `MediaManager` already
existed as the one real Manager for Media, so Constitution Article 11
forbade a second, competing class. None of the four new methods
render, upload, publish, or call any external API -- they only track
`MediaAsset` state in memory.
"""

from dataclasses import replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from media_layer.content_manager.media_registry import MediaDescriptor, build_media_registry
from media_layer.content_manager.media_types import MediaType
from media_layer.content_manager.models import MediaAsset, MediaAssetStatus
from core_layer.logger.logger import setup_logger

logger = setup_logger("MediaManager")


class MediaManager:
    def __init__(self) -> None:
        self._descriptors: Dict[MediaType, MediaDescriptor] = {
            d.media_type: d for d in build_media_registry()
        }
        self._enabled: Dict[MediaType, bool] = {
            media_type: (media_type == MediaType.TEXT) for media_type in self._descriptors
        }
        self._assets: Dict[str, MediaAsset] = {}

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

    # --- Phase 63.7 TASK 3: deterministic asset surface, additive only ---
    # None of the four methods below render, upload, publish, or call
    # any external API -- MediaAsset state tracking only.

    def create_asset(
        self,
        content_id: str,
        media_type: MediaType,
        title: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MediaAsset:
        """Builds a PENDING MediaAsset directly from caller-supplied primitive values -- no rendering, no external call."""
        asset = MediaAsset(
            id=str(uuid4()), content_id=content_id, media_type=media_type,
            status=MediaAssetStatus.PENDING, title=title, description=description,
            metadata=dict(metadata) if metadata else {},
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._assets[asset.id] = asset
        return asset

    def validate_asset(self, asset: MediaAsset) -> bool:
        """Deterministic: True only when the asset's media_type is enabled and its title is non-empty."""
        return bool(self.is_enabled(asset.media_type) and asset.title)

    def prepare_asset(self, asset: MediaAsset) -> MediaAsset:
        """Never raises: transitions to READY when validate_asset() passes, REJECTED otherwise. MediaAsset is frozen, so this returns (and stores) a new instance."""
        new_status = MediaAssetStatus.READY if self.validate_asset(asset) else MediaAssetStatus.REJECTED
        updated = replace(asset, status=new_status)
        self._assets[updated.id] = updated
        return updated

    def get_asset(self, asset_id: str) -> Optional[MediaAsset]:
        return self._assets.get(asset_id)
