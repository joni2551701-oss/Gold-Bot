"""
Phase 59.3, TASK 5 -- telegram/owner/provider_commands.py tests.
"""

from data_layer.providers.registry import ProviderRegistry, build_default_registry
from telegram.owner.provider_commands import (
    ProviderCommandResult,
    disable_provider,
    enable_provider,
    get_data_status,
    list_providers,
)


def test_list_providers_includes_every_registered_provider():
    result = list_providers()

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    for name in ("twelvedata", "mt5", "binance", "fred"):
        assert name in result.message


def test_list_providers_reports_unavailable_for_stubs():
    result = list_providers()
    assert "mt5: UNAVAILABLE" in result.message


def test_list_providers_with_empty_registry_still_succeeds():
    result = list_providers(ProviderRegistry())
    assert result.success is True


def test_get_data_status_includes_status_and_latency():
    result = get_data_status()

    assert result.success is True
    assert "OFFLINE" in result.message or "ONLINE" in result.message
    assert "latency=" in result.message


def test_get_data_status_accepts_an_injected_registry():
    registry = build_default_registry()
    result = get_data_status(registry)
    assert result.success is True


def test_enable_provider_is_honest_about_not_being_a_working_toggle():
    result = enable_provider("mt5")

    assert result.success is False
    assert "runtime" in result.message.lower()


def test_disable_provider_is_honest_about_not_being_a_working_toggle():
    result = disable_provider("twelve")

    assert result.success is False
    assert "twelvedata" in result.message  # alias resolved


def test_name_alias_resolves_twelve_to_twelvedata():
    result = enable_provider("TWELVE")
    assert "twelvedata" in result.message


def test_provider_commands_never_raise():
    list_providers()
    get_data_status()
    enable_provider("nonexistent")
    disable_provider("nonexistent")
