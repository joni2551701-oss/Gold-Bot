"""
Phase 59.8, Owner Control Center -- platform_layer/telegram/owner/control_commands.py
tests. Real RuntimeFeatureManager (backed by real SQLite repositories,
tests/conftest.py's autouse fresh_database fixture) -- no mocks.
"""

from platform_layer.telegram.owner.control_commands import disable_feature, enable_feature, get_feature_states
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def test_get_feature_states_returns_a_provider_command_result():
    result = get_feature_states()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_feature_states_includes_a_known_registry_entry():
    result = get_feature_states()
    assert "ENABLE_MT5" in result.message


def test_get_feature_states_renders_on_off_not_active_inactive():
    result = get_feature_states()
    assert "OFF" in result.message or "ON" in result.message
    assert "ACTIVE" not in result.message
    assert "INACTIVE" not in result.message


def test_enable_feature_reflects_in_get_feature_states():
    enable_feature("ENABLE_NEWS", actor="owner")

    result = get_feature_states()

    assert "ENABLE_NEWS  ON" in result.message


def test_disable_feature_reflects_in_get_feature_states():
    enable_feature("ENABLE_NEWS")
    disable_feature("ENABLE_NEWS", actor="owner")

    result = get_feature_states()

    assert "ENABLE_NEWS  OFF" in result.message


def test_enable_feature_reports_dependency_rejection():
    result = enable_feature("ENABLE_BACKTEST", actor="owner")

    assert result.success is False
    assert "ENABLE_DATASET_SYNC" in result.message


def test_enable_feature_returns_provider_command_result():
    result = enable_feature("ENABLE_NEWS")
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
