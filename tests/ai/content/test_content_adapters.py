"""Phase 63.6 TASK 4/5 — ai/content/content_adapters.py: Explanation/Conversation (upstream, type-only) integration points."""

from datetime import datetime, timezone

from ai.content.content_adapters import (
    content_context_from_conversation,
    content_context_from_explanation,
)
from ai.content.content_types import ContentType
from ai.content.models import ContentMode
from ai.conversation.models import ConversationContext, ConversationMode
from ai.explanation.explanation_output import ExplanationOutput
from ai.session.conversation_state import ConversationTurn


def _explanation_output(summary="Gold remains bullish.", language="uz"):
    return ExplanationOutput(
        title="Gold Outlook", summary=summary, body="Full explanation body.",
        risk_note="Markets can move against any analysis.", invalidation="if price closes below X",
        confidence=0.7, language=language,
    )


def test_content_context_from_explanation_reads_summary_and_language():
    output = _explanation_output()

    context = content_context_from_explanation(output)

    assert context.purpose == "Gold remains bullish."
    assert context.metadata.language == "uz"
    assert context.content_type is ContentType.EXPLANATION
    assert context.mode is ContentMode.GENERAL


def test_content_context_from_explanation_defaults_language_when_missing():
    output = _explanation_output(language="")
    context = content_context_from_explanation(output)
    assert context.metadata.language == "en"


def test_content_context_from_explanation_accepts_explicit_content_type_and_mode():
    output = _explanation_output()
    context = content_context_from_explanation(output, content_type=ContentType.EDUCATION, mode=ContentMode.EDUCATION)
    assert context.content_type is ContentType.EDUCATION
    assert context.mode is ContentMode.EDUCATION


def test_content_context_from_conversation_joins_recent_messages():
    turns = (
        ConversationTurn(role="user", content="What is a BOS?", at=datetime.now(timezone.utc)),
        ConversationTurn(role="assistant", content="A structural break.", at=datetime.now(timezone.utc)),
    )
    context_in = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.EDUCATION, recent_messages=turns)

    context = content_context_from_conversation(context_in)

    assert "user: What is a BOS?" in context.purpose
    assert "assistant: A structural break." in context.purpose
    assert context.content_type is ContentType.EDUCATION
    assert context.mode is ContentMode.EDUCATION


def test_content_context_from_conversation_maps_market_mode():
    context_in = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.MARKET)
    context = content_context_from_conversation(context_in)
    assert context.mode is ContentMode.MARKET


def test_content_context_from_conversation_accepts_explicit_content_type():
    context_in = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.GENERAL)
    context = content_context_from_conversation(context_in, content_type=ContentType.WEEKLY_OUTLOOK)
    assert context.content_type is ContentType.WEEKLY_OUTLOOK


def test_content_adapters_module_never_imports_translation_media_or_broadcast():
    """Per the Intelligence Dependency Principle, ai/content/ may read ai.explanation/ai.conversation (upstream) but must never import translation/media/broadcast (downstream)."""
    import ast
    import pathlib

    adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai" / "content" / "content_adapters.py"
    tree = ast.parse(adapters_file.read_text(), filename=str(adapters_file))
    forbidden_prefixes = ("translation", "media", "broadcast")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith(forbidden_prefixes), alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith(forbidden_prefixes), node.module
