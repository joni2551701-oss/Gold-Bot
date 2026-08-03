"""Phase 61.4 TASK 2 — User Capability: one "can this real user do X" lookup composing AccessControl/ToolPermissions/UsageLimiter, no new entitlement logic."""

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_service.access.user_capability import UserCapability, UserCapabilityService
from ai_layer.ai_engine.capabilities.capability import Capability


def test_can_use_capability_delegates_to_access_control():
    service = UserCapabilityService()
    owner = UserCapability(telegram_id="1", role=AIRole.OWNER)
    free_user = UserCapability(telegram_id="2", role=AIRole.FREE)

    assert service.can_use_capability(owner, Capability.VISION) is True
    assert service.can_use_capability(free_user, Capability.VISION) is False


def test_can_use_tool_delegates_to_tool_permissions():
    service = UserCapabilityService()
    free_user = UserCapability(telegram_id="2", role=AIRole.FREE)

    assert service.can_use_tool(free_user, "education_tool") is True
    assert service.can_use_tool(free_user, "news_tool") is False


def test_check_and_record_usage_delegates_to_usage_limiter():
    service = UserCapabilityService()
    free_user = UserCapability(telegram_id="free-42", role=AIRole.FREE)

    first_check = service.check_usage(free_user, Capability.CHAT)
    assert first_check.allowed is True
    assert first_check.used == 0

    service.record_usage(free_user, Capability.CHAT)

    second_check = service.check_usage(free_user, Capability.CHAT)
    assert second_check.used == 1


def test_owner_usage_is_unlimited():
    service = UserCapabilityService()
    owner = UserCapability(telegram_id="owner-1", role=AIRole.OWNER)

    for _ in range(5):
        service.record_usage(owner, Capability.CHAT)

    result = service.check_usage(owner, Capability.CHAT)
    assert result.allowed is True
    assert result.limit == 0
