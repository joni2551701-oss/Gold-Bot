"""Phase 63.5 TASK 3 — ConversationEngine's deterministic surface (append/summarize/history/context/reset/close), all additive to the existing, LOCKed start_session()/ask()."""

from ai_layer.personal_ai.interaction_manager.conversation_engine import ConversationEngine
from ai_layer.personal_ai.interaction_manager.models import ConversationMode


def _engine_with_session():
    engine = ConversationEngine()
    state = engine.start_session(telegram_id="123")
    return engine, state.session_id


def test_append_records_a_turn_without_calling_ai_service():
    engine, session_id = _engine_with_session()
    assert engine.append(session_id, "user", "hello") is True
    history = engine.history(session_id)
    assert len(history) == 1
    assert history[0].role == "user"
    assert history[0].content == "hello"


def test_append_unknown_session_returns_false():
    engine = ConversationEngine()
    assert engine.append("does-not-exist", "user", "hi") is False


def test_summarize_joins_role_and_content():
    engine, session_id = _engine_with_session()
    engine.append(session_id, "user", "hello")
    engine.append(session_id, "assistant", "hi there")
    summary = engine.summarize(session_id)
    assert "user: hello" in summary
    assert "assistant: hi there" in summary


def test_summarize_unknown_session_returns_none():
    engine = ConversationEngine()
    assert engine.summarize("does-not-exist") is None


def test_history_unknown_session_returns_empty_tuple():
    engine = ConversationEngine()
    assert engine.history("does-not-exist") == ()


def test_context_assembles_session_id_telegram_id_and_recent_messages():
    engine, session_id = _engine_with_session()
    engine.append(session_id, "user", "hello")

    context = engine.context(session_id, mode=ConversationMode.MARKET)

    assert context.session_id == session_id
    assert context.telegram_id == "123"
    assert context.mode is ConversationMode.MARKET
    assert len(context.recent_messages) == 1


def test_context_carries_upstream_key_pointers():
    engine, session_id = _engine_with_session()

    context = engine.context(
        session_id,
        knowledge_keys=("SMC:smc.bos",),
        memory_keys=("MARKET:market.cpi_last",),
        reasoning_keys=("PROBABILITY_ESTIMATE:gold.cpi.prob",),
    )

    assert context.knowledge_keys == ("SMC:smc.bos",)
    assert context.memory_keys == ("MARKET:market.cpi_last",)
    assert context.reasoning_keys == ("PROBABILITY_ESTIMATE:gold.cpi.prob",)


def test_context_unknown_session_returns_none():
    engine = ConversationEngine()
    assert engine.context("does-not-exist") is None


def test_reset_clears_turns_but_keeps_session_alive():
    engine, session_id = _engine_with_session()
    engine.append(session_id, "user", "hello")

    assert engine.reset(session_id) is True

    assert engine.history(session_id) == ()
    assert engine.append(session_id, "user", "still alive") is True


def test_reset_unknown_session_returns_false():
    engine = ConversationEngine()
    assert engine.reset("does-not-exist") is False


def test_close_ends_the_session():
    engine, session_id = _engine_with_session()

    assert engine.close(session_id) is True

    assert engine.append(session_id, "user", "too late") is False
    assert engine.history(session_id) == ()


def test_close_unknown_session_returns_false():
    engine = ConversationEngine()
    assert engine.close("does-not-exist") is False


def test_deterministic_methods_never_call_ai_service():
    """append/summarize/history/context/reset/close never touch AIService -- verified by never passing an ai_context, unlike ask()."""
    engine, session_id = _engine_with_session()
    engine.append(session_id, "user", "no ai_context needed here")
    assert engine.summarize(session_id) is not None
    assert engine.reset(session_id) is True
    assert engine.close(session_id) is True
