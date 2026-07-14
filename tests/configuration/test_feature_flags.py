"""
Phase A13 -- Configuration Layer tests: FeatureFlags
(configuration/feature_flags.py).
"""

import dataclasses

import pytest

from configuration.feature_flags import FeatureFlags, DEFAULT_FLAGS


def test_default_feature_flags_are_all_false():
    flags = FeatureFlags()

    assert flags.enable_ai is False
    assert flags.enable_crypto is False
    assert flags.enable_swing is False
    assert flags.enable_ai_memory is False
    assert flags.enable_replay is False


def test_default_flags_constant_matches_defaults():
    assert DEFAULT_FLAGS == FeatureFlags()


def test_feature_flags_matches_director_example():
    flags = FeatureFlags(
        enable_ai=False,
        enable_crypto=False,
        enable_swing=False,
        enable_ai_memory=False,
    )

    assert flags.enable_ai is False
    assert flags.enable_crypto is False
    assert flags.enable_swing is False
    assert flags.enable_ai_memory is False
    assert flags.enable_replay is False  # not passed -- default still applies


def test_feature_flags_is_immutable():
    flags = FeatureFlags()
    with pytest.raises(dataclasses.FrozenInstanceError):
        flags.enable_ai = True


def test_feature_flags_toggle_support_via_replace():
    """Frozen dataclass -- 'toggling' means constructing a new object, not mutating one in place."""
    base = FeatureFlags()
    toggled = dataclasses.replace(base, enable_ai=True)

    assert base.enable_ai is False  # original untouched
    assert toggled.enable_ai is True
    # every other flag stays at its safe default
    assert toggled.enable_crypto is False
    assert toggled.enable_swing is False
    assert toggled.enable_ai_memory is False
    assert toggled.enable_replay is False


def test_feature_flags_field_names_are_exactly_the_five_foundation_flags():
    field_names = {f.name for f in dataclasses.fields(FeatureFlags)}
    assert field_names == {
        "enable_ai", "enable_crypto", "enable_swing", "enable_ai_memory", "enable_replay",
    }
