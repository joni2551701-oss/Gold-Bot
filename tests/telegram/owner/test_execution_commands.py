"""
Phase 60.3, TASK 7 -- platform_layer/telegram/owner/execution_commands.py tests.
"""

from platform_layer.telegram.owner.execution_commands import execution_status, set_simulation_mode, slippage_status
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def test_execution_status_reports_defaults():
    result = execution_status()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "Mode:" in result.message
    assert "Slippage:" in result.message
    assert "Live execution: INERT" in result.message


def test_slippage_status_reports_configured_points():
    result = slippage_status()
    assert result.success is True
    assert "Slippage:" in result.message


def test_set_simulation_mode_accepts_known_mode():
    result = set_simulation_mode("LONDON")
    assert result.success is True
    assert "LONDON" in result.message

    status = execution_status()
    assert "Mode: LONDON" in status.message

    set_simulation_mode("DEFAULT")  # reset for other tests


def test_set_simulation_mode_rejects_unknown_mode():
    result = set_simulation_mode("TOKYO")
    assert result.success is False
    assert "Unknown mode" in result.message
