"""Setup layer — registry (TASK-CORE-007)."""

import pytest

from strategies.registry import (
    SetupRegistry,
    build_setup_registry,
    DuplicateStrategyNameError,
    DEFAULT_SETUP_STRATEGIES,
)
from strategies.base import SetupStrategy

_EXPECTED = {
    "AMD_SETUP", "LIQUIDITY_SETUP", "FVG_SETUP", "ORDER_BLOCK_SETUP",
    "BOS_CHOCH_SETUP", "TREND_CONTINUATION_SETUP", "REVERSAL_SETUP",
    "BREAKOUT_SETUP", "SESSION_SETUP", "SUPPORT_RESISTANCE_SETUP", "WYCKOFF_SETUP",
}


def test_default_registry_has_all_eleven():
    reg = build_setup_registry()
    assert set(reg.names()) == _EXPECTED
    assert len(reg.all()) == 11
    assert all(isinstance(s, SetupStrategy) for s in reg.all())


def test_registry_covers_the_directors_list():
    # AMD, Liquidity, FVG, OB, BOS, Trend, Reversal, Breakout, Session, SNR, Wyckoff.
    assert len(DEFAULT_SETUP_STRATEGIES) == 11
    assert "SUPPORT_RESISTANCE_SETUP" in _EXPECTED  # SNR present (required)


def test_get_returns_none_for_unknown():
    assert build_setup_registry().get("NOPE") is None


def test_duplicate_registration_raises():
    reg = SetupRegistry()
    from strategies.snr_strategy import SNRStrategy
    reg.register(SNRStrategy())
    with pytest.raises(DuplicateStrategyNameError):
        reg.register(SNRStrategy())


def test_build_returns_fresh_registries():
    assert build_setup_registry() is not build_setup_registry()
