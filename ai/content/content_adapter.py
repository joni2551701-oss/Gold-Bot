"""
AI Layer — AI Content Adapter (Phase 61.5: AI Production Integration
Foundation, TASK 5; extended Phase 63.6: AI Content Intelligence
Foundation, TASK 3).

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

Phase 63.6 added a second, deterministic surface on this same class,
alongside `generate()` (Article 9 -- LOCKed since Phase 61.5,
additive-only): `create()`/`format()`/`preview()`/`validate()`/
`history()`. None of these five call `AIService.ask()` or make any
network call -- per `docs/PHASE63_6_AUDIT.md`'s own finding,
`ContentEngine` already existed as the one real Manager for Content,
so Constitution Article 11 forbade a second, competing class. `generate()`
itself gained one additive line (recording its own result to the new
internal `self._history`) -- its signature, parameters, and return
value are unchanged.
"""

from dataclasses import asdict
from datetime import datetime, timezone
from typing import List, Optional, Sequence

from ai.content.content_schema import ContentRequest, ContentResult
from ai.content.content_types import ContentType, content_title, is_content_capability
from ai.content.models import ContentMetadata
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
        self._history: List[ContentResult] = []

    def generate(self, request: ContentRequest) -> ContentResult:
        """Never raises: an unrecognized (non-content) capability is rejected here, before any AIService.ask() call."""
        generated_at = datetime.now(timezone.utc).isoformat()

        if not is_content_capability(request.capability):
            result = ContentResult(
                accepted=False, content_type=request.capability.value, title=content_title(request.capability),
                body=None, reason=f"{request.capability.value} is not a content-generation capability",
                generated_at=generated_at,
            )
            self._history.append(result)
            return result

        prompt = _build_prompt(request)
        runtime_request = RuntimeRequest(
            capability=request.capability, ai_context=request.ai_context, role=request.role,
            prompt=prompt, telegram_id=request.telegram_id,
        )
        response = self._ai_service.ask(runtime_request)

        result = ContentResult(
            accepted=response.accepted, content_type=request.capability.value, title=content_title(request.capability),
            body=response.content, reason=response.reason, generated_at=generated_at,
            provider_name=response.provider_name, metadata=dict(response.metadata) if response.metadata else None,
        )
        self._history.append(result)
        return result

    # --- Phase 63.6 TASK 3: deterministic surface, additive only ---
    # None of the four methods below call AIService.ask() or make any
    # network call.

    def create(self, content_type: ContentType, title: str, body: str, metadata: Optional[ContentMetadata] = None) -> ContentResult:
        """Builds an accepted ContentResult directly from caller-supplied primitive values -- no AIService call, no fabricated generation."""
        result = ContentResult(
            accepted=True, content_type=content_type.value, title=title, body=body,
            reason="created directly, no AI generation", generated_at=datetime.now(timezone.utc).isoformat(),
            metadata=asdict(metadata) if metadata else None,
        )
        self._history.append(result)
        return result

    def format(self, result: ContentResult) -> str:
        """Deterministic 'Title\\n\\nBody' rendering. Never raises: an unaccepted result with no body renders using its own reason instead."""
        body = result.body if result.body else f"(not generated: {result.reason})"
        return f"{result.title}\n\n{body}"

    def preview(self, result: ContentResult, max_length: int = 280) -> str:
        """Deterministic, length-capped preview of format()'s own output."""
        text = self.format(result)
        return text if len(text) <= max_length else text[: max_length - 1] + "…"

    def validate(self, result: ContentResult) -> bool:
        """Deterministic: True only when accepted and both title/body are non-empty."""
        return bool(result.accepted and result.title and result.body)

    def history(self) -> Sequence[ContentResult]:
        """Every result generate()/create() has produced on this instance, oldest first."""
        return tuple(self._history)
