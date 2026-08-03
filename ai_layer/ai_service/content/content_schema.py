"""
AI Layer — AI Content Schema (Phase 61.5: AI Production Integration
Foundation, TASK 5).

`ContentRequest`/`ContentResult` are the one input/output shape
`ai/content/content_adapter.py`'s `ContentEngine` accepts/returns --
composes already-existing foundation types
(`ai_layer.ai_engine.capabilities.capability.Capability`, `ai_layer.ai_engine.context.context_snapshot.AIContext`,
`ai_layer.ai_service.access.permissions.AIRole`) rather than re-declaring any of them,
same convention `ai/runtime/runtime_request.py`'s `RuntimeRequest`
already established.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.context.context_snapshot import AIContext


@dataclass(frozen=True)
class ContentRequest:
    """
    topic: optional free-text focus for the generated content (e.g. a
        specific news headline for AI_NEWS_ANALYSIS) -- appended to the
        capability's own generated prompt, never used to build a prompt
        on its own.
    telegram_id: optional, carried through to `AIService.ask()`'s own
        audit logging -- never used for anything else.
    """
    capability: Capability
    ai_context: AIContext
    role: AIRole
    topic: Optional[str] = None
    telegram_id: Optional[str] = None


@dataclass(frozen=True)
class ContentResult:
    """
    accepted: False whenever the underlying `AIService.ask()` call was
        rejected (access/capability/no-provider/no-runtime-mapping) --
        `body` is always None when this is False, never a
        partial/fabricated answer, same "never fabricate" convention
        `ai/runtime/runtime_response.py`'s `RuntimeResponse` already
        uses.
    generated_at: ISO-8601 timestamp string, set by
        `ai/content/content_adapter.py` at construction time -- when
        `accepted` is False this is still set (the *attempt* happened
        at this time, even if it produced no content).
    """
    accepted: bool
    content_type: str
    title: str
    body: Optional[str]
    reason: str
    generated_at: str
    provider_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """The JSON-serializable shape a future broadcast/owner-facing consumer reads -- plain dict of this dataclass's own fields, no hidden transformation."""
        return {
            "accepted": self.accepted,
            "content_type": self.content_type,
            "title": self.title,
            "body": self.body,
            "reason": self.reason,
            "generated_at": self.generated_at,
            "provider_name": self.provider_name,
            "metadata": dict(self.metadata) if self.metadata else {},
        }
