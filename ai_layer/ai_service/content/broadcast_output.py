"""
AI Layer — Broadcast Preparation Interface (Phase 61.5: AI Production
Integration Foundation, TASK 6).

Contract only -- no real streaming/voice/video/scheduling/send logic.
Adapts an already-generated, accepted `ai_layer.ai_service.content.content_schema.
ContentResult` (Phase 61.5 TASK 5) into the shape a future broadcast
layer would consume, per the Director's own decision this phase (see
`docs/PHASE61_5_PRODUCTION_INTEGRATION_AUDIT.md`): Broadcast Foundation
itself (real channel delivery, media, scheduling) is explicitly out of
scope, deferred to a future v0.5 Product Media Layer / Phase 62.x
Owner Broadcast Foundation. This module's only job is the interface
boundary between "AI generated this content" and "a future layer sends
it somewhere" -- it never sends, schedules, or renders anything.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ai_layer.ai_service.content.content_schema import ContentResult


@dataclass(frozen=True)
class BroadcastReadyContent:
    """The one shape a future broadcast layer would receive -- plain data, no channel/delivery logic of its own."""
    content_type: str
    title: str
    body: str
    prepared_at: str
    provider_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_type": self.content_type,
            "title": self.title,
            "body": self.body,
            "prepared_at": self.prepared_at,
            "provider_name": self.provider_name,
        }


def prepare_broadcast(result: ContentResult) -> Optional[BroadcastReadyContent]:
    """
    Never raises: a non-accepted `ContentResult` (every result today,
    per TASK 5's own foundation-only posture -- no `AIService` runtime
    mapping exists yet for any content capability) returns `None`
    rather than fabricating broadcast-ready content from a rejected or
    empty generation.
    """
    if not result.accepted or not result.body:
        return None
    return BroadcastReadyContent(
        content_type=result.content_type, title=result.title, body=result.body,
        prepared_at=result.generated_at, provider_name=result.provider_name,
    )
