"""
Broadcast Layer — Trigger Manager (Phase 63.0: Senior Trading AI
Foundation, TASK 4).

In-memory registry of `BroadcastTrigger`s -- one per
`ai.content_types.ContentType`, Owner-armed intent only.
`is_armed()` never fires anything; it is a read-only check a future
delivery loop (not this phase) would consult before acting.
"""

from typing import Dict, List, Optional

from ai.content_types import ContentType
from media_layer.telegram_broadcast.models import BroadcastTrigger
from core_layer.logger.logger import setup_logger

logger = setup_logger("BroadcastTriggerManager")


class BroadcastTriggerManager:
    """Every ContentType starts with no trigger registered -- disarmed by default, same "nothing happens until an Owner says so" posture BroadcastProviderManager already uses."""

    def __init__(self) -> None:
        self._triggers: Dict[ContentType, BroadcastTrigger] = {}

    def register(self, trigger: BroadcastTrigger) -> None:
        self._triggers[trigger.content_type] = trigger
        logger.info(f"Broadcast trigger registered: content_type={trigger.content_type.value} enabled={trigger.enabled}")

    def get(self, content_type: ContentType) -> Optional[BroadcastTrigger]:
        return self._triggers.get(content_type)

    def is_armed(self, content_type: ContentType) -> bool:
        """Never raises: an unregistered content_type is disarmed by definition."""
        trigger = self._triggers.get(content_type)
        return trigger is not None and trigger.enabled

    def all(self) -> List[BroadcastTrigger]:
        return list(self._triggers.values())
