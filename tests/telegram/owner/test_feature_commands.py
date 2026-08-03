"""
Phase 59.3, TASK 5 -- platform_layer/telegram/owner/feature_commands.py tests.
"""

from platform_layer.telegram.owner.feature_commands import list_features
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def test_list_features_succeeds():
    result = list_features()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_list_features_includes_every_configuration_feature_flag():
    result = list_features()
    for flag in ("enable_ai", "enable_crypto", "enable_swing", "enable_ai_memory", "enable_replay"):
        assert flag in result.message


def test_list_features_includes_provider_flags():
    result = list_features()
    assert "MARKET_DATA_PROVIDER" in result.message
    assert "ENABLE_TWELVEDATA" in result.message
    assert "ENABLE_MT5" in result.message


def test_list_features_reflects_real_default_config_values():
    result = list_features()
    assert "MARKET_DATA_PROVIDER: twelvedata" in result.message
    assert "ENABLE_MT5: False" in result.message


def test_list_features_never_raises():
    list_features()
