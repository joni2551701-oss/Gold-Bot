"""Phase 63.5 TASK 4/5/6/7 — ai/conversation/conversation_adapters.py: Knowledge/Memory/Reasoning (upstream, type-only) and Explanation (downstream, dict-only) integration points."""

from datetime import datetime, timezone

from ai.conversation.conversation_adapters import (
    conversation_context_to_explanation_fields,
    knowledge_key_from_entry,
    memory_key_from_entry,
    reasoning_key_from_result,
)
from ai.conversation.models import ConversationContext, ConversationMode
from ai.memory.models import MemoryEntry, MemoryScope, MemoryType
from ai.reasoning.models import ReasoningMode, ReasoningResult, ReasoningType
from ai.session.conversation_state import ConversationTurn
from knowledge.models import KnowledgeCategory, KnowledgeEntry


def test_knowledge_key_from_entry_combines_category_and_key():
    entry = KnowledgeEntry(key="smc.bos", category=KnowledgeCategory.SMC, title="BOS", summary="s")
    assert knowledge_key_from_entry(entry) == "SMC:smc.bos"


def test_memory_key_from_entry_combines_scope_and_key():
    entry = MemoryEntry(key="market.cpi_last", scope=MemoryScope.MARKET, memory_type=MemoryType.SHORT_TERM, value="bullish")
    assert memory_key_from_entry(entry) == "MARKET:market.cpi_last"


def test_reasoning_key_from_result_combines_type_and_key():
    result = ReasoningResult(
        key="gold.cpi.prob", mode=ReasoningMode.MARKET, reasoning_type=ReasoningType.PROBABILITY_ESTIMATE, conclusion="c",
    )
    assert reasoning_key_from_result(result) == "PROBABILITY_ESTIMATE:gold.cpi.prob"


def test_conversation_context_to_explanation_fields_joins_recent_messages():
    turns = (
        ConversationTurn(role="user", content="What is a BOS?", at=datetime.now(timezone.utc)),
        ConversationTurn(role="assistant", content="A structural break.", at=datetime.now(timezone.utc)),
    )
    context = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.EDUCATION, recent_messages=turns)

    fields = conversation_context_to_explanation_fields(context)

    assert "user: What is a BOS?" in fields["technical_reason"]
    assert "assistant: A structural break." in fields["technical_reason"]


def test_conversation_context_to_explanation_fields_returns_a_plain_dict():
    context = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.GENERAL)
    fields = conversation_context_to_explanation_fields(context)
    assert isinstance(fields, dict)
    assert set(fields.keys()) == {"technical_reason"}


def test_conversation_adapters_module_never_imports_ai_explanation():
    """The one file this phase's Intelligence Dependency Principle cares most about -- conversation_context_to_explanation_fields() must return a plain dict, never import ai.explanation itself."""
    import ast
    import pathlib

    adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai" / "conversation" / "conversation_adapters.py"
    tree = ast.parse(adapters_file.read_text(), filename=str(adapters_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("ai.explanation"), alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith("ai.explanation"), node.module
