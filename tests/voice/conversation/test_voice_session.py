"""Phase 65.2 TASK 7/8 — voice/session/: VoiceSession + VoiceSessionManager."""

from voice.session.manager import VoiceSessionManager
from voice.session.models import VoiceSession


def test_voice_session_defaults():
    session = VoiceSession(session_id="s1", user_id="u1", voice_profile_name="Senior")
    assert session.language == "en"
    assert session.conversation_session_id is None
    assert session.created_at is None


def test_voice_session_is_mutable():
    session = VoiceSession(session_id="s1", user_id="u1", voice_profile_name="Senior")
    session.voice_profile_name = "Seniorita"
    assert session.voice_profile_name == "Seniorita"


def test_create_session_with_known_profile_succeeds():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    assert session is not None
    assert session.voice_profile_name == "Senior"
    assert session.user_id == "u1"


def test_create_session_with_unknown_profile_returns_none():
    manager = VoiceSessionManager()
    assert manager.create_session("u1", "NoSuchProfile") is None


def test_get_session_returns_created_session():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    assert manager.get_session(session.session_id) is session


def test_get_session_unknown_returns_none():
    manager = VoiceSessionManager()
    assert manager.get_session("unknown-id") is None


def test_end_session_removes_it():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    manager.end_session(session.session_id)
    assert manager.get_session(session.session_id) is None


def test_end_session_unknown_id_never_raises():
    manager = VoiceSessionManager()
    manager.end_session("unknown-id")


def test_set_voice_profile_valid_profile_succeeds():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    assert manager.set_voice_profile(session.session_id, "Seniorita") is True
    assert manager.get_session(session.session_id).voice_profile_name == "Seniorita"


def test_set_voice_profile_unknown_profile_fails_without_mutating():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    assert manager.set_voice_profile(session.session_id, "NoSuchProfile") is False
    assert manager.get_session(session.session_id).voice_profile_name == "Senior"


def test_set_voice_profile_unknown_session_returns_false():
    manager = VoiceSessionManager()
    assert manager.set_voice_profile("unknown-id", "Senior") is False


def test_link_conversation_session_sets_pointer():
    manager = VoiceSessionManager()
    session = manager.create_session("u1", "Senior")
    assert manager.link_conversation_session(session.session_id, "conv-123") is True
    assert manager.get_session(session.session_id).conversation_session_id == "conv-123"


def test_link_conversation_session_unknown_session_returns_false():
    manager = VoiceSessionManager()
    assert manager.link_conversation_session("unknown-id", "conv-123") is False


def test_voice_session_never_carries_a_persona_field():
    """Phase 65.2 TASK 8 regression guard: VoiceSession selects an existing VoiceProfile by name only -- no Persona-linkage field of any kind."""
    field_names = {f for f in VoiceSession.__dataclass_fields__}
    assert "persona" not in field_names
    assert "persona_name" not in field_names
