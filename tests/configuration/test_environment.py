"""
Phase A13 -- Configuration Layer tests: Environment
(configuration/environment.py).
"""

import pytest

from goldbot.core_layer.configuration.environment import Environment, resolve_environment


def test_enum_creation_has_exactly_three_values():
    assert {e.value for e in Environment} == {"development", "testing", "production"}
    assert Environment.DEVELOPMENT.value == "development"
    assert Environment.TESTING.value == "testing"
    assert Environment.PRODUCTION.value == "production"


def test_environment_from_raw_string_round_trips():
    assert Environment("development") == Environment.DEVELOPMENT
    assert Environment("testing") == Environment.TESTING
    assert Environment("production") == Environment.PRODUCTION


def test_invalid_value_rejected_by_raw_constructor():
    with pytest.raises(ValueError):
        Environment("staging")


def test_resolve_environment_maps_known_values():
    assert resolve_environment("development") == Environment.DEVELOPMENT
    assert resolve_environment("testing") == Environment.TESTING
    assert resolve_environment("production") == Environment.PRODUCTION


def test_resolve_environment_is_case_insensitive():
    assert resolve_environment("PRODUCTION") == Environment.PRODUCTION
    assert resolve_environment("Development") == Environment.DEVELOPMENT


def test_resolve_environment_defaults_safely_on_none():
    assert resolve_environment(None) == Environment.DEVELOPMENT


def test_resolve_environment_defaults_safely_on_invalid_value():
    """Never raises -- an unrecognized APP_ENV value must not crash application startup."""
    assert resolve_environment("staging") == Environment.DEVELOPMENT
    assert resolve_environment("") == Environment.DEVELOPMENT


def test_resolve_environment_honors_custom_default():
    assert resolve_environment("garbage", default=Environment.PRODUCTION) == Environment.PRODUCTION
    assert resolve_environment(None, default=Environment.TESTING) == Environment.TESTING
