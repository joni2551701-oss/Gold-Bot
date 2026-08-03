"""Phase 61.0 TASK 6 — AI Access Control: Role x Capability permission matrix, not a global AI on/off."""

from ai_layer.ai_service.access.access_control import AccessControl
from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability


def test_owner_and_admin_are_allowed_every_capability():
    access = AccessControl()
    for capability in Capability:
        assert access.is_allowed(AIRole.OWNER, capability)
        assert access.is_allowed(AIRole.ADMIN, capability)


def test_free_role_is_restricted_to_low_cost_capabilities():
    access = AccessControl()
    assert access.is_allowed(AIRole.FREE, Capability.CHAT)
    assert access.is_allowed(AIRole.FREE, Capability.EXPLANATION)
    assert not access.is_allowed(AIRole.FREE, Capability.VISION)
    assert not access.is_allowed(AIRole.FREE, Capability.TOOL_CALLING)


def test_premium_has_more_access_than_free_but_less_than_vip():
    access = AccessControl()
    premium = access.allowed_capabilities(AIRole.PREMIUM)
    free = access.allowed_capabilities(AIRole.FREE)
    vip = access.allowed_capabilities(AIRole.VIP)
    assert free.issubset(premium)
    assert premium.issubset(vip)
    assert premium != vip


def test_custom_matrix_overrides_default():
    custom = {AIRole.FREE: frozenset({Capability.VISION})}
    access = AccessControl(matrix=custom)
    assert access.is_allowed(AIRole.FREE, Capability.VISION)
    assert not access.is_allowed(AIRole.FREE, Capability.CHAT)


def test_role_missing_from_matrix_has_no_entitlement():
    access = AccessControl(matrix={})
    assert not access.is_allowed(AIRole.OWNER, Capability.CHAT)
