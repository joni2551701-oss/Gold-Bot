from datetime import datetime, timezone

from assistant.models import AssistantRuntime


def test_assistant_runtime_required_fields():
    runtime = AssistantRuntime(session_id="s1", assistant_id="a1")
    assert runtime.session_id == "s1"
    assert runtime.assistant_id == "a1"


def test_assistant_runtime_defaults():
    runtime = AssistantRuntime(session_id="s1", assistant_id="a1")
    assert runtime.started_at is None
    assert runtime.updated_at is None
    assert runtime.active is True
    assert runtime.conversation_id is None


def test_assistant_runtime_is_mutable():
    runtime = AssistantRuntime(session_id="s1", assistant_id="a1")
    runtime.active = False
    now = datetime.now(timezone.utc)
    runtime.updated_at = now
    runtime.conversation_id = "conv-1"
    assert runtime.active is False
    assert runtime.updated_at == now
    assert runtime.conversation_id == "conv-1"


def test_assistant_runtime_session_id_and_assistant_id_are_distinct_fields():
    field_names = set(AssistantRuntime.__dataclass_fields__.keys())
    assert "session_id" in field_names
    assert "assistant_id" in field_names


def test_assistant_runtime_has_no_provider_field():
    field_names = set(AssistantRuntime.__dataclass_fields__.keys())
    assert "provider" not in field_names
    assert "voice_provider" not in field_names


def test_assistant_runtime_conversation_id_is_a_pointer_not_an_object():
    """conversation_id must stay a plain string pointer, never an embedded ConversationState object."""
    runtime = AssistantRuntime(session_id="s1", assistant_id="a1", conversation_id="conv-1")
    assert isinstance(runtime.conversation_id, str)
