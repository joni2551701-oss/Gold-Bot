"""
Media Layer — Media Domain Model (Phase 63.7, TASK 1).

`MediaAsset`/`MediaAssetStatus` are the one genuine gap this phase's
Foundation Reuse Audit found (`docs/PHASE63_7_AUDIT.md`) — `MediaType`
(`media_types.py`) and `MediaDescriptor`/`build_media_registry()`
(`media_registry.py`, both Phase 63.0) already existed and are reused
as-is. Every field here is primitive, enum, or a plain dict — no
`ContentResult`, `DecisionResult`, `RiskResult`, `Trade`, `Order`, or
`Position` anywhere.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from media.media_types import MediaType


class MediaAssetStatus(Enum):
    PENDING = "PENDING"
    READY = "READY"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class MediaAsset:
    """
    `content_id` is a free-text reference to whatever upstream Content
    result this asset represents (populated by `media_adapter.py`,
    TASK 4) — never an embedded `ContentResult` object; `media/` never
    carries another package's object graph, the same posture
    `ai/conversation/models.py`'s `ConversationContext` already
    established for `knowledge_keys`/`memory_keys`/`reasoning_keys`.
    """
    id: str
    content_id: str
    media_type: MediaType
    status: MediaAssetStatus
    title: str
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_id": self.content_id,
            "media_type": self.media_type.value,
            "status": self.status.value,
            "title": self.title,
            "description": self.description,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }
