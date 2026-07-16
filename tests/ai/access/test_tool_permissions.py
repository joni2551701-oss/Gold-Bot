"""Phase 61.1 TASK 6 — AI Tool Permission Matrix, a second axis alongside Capability entitlement."""

from ai.access.permissions import AIRole
from ai.access.tool_permissions import ToolPermissions


def test_owner_and_admin_are_allowed_every_tool():
    permissions = ToolPermissions()
    for tool_name in ("market_tool", "news_tool", "analytics_tool", "education_tool"):
        assert permissions.is_tool_allowed(AIRole.OWNER, tool_name)
        assert permissions.is_tool_allowed(AIRole.ADMIN, tool_name)


def test_vip_is_allowed_news_tool_per_worked_example():
    permissions = ToolPermissions()
    assert permissions.is_tool_allowed(AIRole.VIP, "news_tool") is True


def test_free_is_not_allowed_news_tool_per_worked_example():
    permissions = ToolPermissions()
    assert permissions.is_tool_allowed(AIRole.FREE, "news_tool") is False


def test_free_is_allowed_education_tool():
    permissions = ToolPermissions()
    assert permissions.is_tool_allowed(AIRole.FREE, "education_tool") is True


def test_allowed_tools_returns_the_full_set_for_a_role():
    permissions = ToolPermissions()
    assert permissions.allowed_tools(AIRole.FREE) == frozenset({"education_tool"})


def test_custom_matrix_overrides_default():
    custom = {AIRole.FREE: frozenset({"news_tool"})}
    permissions = ToolPermissions(matrix=custom)
    assert permissions.is_tool_allowed(AIRole.FREE, "news_tool") is True
    assert permissions.is_tool_allowed(AIRole.FREE, "education_tool") is False


def test_unknown_tool_name_is_never_allowed():
    permissions = ToolPermissions()
    assert permissions.is_tool_allowed(AIRole.OWNER, "nonexistent_tool") is False
