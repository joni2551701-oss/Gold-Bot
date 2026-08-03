"""Phase 61.0 TASK 7 — AI Session Foundation: Session != Memory, session is temporary."""

from datetime import datetime, timedelta, timezone

from ai_layer.ai_service.session.context_window import ContextWindow
from ai_layer.ai_service.session.conversation_state import ConversationState
from ai_layer.ai_service.session.session_manager import SessionManager


def test_create_session_returns_a_fresh_conversation_state():
    manager = SessionManager()
    state = manager.create_session(telegram_id="123")
    assert isinstance(state, ConversationState)
    assert state.telegram_id == "123"
    assert state.turns == []


def test_get_session_returns_the_created_session():
    manager = SessionManager()
    created = manager.create_session(telegram_id="123")
    fetched = manager.get_session(created.session_id)
    assert fetched is created


def test_get_session_returns_none_for_unknown_id():
    manager = SessionManager()
    assert manager.get_session("unknown") is None


def test_end_session_removes_it():
    manager = SessionManager()
    state = manager.create_session(telegram_id="123")
    manager.end_session(state.session_id)
    assert manager.get_session(state.session_id) is None


def test_add_turn_updates_last_activity():
    state = ConversationState(session_id="s1", telegram_id="123", created_at=datetime.now(timezone.utc))
    state.add_turn("user", "hello")
    assert len(state.history()) == 1
    assert state.last_activity is not None


def test_session_is_expired_after_ttl():
    manager = SessionManager(ttl=timedelta(minutes=1))
    state = manager.create_session(telegram_id="123")
    future = datetime.now(timezone.utc) + timedelta(minutes=5)
    assert manager.is_expired(state.session_id, now=future) is True


def test_session_is_not_expired_within_ttl():
    manager = SessionManager(ttl=timedelta(minutes=30))
    state = manager.create_session(telegram_id="123")
    assert manager.is_expired(state.session_id, now=datetime.now(timezone.utc)) is False


def test_unknown_session_is_treated_as_expired():
    manager = SessionManager()
    assert manager.is_expired("unknown") is True


def test_purge_expired_removes_only_expired_sessions():
    manager = SessionManager(ttl=timedelta(minutes=1))
    reference_now = datetime.now(timezone.utc)
    old_state = manager.create_session(telegram_id="old")
    fresh_state = manager.create_session(telegram_id="fresh")
    manager._sessions[old_state.session_id].last_activity = reference_now - timedelta(minutes=10)
    manager._sessions[fresh_state.session_id].last_activity = reference_now
    removed = manager.purge_expired(now=reference_now)
    assert removed == 1
    assert manager.get_session(fresh_state.session_id) is not None


def test_context_window_rejects_non_positive_max_turns():
    import pytest
    with pytest.raises(ValueError):
        ContextWindow(max_turns=0)


def test_context_window_trims_to_most_recent_turns():
    state = ConversationState(session_id="s1", telegram_id="123", created_at=datetime.now(timezone.utc))
    for i in range(5):
        state.add_turn("user", f"turn {i}")
    window = ContextWindow(max_turns=2)
    trimmed = window.trim(state.history())
    assert len(trimmed) == 2
    assert trimmed[-1].content == "turn 4"


def test_context_window_returns_all_turns_when_under_limit():
    state = ConversationState(session_id="s1", telegram_id="123", created_at=datetime.now(timezone.utc))
    state.add_turn("user", "hi")
    window = ContextWindow(max_turns=20)
    assert len(window.trim(state.history())) == 1


def test_clear_turns_empties_history_but_keeps_the_session_identity():
    """Phase 63.5 TASK 3 -- clear_turns() is additive (Article 9); add_turn()/history() are unchanged."""
    state = ConversationState(session_id="s1", telegram_id="123", created_at=datetime.now(timezone.utc))
    state.add_turn("user", "hi")
    state.add_turn("assistant", "hello")

    state.clear_turns()

    assert state.history() == ()
    assert state.session_id == "s1"
    assert state.telegram_id == "123"

    state.add_turn("user", "still works")
    assert len(state.history()) == 1
