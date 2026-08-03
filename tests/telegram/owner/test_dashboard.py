"""
Phase 59.8, Owner Control Center -- platform_layer/telegram/owner/dashboard.py tests.
Real repositories (SQLite, tests/conftest.py's autouse fresh_database
fixture) -- no mocks.
"""

from platform_layer.telegram.owner.control_commands import enable_feature
from platform_layer.telegram.owner.dashboard import get_dashboard
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def test_get_dashboard_returns_a_provider_command_result():
    result = get_dashboard()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_dashboard_includes_all_three_sections():
    result = get_dashboard()

    assert "GoldBot Status" in result.message
    assert "Features:" in result.message
    assert "Providers:" in result.message


def test_get_dashboard_feature_count_reflects_a_toggle():
    before = get_dashboard()
    before_on = before.message.split("Features: ")[1].split("/")[0]

    enable_feature("ENABLE_NEWS", actor="owner")

    after = get_dashboard()
    after_on = after.message.split("Features: ")[1].split("/")[0]

    assert int(after_on) == int(before_on) + 1


def test_get_dashboard_lists_provider_availability():
    result = get_dashboard()
    assert "twelvedata: AVAILABLE" in result.message
