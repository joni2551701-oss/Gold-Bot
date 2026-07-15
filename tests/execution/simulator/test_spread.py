"""
Phase 60.3, TASK 4 -- execution/simulator/spread.py tests.
"""

from execution.simulator.spread import SpreadConfig, get_spread, is_spread_too_wide


def test_get_spread_returns_session_override():
    assert get_spread("LONDON") == 0.15
    assert get_spread("NY_NEWS") == 0.80


def test_get_spread_falls_back_to_default_for_unknown_session():
    assert get_spread("TOKYO") == SpreadConfig().default_points


def test_get_spread_none_session_returns_default():
    assert get_spread(None) == SpreadConfig().default_points


def test_get_spread_respects_custom_config():
    config = SpreadConfig(default_points=0.5, session_spreads={"LONDON": 0.05})
    assert get_spread("LONDON", config) == 0.05
    assert get_spread("NY_NEWS", config) == 0.5


def test_is_spread_too_wide_true_at_or_above_max():
    config = SpreadConfig(max_points=1.0)
    assert is_spread_too_wide(1.0, config) is True
    assert is_spread_too_wide(1.5, config) is True


def test_is_spread_too_wide_false_below_max():
    config = SpreadConfig(max_points=1.0)
    assert is_spread_too_wide(0.5, config) is False


def test_default_session_spreads_are_independent_across_instances():
    """A frozen dataclass with a mutable default (dict) must not leak state across instances."""
    a = SpreadConfig()
    b = SpreadConfig()
    assert a.session_spreads is not b.session_spreads
