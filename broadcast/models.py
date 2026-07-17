"""
Broadcast Layer — Data Models (Phase 63.0: Senior Trading AI
Foundation, TASK 4).

Pure data. No network client, no channel SDK, no streaming library
import anywhere in this package (Rule 2 — no YouTube API/OBS/RTMP/
socket/video/stream). `BroadcastRequest` composes
`ai.content.broadcast_output.BroadcastReadyContent` (Phase 61.5 TASK 6)
as its content input rather than re-declaring a content shape (Module
Reuse Principle).
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ai.content.broadcast_output import BroadcastReadyContent
from ai.content.content_types import ContentType


class BroadcastProviderType(Enum):
    """The channel types a future broadcast layer may deliver to -- vocabulary only, no client for any of them."""
    YOUTUBE = "YOUTUBE"
    OBS = "OBS"
    RTMP = "RTMP"
    TWITCH = "TWITCH"
    KICK = "KICK"
    CUSTOM = "CUSTOM"


class BroadcastProviderStatus(Enum):
    """Owner-set intent only -- ENABLED never means "connected," since no provider has a real connection this phase."""
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


@dataclass(frozen=True)
class BroadcastProviderDescriptor:
    provider_type: BroadcastProviderType
    name: str
    description: str = ""


@dataclass(frozen=True)
class BroadcastTrigger:
    """
    content_type: which `ai.content.content_types.ContentType` this
        trigger watches for.
    enabled: Owner-set intent -- whether this trigger is armed. Never
        actually fires anything this phase; `TriggerManager.is_armed()`
        only reports this flag back.
    """
    content_type: ContentType
    enabled: bool = False
    description: str = ""


@dataclass(frozen=True)
class BroadcastRequest:
    """
    The one shape a future real delivery layer would consume -- built
    by `BroadcastManager.prepare()` below, never sent anywhere this
    phase. `requested_at` records when the request was assembled, not
    when (or whether) anything was ever delivered.
    """
    content: BroadcastReadyContent
    provider_type: BroadcastProviderType
    requested_at: datetime
