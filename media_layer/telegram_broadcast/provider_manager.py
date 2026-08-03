"""
Broadcast Layer — Provider Manager (Phase 63.0: Senior Trading AI
Foundation, TASK 4; extended Phase 63.8: AI Broadcast Intelligence
Foundation, TASK 3).

Same "static catalog + Owner-set status" shape
`ai.providers.provider_manager.ProviderManager` already established
for AI providers (Rule 8 — reuse the pattern, not the code, since this
manages channel *intent*, not AI vendors). Every provider starts
`DISABLED` — no channel is enabled until an Owner explicitly turns one
on via a future, separately-approved wiring of `/broadcast_enable`.
No network client, no SDK import (Rule 2).

Phase 63.8 added `TELEGRAM`/`MINI_APP` descriptors (Article 9 --
LOCKed since Phase 63.0, additive-only) -- both start `DISABLED`, same
as every other provider.
"""

from typing import Dict, List, Optional

from media_layer.telegram_broadcast.models import BroadcastProviderDescriptor, BroadcastProviderStatus, BroadcastProviderType
from core_layer.logger.logger import setup_logger

logger = setup_logger("BroadcastProviderManager")


def build_broadcast_provider_registry() -> List[BroadcastProviderDescriptor]:
    """Never raises. One descriptor per BroadcastProviderType -- the fixed catalog, Phase 63.0's original six plus Phase 63.8's TELEGRAM/MINI_APP, no more, no fewer."""
    return [
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.YOUTUBE, name="youtube", description="YouTube Live (no real API client this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.OBS, name="obs", description="OBS Studio integration (no real connection this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.RTMP, name="rtmp", description="Generic RTMP endpoint (no real stream this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.TWITCH, name="twitch", description="Twitch (no real API client this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.KICK, name="kick", description="Kick (no real API client this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.CUSTOM, name="custom", description="Owner-defined custom endpoint (no real delivery this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.TELEGRAM, name="telegram", description="GoldBot's own Telegram channel (no real delivery this phase)."),
        BroadcastProviderDescriptor(provider_type=BroadcastProviderType.MINI_APP, name="mini_app", description="Telegram Mini App surface (no real delivery this phase)."),
    ]


class BroadcastProviderManager:
    def __init__(self) -> None:
        self._descriptors: Dict[str, BroadcastProviderDescriptor] = {
            d.name: d for d in build_broadcast_provider_registry()
        }
        self._status: Dict[str, BroadcastProviderStatus] = {
            name: BroadcastProviderStatus.DISABLED for name in self._descriptors
        }

    def list_providers(self) -> List[str]:
        return list(self._descriptors.keys())

    def descriptor_of(self, name: str) -> Optional[BroadcastProviderDescriptor]:
        return self._descriptors.get(name)

    def status_of(self, name: str) -> Optional[BroadcastProviderStatus]:
        return self._status.get(name)

    def set_status(self, name: str, status: BroadcastProviderStatus) -> None:
        """Unknown `name` is silently ignored, same fail-safe posture ai.providers.provider_manager.ProviderManager.set_status() already uses."""
        if name not in self._descriptors:
            logger.warning(f"set_status called for an unregistered broadcast provider: {name}")
            return
        self._status[name] = status
        logger.info(f"Broadcast provider {name} status set to {status.value}")

    def is_enabled(self, name: str) -> bool:
        return self._status.get(name) == BroadcastProviderStatus.ENABLED
