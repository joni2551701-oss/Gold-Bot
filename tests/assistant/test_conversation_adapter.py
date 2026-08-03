from ai.access.permissions import AIRole
from assistant.assistant_manager import AssistantManager
from assistant.conversation_adapter import (
    assistant_memory_scope_key,
    assistant_to_conversation_params,
    assistant_to_voice_session_params,
)
from assistant.identity_manager import IdentityManager
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_personal_ai=True)


def _profile_and_identity():
    manager = AssistantManager(identity_manager=IdentityManager(), flags=ENABLED)
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER, identity_name="Senior")
    identity = IdentityManager().get(profile.selected_identity)
    return profile, identity


def test_assistant_to_voice_session_params_shape():
    profile, identity = _profile_and_identity()
    params = assistant_to_voice_session_params(profile, identity)
    assert set(params.keys()) == {"user_id", "voice_profile_name", "language"}


def test_assistant_to_voice_session_params_falls_back_to_identity_default_voice():
    profile, identity = _profile_and_identity()
    assert profile.selected_voice is None
    params = assistant_to_voice_session_params(profile, identity)
    assert params["voice_profile_name"] == identity.default_voice


def test_assistant_to_voice_session_params_prefers_explicit_selected_voice():
    profile, identity = _profile_and_identity()
    profile.selected_voice = "Narrator"
    params = assistant_to_voice_session_params(profile, identity)
    assert params["voice_profile_name"] == "Narrator"


def test_assistant_to_voice_session_params_uses_profile_language():
    profile, identity = _profile_and_identity()
    profile.selected_language = "es"
    params = assistant_to_voice_session_params(profile, identity)
    assert params["language"] == "es"


def test_assistant_to_conversation_params_shape():
    profile, _ = _profile_and_identity()
    params = assistant_to_conversation_params(profile)
    assert params == {"telegram_id": profile.user_id}


def test_assistant_memory_scope_key_scoped_by_user_id():
    profile, _ = _profile_and_identity()
    key = assistant_memory_scope_key(profile)
    assert key == f"USER_PREFERENCE:{profile.user_id}"
    assert profile.assistant_id not in key


def test_assistant_memory_scope_key_with_sub_key():
    profile, _ = _profile_and_identity()
    key = assistant_memory_scope_key(profile, sub_key="tone")
    assert key == f"USER_PREFERENCE:{profile.user_id}:tone"


def test_assistant_memory_scope_key_never_uses_assistant_id_as_scope():
    profile, _ = _profile_and_identity()
    key = assistant_memory_scope_key(profile)
    assert not key.startswith(profile.assistant_id)
