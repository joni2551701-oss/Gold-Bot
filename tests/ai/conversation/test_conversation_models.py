"""Phase 63.5 TASK 2 — ai/conversation/models.py: ConversationMode/ConversationContext."""

from datetime import datetime, timezone

from ai.conversation.models import ConversationContext, ConversationMode
from ai.session.conversation_state import ConversationTurn


def test_conversation_context_defaults_are_empty_tuples():
    context = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.GENERAL)
    assert context.recent_messages == ()
    assert context.knowledge_keys == ()
    assert context.memory_keys == ()
    assert context.reasoning_keys == ()


def test_conversation_context_accepts_recent_messages_and_keys():
    turn = ConversationTurn(role="user", content="hi", at=datetime.now(timezone.utc))
    context = ConversationContext(
        session_id="s1", telegram_id="t1", mode=ConversationMode.MARKET,
        recent_messages=(turn,), knowledge_keys=("SMC:smc.bos",),
        memory_keys=("MARKET:market.cpi_last",), reasoning_keys=("PROBABILITY_ESTIMATE:gold.cpi.prob",),
    )
    assert context.recent_messages == (turn,)
    assert context.knowledge_keys == ("SMC:smc.bos",)
    assert context.memory_keys == ("MARKET:market.cpi_last",)
    assert context.reasoning_keys == ("PROBABILITY_ESTIMATE:gold.cpi.prob",)


def test_conversation_context_is_frozen():
    context = ConversationContext(session_id="s1", telegram_id="t1", mode=ConversationMode.GENERAL)
    try:
        context.session_id = "mutated"
        assert False, "ConversationContext should be frozen"
    except AttributeError:
        pass


def test_conversation_mode_has_the_three_brief_named_values():
    assert {m.value for m in ConversationMode} == {"GENERAL", "MARKET", "EDUCATION"}
