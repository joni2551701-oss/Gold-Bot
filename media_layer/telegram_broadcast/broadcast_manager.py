"""
Broadcast Layer — Broadcast Manager (Phase 63.0: Senior Trading AI
Foundation, TASK 4; extended Phase 63.8: AI Broadcast Intelligence
Foundation, TASK 2).

Composes `BroadcastProviderManager` + `BroadcastTriggerManager` into
the one decision a future delivery layer would need -- "is there
anywhere and anything armed to send this to right now?" `prepare()`
only ever builds a `BroadcastRequest` value; it never sends one
anywhere. No network call, no SDK, no streaming library import
anywhere in this class (Rule 2).

Phase 63.8 added a second, deterministic surface on this same class,
alongside `would_broadcast()`/`prepare()` (Article 9 -- LOCKed since
Phase 63.0, additive-only): `create_broadcast()`/`validate_broadcast()`/
`prepare_broadcast()`/`get_broadcast()`/`list_broadcasts()`. Per
`docs/PHASE63_8_AUDIT.md`'s own finding, `BroadcastManager` already
existed as the one real Manager for Broadcast, so Constitution
Article 11 forbade a second, competing class. None of the five new
methods send anything anywhere -- they only track `BroadcastAsset`
state in memory, the same posture `MediaManager`'s Phase 63.7 asset
surface already established.
"""

from dataclasses import replace
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from ai_layer.ai_service.content.broadcast_output import BroadcastReadyContent
from ai_layer.ai_service.content.content_type_vocabulary import ContentType
from media_layer.telegram_broadcast.models import BroadcastAsset, BroadcastRequest, BroadcastStatus
from media_layer.telegram_broadcast.provider_manager import BroadcastProviderManager
from media_layer.telegram_broadcast.trigger_manager import BroadcastTriggerManager


class BroadcastManager:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager."""

    def __init__(
        self,
        provider_manager: Optional[BroadcastProviderManager] = None,
        trigger_manager: Optional[BroadcastTriggerManager] = None,
    ) -> None:
        self._provider_manager = provider_manager or BroadcastProviderManager()
        self._trigger_manager = trigger_manager or BroadcastTriggerManager()
        self._assets: Dict[str, BroadcastAsset] = {}

    def would_broadcast(self, content_type: ContentType, provider_name: str) -> bool:
        """Both the trigger for this content_type and the named provider must be Owner-armed/enabled. Never raises: an unknown provider_name reports False."""
        return self._trigger_manager.is_armed(content_type) and self._provider_manager.is_enabled(provider_name)

    def prepare(
        self, content: BroadcastReadyContent, content_type: ContentType, provider_name: str,
    ) -> Optional[BroadcastRequest]:
        """
        Never sends anything -- builds a `BroadcastRequest` value only
        if `would_broadcast()` says the trigger and provider are both
        armed/enabled, else returns `None`. A future, separately-
        approved delivery layer is the only thing that would ever act
        on this value.
        """
        if not self.would_broadcast(content_type, provider_name):
            return None

        descriptor = self._provider_manager.descriptor_of(provider_name)
        if descriptor is None:
            return None

        return BroadcastRequest(
            content=content, provider_type=descriptor.provider_type,
            requested_at=datetime.now(timezone.utc),
        )

    # --- Phase 63.8 TASK 2: deterministic asset surface, additive only ---
    # None of the five methods below send anything anywhere -- BroadcastAsset
    # state tracking only.

    def create_broadcast(
        self,
        content_id: str,
        media_id: str,
        broadcast_type: ContentType,
        persona_name: Optional[str] = None,
        metadata: Optional[Dict[str, object]] = None,
    ) -> BroadcastAsset:
        """Builds a DRAFT BroadcastAsset directly from caller-supplied primitive values -- no delivery, no external call."""
        asset = BroadcastAsset(
            id=str(uuid4()), content_id=content_id, media_id=media_id,
            broadcast_type=broadcast_type, status=BroadcastStatus.DRAFT,
            persona_name=persona_name, metadata=dict(metadata) if metadata else {},
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._assets[asset.id] = asset
        return asset

    def validate_broadcast(self, asset: BroadcastAsset) -> bool:
        """Deterministic: True only when both content_id and media_id are non-empty -- a broadcast asset with nothing to show is never valid."""
        return bool(asset.content_id and asset.media_id)

    def prepare_broadcast(self, asset: BroadcastAsset) -> BroadcastAsset:
        """Never raises: transitions to READY when validate_broadcast() passes, FAILED otherwise. BroadcastAsset is frozen, so this returns (and stores) a new instance."""
        new_status = BroadcastStatus.READY if self.validate_broadcast(asset) else BroadcastStatus.FAILED
        updated = replace(asset, status=new_status)
        self._assets[updated.id] = updated
        return updated

    def get_broadcast(self, asset_id: str) -> Optional[BroadcastAsset]:
        return self._assets.get(asset_id)

    def list_broadcasts(self) -> List[BroadcastAsset]:
        """Every BroadcastAsset create_broadcast() has produced on this instance, oldest first."""
        return list(self._assets.values())
