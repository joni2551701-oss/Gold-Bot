"""
AI Layer — Content Integration Adapters (Phase 63.6, TASK 4/5).

Two pure functions reading an *upstream* package's own already-public
fields into a `ContentContext` -- never a Manager/Engine/Runtime's
internal state. Per the Intelligence Dependency Principle (Director
Policy, `docs/policies/DIRECTOR_POLICY.md`), both `ai/explanation/`
and `ai/conversation/` sit upstream of `ai/content/` in the Official
Intelligence Pipeline, so reading their contracts is allowed --
`ai/content/` never imports `translation/`, `media/`, or `broadcast/`
(all downstream).
"""

from ai.content_types import ContentType
from ai.content.models import ContentContext, ContentMetadata, ContentMode
from ai.conversation.models import ConversationContext, ConversationMode
from ai.explanation.explanation_output import ExplanationOutput

_CONVERSATION_MODE_MAP = {
    ConversationMode.GENERAL: ContentMode.GENERAL,
    ConversationMode.MARKET: ContentMode.MARKET,
    ConversationMode.EDUCATION: ContentMode.EDUCATION,
}


def content_context_from_explanation(
    output: ExplanationOutput,
    content_type: ContentType = ContentType.EXPLANATION,
    mode: ContentMode = ContentMode.GENERAL,
) -> ContentContext:
    """Reads ExplanationOutput's own already-public fields (summary/language) -- never calls ExplanationBuilder."""
    return ContentContext(
        content_type=content_type,
        mode=mode,
        purpose=output.summary or "",
        metadata=ContentMetadata(language=output.language or "en"),
    )


def content_context_from_conversation(
    context: ConversationContext,
    content_type: ContentType = ContentType.EDUCATION,
) -> ContentContext:
    """Reads ConversationContext's own fields (mode/recent_messages) -- never touches ConversationEngine's internal session state."""
    purpose = "; ".join(f"{turn.role}: {turn.content}" for turn in context.recent_messages)
    return ContentContext(
        content_type=content_type,
        mode=_CONVERSATION_MODE_MAP.get(context.mode, ContentMode.GENERAL),
        purpose=purpose,
        metadata=ContentMetadata(),
    )
