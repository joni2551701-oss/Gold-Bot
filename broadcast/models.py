"""
Broadcast Layer — Data Models (Phase 63.0: Senior Trading AI
Foundation, TASK 4; extended Phase 63.8: AI Broadcast Intelligence
Foundation, TASK 1/3/4).

Pure data. No network client, no channel SDK, no streaming library
import anywhere in this package (Rule 2 — no YouTube API/OBS/RTMP/
socket/video/stream). `BroadcastRequest` composes
`ai.content.broadcast_output.BroadcastReadyContent` (Phase 61.5 TASK 6)
as its content input rather than re-declaring a content shape (Module
Reuse Principle).

Phase 63.8 additions (all additive, Article 9 -- LOCKed since Phase
63.0): `BroadcastProviderType` gained `TELEGRAM`/`MINI_APP`;
`BroadcastTrigger` gained one new optional field, `trigger_type`, and
its own new `BroadcastTriggerType` enum; `BroadcastStatus`/
`BroadcastAsset` are the two genuine new models
`docs/PHASE63_8_AUDIT.md`'s Foundation Reuse Audit found -- no
`BroadcastType` enum was created (see that audit's own naming
resolution: `ai.content.content_types.ContentType`, already the type
`BroadcastTrigger.content_type` references, covers that vocabulary).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from ai.content.broadcast_output import BroadcastReadyContent
from ai.content.content_types import ContentType


class BroadcastProviderType(Enum):
    """The channel types a future broadcast layer may deliver to -- vocabulary only, no client for any of them. TELEGRAM/MINI_APP added Phase 63.8 TASK 3."""
    YOUTUBE = "YOUTUBE"
    OBS = "OBS"
    RTMP = "RTMP"
    TWITCH = "TWITCH"
    KICK = "KICK"
    CUSTOM = "CUSTOM"
    TELEGRAM = "TELEGRAM"
    MINI_APP = "MINI_APP"


class BroadcastProviderStatus(Enum):
    """Owner-set intent only -- ENABLED never means "connected," since no provider has a real connection this phase."""
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


@dataclass(frozen=True)
class BroadcastProviderDescriptor:
    provider_type: BroadcastProviderType
    name: str
    description: str = ""


class BroadcastTriggerType(Enum):
    """Phase 63.8 TASK 4 -- categorizes *why* a trigger would arm, never *what* fires it (nothing fires this phase)."""
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    EVENT = "EVENT"
    MARKET = "MARKET"


@dataclass(frozen=True)
class BroadcastTrigger:
    """
    content_type: which `ai.content.content_types.ContentType` this
        trigger watches for.
    enabled: Owner-set intent -- whether this trigger is armed. Never
        actually fires anything this phase; `TriggerManager.is_armed()`
        only reports this flag back.
    trigger_type: (Phase 63.8) which category of trigger this is --
        pure categorization, `TriggerManager` behavior is identical for
        every value; defaults to `MANUAL`.
    """
    content_type: ContentType
    enabled: bool = False
    description: str = ""
    trigger_type: BroadcastTriggerType = BroadcastTriggerType.MANUAL


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


class BroadcastStatus(Enum):
    """Phase 63.8 TASK 1 -- one `BroadcastAsset`'s own lifecycle state, distinct from `BroadcastProviderStatus` (which is provider-intent, not per-item)."""
    DRAFT = "DRAFT"
    READY = "READY"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class BroadcastAsset:
    """
    Phase 63.8 TASK 1 -- the one tracked, lifecycle-aware object this
    phase's `BroadcastManager` extension operates on. `content_id`/
    `media_id` are free-text reference strings (populated by
    `broadcast_adapter.py`, TASK 6) -- never an embedded `ContentResult`/
    `MediaAsset` object, the same "never carry another package's object
    graph" posture `media/models.py`'s `MediaAsset.content_id` already
    established. `persona_name` is likewise a free-text reference, never
    an embedded `ai.persona.persona.Persona` -- see
    `docs/PHASE63_8_AUDIT.md`'s Persona resolution.
    """
    id: str
    content_id: str
    media_id: str
    broadcast_type: ContentType
    status: BroadcastStatus
    persona_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_id": self.content_id,
            "media_id": self.media_id,
            "broadcast_type": self.broadcast_type.value,
            "status": self.status.value,
            "persona_name": self.persona_name,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }
