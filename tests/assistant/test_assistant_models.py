from datetime import datetime, timezone

from assistant.models import AssistantProfile


def test_assistant_profile_required_fields():
    profile = AssistantProfile(assistant_id="a1", user_id="u1", selected_identity="Senior")
    assert profile.assistant_id == "a1"
    assert profile.user_id == "u1"
    assert profile.selected_identity == "Senior"


def test_assistant_profile_defaults():
    profile = AssistantProfile(assistant_id="a1", user_id="u1", selected_identity="Senior")
    assert profile.selected_voice is None
    assert profile.selected_language == "en"
    assert profile.timezone == "UTC"
    assert profile.created_at is None
    assert profile.updated_at is None


def test_assistant_profile_is_mutable():
    profile = AssistantProfile(assistant_id="a1", user_id="u1", selected_identity="Senior")
    profile.selected_identity = "Seniorita"
    profile.selected_voice = "Narrator"
    now = datetime.now(timezone.utc)
    profile.updated_at = now
    assert profile.selected_identity == "Seniorita"
    assert profile.selected_voice == "Narrator"
    assert profile.updated_at == now


def test_assistant_profile_has_no_provider_field():
    """TASK 8: Provider: Hidden -- enforced by this field never existing."""
    field_names = set(AssistantProfile.__dataclass_fields__.keys())
    assert "provider" not in field_names
    assert "voice_provider" not in field_names


def test_assistant_profile_user_id_and_assistant_id_are_distinct_fields():
    """TASK 6: memory ownership must key by user_id, never assistant_id -- both fields must independently exist."""
    field_names = set(AssistantProfile.__dataclass_fields__.keys())
    assert "user_id" in field_names
    assert "assistant_id" in field_names
