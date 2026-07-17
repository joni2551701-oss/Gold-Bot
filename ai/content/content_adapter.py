"""
AI Layer — AI Content Adapter (Phase 61.5: AI Production Integration
Foundation, TASK 5).

`ContentEngine` wraps `ai/runtime/ai_service.py`'s `AIService.ask()`
(unmodified) for the four content-generation capabilities -- no new
provider call, no new orchestration, same pattern
`ai/explanation/explanation_engine.py`'s `ExplanationEngine` already
established (Phase 61.3 TASK 7) for EXPLANATION/SUMMARY/EDUCATION.

Foundation only: none of `AI_MARKET_REPORT`/`AI_WEEKLY_OUTLOOK`/
`AI_NEWS_ANALYSIS`/`AI_SCRIPT_GENERATION` has a runtime method mapping
in `ai/runtime/ai_service.py`'s `_CAPABILITY_METHOD` yet (same
pre-existing gap `SUMMARY`/`EDUCATION`/`MEMORY`/`TOOL_CALLING`/`VIDEO`/
`DOCUMENT` already have) -- `generate()` below always receives a
cleanly rejected `RuntimeResponse` ("no runtime method mapping yet")
until a future phase adds that mapping. This module builds the
correctly-shaped request/response contract now; it never fabricates a
generated answer, never touches `database/`/`telegram/`, and never
produces or influences a trading signal.
"""

from datetime import datetime, timezone
from typing import Optional

from ai.content.content_schema import ContentRequest, ContentResult
from ai.content.content_types import content_title, is_content_capability
from ai.runtime.ai_service import AIService
from ai.runtime.runtime_request import RuntimeRequest


def _build_prompt(request: ContentRequest) -> str:
    title = content_title(request.capability)
    if request.topic:
        return f"Generate a {title} for XAUUSD (Gold). Focus: {request.topic}."
    return f"Generate a {title} for XAUUSD (Gold)."


class ContentEngine:
    """Every dependency is injectable, same convention as `AIService`/`ExplanationEngine`/`ConversationEngine`."""

    def __init__(self, ai_service: Optional[AIService] = None) -> None:
        self._ai_service = ai_service or AIService()

    def generate(self, request: ContentRequest) -> ContentResult:
        """Never raises: an unrecognized (non-content) capability is rejected here, before any AIService.ask() call."""
        generated_at = datetime.now(timezone.utc).isoformat()

        if not is_content_capability(request.capability):
            return ContentResult(
                accepted=False, content_type=request.capability.value, title=content_title(request.capability),
                body=None, reason=f"{request.capability.value} is not a content-generation capability",
                generated_at=generated_at,
            )

        prompt = _build_prompt(request)
        runtime_request = RuntimeRequest(
            capability=request.capability, ai_context=request.ai_context, role=request.role,
            prompt=prompt, telegram_id=request.telegram_id,
        )
        response = self._ai_service.ask(runtime_request)

        return ContentResult(
            accepted=response.accepted, content_type=request.capability.value, title=content_title(request.capability),
            body=response.content, reason=response.reason, generated_at=generated_at,
            provider_name=response.provider_name, metadata=dict(response.metadata) if response.metadata else None,
        )
