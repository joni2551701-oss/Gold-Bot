from ai.access.permissions import AIRole
from assistant.assistant_manager import AssistantManager
from assistant.identity_manager import IdentityManager
from goldbot.core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_personal_ai=True)
DISABLED = FeatureFlags(enable_personal_ai=False)


def _manager(flags=ENABLED):
    return AssistantManager(identity_manager=IdentityManager(), flags=flags)


def test_create_assistant_owner_succeeds():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    assert profile is not None
    assert profile.user_id == "u1"
    assert profile.selected_identity == "Senior"


def test_create_assistant_default_identity_is_senior():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    assert profile.selected_identity == "Senior"


def test_create_assistant_explicit_seniorita():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER, identity_name="Seniorita")
    assert profile.selected_identity == "Seniorita"


def test_create_assistant_admin_blocked():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.ADMIN)
    assert profile is None


def test_create_assistant_vip_blocked():
    manager = _manager()
    assert manager.create_assistant(user_id="u1", role=AIRole.VIP) is None


def test_create_assistant_premium_blocked():
    manager = _manager()
    assert manager.create_assistant(user_id="u1", role=AIRole.PREMIUM) is None


def test_create_assistant_free_blocked():
    manager = _manager()
    assert manager.create_assistant(user_id="u1", role=AIRole.FREE) is None


def test_create_assistant_blocked_when_flag_disabled_even_for_owner():
    manager = _manager(flags=DISABLED)
    assert manager.create_assistant(user_id="u1", role=AIRole.OWNER) is None


def test_create_assistant_unknown_identity_returns_none():
    manager = _manager()
    assert manager.create_assistant(user_id="u1", role=AIRole.OWNER, identity_name="Nonexistent") is None


def test_create_assistant_sets_created_and_updated_at():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    assert profile.created_at is not None
    assert profile.updated_at is not None
    assert profile.created_at == profile.updated_at


def test_get_assistant_returns_created_profile():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    fetched = manager.get_assistant(profile.assistant_id)
    assert fetched is profile


def test_get_assistant_unknown_id_returns_none():
    manager = _manager()
    assert manager.get_assistant("nonexistent") is None


def test_get_assistant_for_user_finds_by_user_id():
    manager = _manager()
    profile = manager.create_assistant(user_id="u42", role=AIRole.OWNER)
    fetched = manager.get_assistant_for_user("u42")
    assert fetched is profile


def test_get_assistant_for_user_unknown_returns_none():
    manager = _manager()
    assert manager.get_assistant_for_user("nonexistent-user") is None


def test_switch_identity_owner_succeeds():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    result = manager.switch_identity(profile.assistant_id, "Seniorita", AIRole.OWNER)
    assert result is True
    assert manager.get_assistant(profile.assistant_id).selected_identity == "Seniorita"


def test_switch_identity_admin_blocked():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    result = manager.switch_identity(profile.assistant_id, "Seniorita", AIRole.ADMIN)
    assert result is False
    assert manager.get_assistant(profile.assistant_id).selected_identity == "Senior"


def test_switch_identity_unknown_assistant_id_returns_false():
    manager = _manager()
    assert manager.switch_identity("nonexistent", "Seniorita", AIRole.OWNER) is False


def test_switch_identity_unknown_identity_name_returns_false():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    assert manager.switch_identity(profile.assistant_id, "Nonexistent", AIRole.OWNER) is False


def test_switch_identity_updates_updated_at():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    original_updated_at = profile.updated_at
    manager.switch_identity(profile.assistant_id, "Seniorita", AIRole.OWNER)
    assert manager.get_assistant(profile.assistant_id).updated_at >= original_updated_at


def test_update_settings_owner_succeeds():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    result = manager.update_settings(profile.assistant_id, AIRole.OWNER, selected_voice="Narrator", selected_language="es", timezone_name="Europe/Berlin")
    assert result is True
    updated = manager.get_assistant(profile.assistant_id)
    assert updated.selected_voice == "Narrator"
    assert updated.selected_language == "es"
    assert updated.timezone == "Europe/Berlin"


def test_update_settings_admin_blocked():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    result = manager.update_settings(profile.assistant_id, AIRole.ADMIN, selected_voice="Narrator")
    assert result is False
    assert manager.get_assistant(profile.assistant_id).selected_voice is None


def test_update_settings_partial_update_leaves_other_fields_unchanged():
    manager = _manager()
    profile = manager.create_assistant(user_id="u1", role=AIRole.OWNER, language="en", timezone_name="UTC")
    manager.update_settings(profile.assistant_id, AIRole.OWNER, selected_language="fr")
    updated = manager.get_assistant(profile.assistant_id)
    assert updated.selected_language == "fr"
    assert updated.timezone == "UTC"


def test_update_settings_unknown_assistant_id_returns_false():
    manager = _manager()
    assert manager.update_settings("nonexistent", AIRole.OWNER, selected_voice="Narrator") is False


def test_multiple_users_get_independent_profiles():
    manager = _manager()
    p1 = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    p2 = manager.create_assistant(user_id="u2", role=AIRole.OWNER)
    assert p1.assistant_id != p2.assistant_id
    assert manager.get_assistant_for_user("u1") is p1
    assert manager.get_assistant_for_user("u2") is p2
