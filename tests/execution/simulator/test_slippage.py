"""
Phase 60.3, TASK 3 -- execution/simulator/slippage.py tests.
"""

import pytest

from execution.simulator.slippage import SlippageConfig, apply_slippage, compute_slippage


def test_compute_slippage_returns_configured_points():
    assert compute_slippage(SlippageConfig(points=0.15)) == 0.15


def test_compute_slippage_clamps_to_max():
    assert compute_slippage(SlippageConfig(points=1.0, max_points=0.5)) == 0.5


def test_compute_slippage_uses_defaults_when_no_config():
    assert compute_slippage() == SlippageConfig().points


def test_apply_slippage_buy_is_worse_higher():
    """Director's own worked example: BUY 2350.00 -> fill 2350.15."""
    fill = apply_slippage(2350.00, "BUY", 0.15)
    assert fill == pytest.approx(2350.15)


def test_apply_slippage_sell_is_worse_lower():
    fill = apply_slippage(2350.00, "SELL", 0.15)
    assert fill == pytest.approx(2349.85)


def test_apply_slippage_unknown_direction_raises():
    with pytest.raises(ValueError):
        apply_slippage(2350.00, "HOLD", 0.15)


def test_slippage_config_is_frozen():
    config = SlippageConfig()
    with pytest.raises(AttributeError):
        config.points = 99.0
