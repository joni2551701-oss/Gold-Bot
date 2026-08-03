"""
AI Layer — Content Model (Phase 63.6, TASK 2).

`ContentMode`, `ContentMetadata`, and `ContentContext` are the three
genuine gaps this phase's Foundation Reuse Audit found
(`docs/PHASE63_6_AUDIT.md`) — `ContentRequest`/`ContentResult`
(`content_schema.py`, Phase 61.5) and `ContentType`
(`content_types.py`, Phase 61.5/63.0) already existed and are reused
as-is. Every field here is primitive, enum, or the new
`ContentMetadata` -- no `DecisionResult`, `RiskResult`, `Trade`,
`Order`, or `Position` anywhere.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

from ai_layer.ai_service.content.content_type_vocabulary import ContentType


class ContentMode(Enum):
    GENERAL = "GENERAL"
    MARKET = "MARKET"
    EDUCATION = "EDUCATION"


@dataclass(frozen=True)
class ContentMetadata:
    category: str = ""
    language: str = "en"
    priority: int = 0
    tags: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class ContentContext:
    """
    `audience`/`tone`/`purpose` are free-text fields a caller sets
    directly, or that `content_adapters.py`'s integration functions
    derive from an upstream `ExplanationOutput`/`ConversationContext`
    -- never an embedded object from either package.
    """
    content_type: ContentType
    mode: ContentMode
    audience: str = ""
    tone: str = ""
    purpose: str = ""
    metadata: ContentMetadata = field(default_factory=ContentMetadata)
