from ai.access.permissions import AIRole
from assistant.assistant_manager import AssistantManager
from assistant.identity_manager import IdentityManager
from configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_personal_ai=True)
DISABLED = FeatureFlags(enable_personal_ai=False)


def _manager(flags=ENABLED):
    return AssistantManager(identity_manager=IdentityManager(), flags=flags)


def _profile(manager, role=AIRole.OWNER):
    return manager.create_assistant(user_id="u1", role=role)


def test_create_runtime_owner_succeeds():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    assert runtime is not None
    assert runtime.assistant_id == profile.assistant_id
    assert runtime.active is True


def test_create_runtime_admin_blocked():
    manager = _manager()
    profile = _profile(manager)
    assert manager.create_runtime(profile.assistant_id, AIRole.ADMIN) is None


def test_create_runtime_vip_blocked():
    manager = _manager()
    profile = _profile(manager)
    assert manager.create_runtime(profile.assistant_id, AIRole.VIP) is None


def test_create_runtime_premium_blocked():
    manager = _manager()
    profile = _profile(manager)
    assert manager.create_runtime(profile.assistant_id, AIRole.PREMIUM) is None


def test_create_runtime_free_blocked():
    manager = _manager()
    profile = _profile(manager)
    assert manager.create_runtime(profile.assistant_id, AIRole.FREE) is None


def test_create_runtime_blocked_when_flag_disabled_even_for_owner():
    im = IdentityManager()
    profile_manager = AssistantManager(identity_manager=im, flags=ENABLED)
    profile = _profile(profile_manager)
    # runtime manager itself has the flag off
    manager_disabled = AssistantManager(identity_manager=im, flags=DISABLED)
    manager_disabled._profiles[profile.assistant_id] = profile
    assert manager_disabled.create_runtime(profile.assistant_id, AIRole.OWNER) is None


def test_create_runtime_unknown_assistant_id_returns_none():
    manager = _manager()
    assert manager.create_runtime("nonexistent", AIRole.OWNER) is None


def test_create_runtime_sets_started_and_updated_at():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    assert runtime.started_at is not None
    assert runtime.updated_at is not None
    assert runtime.started_at == runtime.updated_at


def test_load_runtime_returns_created_runtime():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    assert manager.load_runtime(runtime.session_id) is runtime


def test_load_runtime_unknown_session_id_returns_none():
    manager = _manager()
    assert manager.load_runtime("nonexistent") is None


def test_restore_runtime_owner_succeeds():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    manager.close_runtime(runtime.session_id, AIRole.OWNER)
    assert manager.runtime_status(runtime.session_id) == "closed"
    result = manager.restore_runtime(runtime.session_id, AIRole.OWNER)
    assert result is True
    assert manager.runtime_status(runtime.session_id) == "active"


def test_restore_runtime_admin_blocked():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    manager.close_runtime(runtime.session_id, AIRole.OWNER)
    assert manager.restore_runtime(runtime.session_id, AIRole.ADMIN) is False
    assert manager.runtime_status(runtime.session_id) == "closed"


def test_restore_runtime_unknown_session_id_returns_false():
    manager = _manager()
    assert manager.restore_runtime("nonexistent", AIRole.OWNER) is False


def test_close_runtime_owner_succeeds():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    result = manager.close_runtime(runtime.session_id, AIRole.OWNER)
    assert result is True
    assert manager.runtime_status(runtime.session_id) == "closed"


def test_close_runtime_admin_blocked():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    assert manager.close_runtime(runtime.session_id, AIRole.ADMIN) is False
    assert manager.runtime_status(runtime.session_id) == "active"


def test_close_runtime_unknown_session_id_returns_false():
    manager = _manager()
    assert manager.close_runtime("nonexistent", AIRole.OWNER) is False


def test_close_runtime_keeps_record_loadable():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    manager.close_runtime(runtime.session_id, AIRole.OWNER)
    assert manager.load_runtime(runtime.session_id) is not None


def test_runtime_status_active_after_create():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    assert manager.runtime_status(runtime.session_id) == "active"


def test_runtime_status_unknown_session_id_returns_none():
    manager = _manager()
    assert manager.runtime_status("nonexistent") is None


def test_close_runtime_updates_updated_at():
    manager = _manager()
    profile = _profile(manager)
    runtime = manager.create_runtime(profile.assistant_id, AIRole.OWNER)
    original_updated_at = runtime.updated_at
    manager.close_runtime(runtime.session_id, AIRole.OWNER)
    assert manager.load_runtime(runtime.session_id).updated_at >= original_updated_at


def test_multiple_assistants_get_independent_runtimes():
    manager = _manager()
    p1 = manager.create_assistant(user_id="u1", role=AIRole.OWNER)
    p2 = manager.create_assistant(user_id="u2", role=AIRole.OWNER)
    r1 = manager.create_runtime(p1.assistant_id, AIRole.OWNER)
    r2 = manager.create_runtime(p2.assistant_id, AIRole.OWNER)
    assert r1.session_id != r2.session_id
    assert r1.assistant_id != r2.assistant_id
