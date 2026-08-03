from ai.access.permissions import AIRole
from ai.coaching.access import is_coaching_intelligence_enabled_for
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_coaching_intelligence=True)
DISABLED = FeatureFlags(enable_coaching_intelligence=False)


def test_owner_enabled_when_flag_on():
    assert is_coaching_intelligence_enabled_for(AIRole.OWNER, ENABLED) is True


def test_owner_blocked_when_flag_off():
    assert is_coaching_intelligence_enabled_for(AIRole.OWNER, DISABLED) is False


def test_admin_blocked_even_with_flag_on():
    assert is_coaching_intelligence_enabled_for(AIRole.ADMIN, ENABLED) is False


def test_vip_blocked_even_with_flag_on():
    assert is_coaching_intelligence_enabled_for(AIRole.VIP, ENABLED) is False


def test_premium_blocked_even_with_flag_on():
    assert is_coaching_intelligence_enabled_for(AIRole.PREMIUM, ENABLED) is False


def test_free_blocked_even_with_flag_on():
    assert is_coaching_intelligence_enabled_for(AIRole.FREE, ENABLED) is False


def test_default_flags_block_owner():
    assert is_coaching_intelligence_enabled_for(AIRole.OWNER) is False


def test_never_raises_for_any_role():
    for role in AIRole:
        result = is_coaching_intelligence_enabled_for(role, ENABLED)
        assert isinstance(result, bool)


def test_only_owner_true_across_all_roles_when_enabled():
    results = {role: is_coaching_intelligence_enabled_for(role, ENABLED) for role in AIRole}
    assert results[AIRole.OWNER] is True
    assert all(v is False for role, v in results.items() if role is not AIRole.OWNER)


def test_all_roles_false_when_disabled():
    results = {role: is_coaching_intelligence_enabled_for(role, DISABLED) for role in AIRole}
    assert all(v is False for v in results.values())
