"""
Phase 59.3, TASK 5 -- telegram/owner/system_commands.py tests.
"""

from telegram.owner.provider_commands import ProviderCommandResult
from telegram.owner.system_commands import count_online_providers, get_system_health


def test_get_system_health_succeeds_and_never_raises():
    result = get_system_health()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_system_health_includes_admin_service_fields():
    result = get_system_health()
    assert "database:" in result.message
    assert "telegram:" in result.message
    assert "ai:" in result.message


def test_get_system_health_includes_every_provider():
    result = get_system_health()
    for name in ("twelvedata", "mt5", "binance", "fred"):
        assert name in result.message


def test_count_online_providers_excludes_always_unimplemented_stubs():
    """MT5/Binance/FRED are always OFFLINE; TwelveData may report ONLINE since tests/conftest.py sets a placeholder API key -- so at most 1 provider can be online in this test environment."""
    assert count_online_providers() <= 1


def test_count_online_providers_never_raises():
    count_online_providers()
