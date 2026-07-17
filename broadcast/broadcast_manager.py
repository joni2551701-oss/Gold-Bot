"""
Broadcast Layer — Broadcast Manager (Phase 63.0: Senior Trading AI
Foundation, TASK 4).

Composes `BroadcastProviderManager` + `BroadcastTriggerManager` into
the one decision a future delivery layer would need -- "is there
anywhere and anything armed to send this to right now?" `prepare()`
only ever builds a `BroadcastRequest` value; it never sends one
anywhere. No network call, no SDK, no streaming library import
anywhere in this class (Rule 2).
"""

from datetime import datetime, timezone
from typing import Optional

from ai.content.broadcast_output import BroadcastReadyContent
from ai.content.content_types import ContentType
from broadcast.models import BroadcastRequest
from broadcast.provider_manager import BroadcastProviderManager
from broadcast.trigger_manager import BroadcastTriggerManager


class BroadcastManager:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager."""

    def __init__(
        self,
        provider_manager: Optional[BroadcastProviderManager] = None,
        trigger_manager: Optional[BroadcastTriggerManager] = None,
    ) -> None:
        self._provider_manager = provider_manager or BroadcastProviderManager()
        self._trigger_manager = trigger_manager or BroadcastTriggerManager()

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
