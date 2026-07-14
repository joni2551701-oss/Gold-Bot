"""
Phase A18 -- Error Classification tests: hierarchy
(core/errors/base.py, core/errors/exceptions.py).
"""

import pytest

from core.errors.base import GoldBotError
from core.errors.exceptions import (
    ConfigurationError,
    ValidationError,
    DataError,
    ExternalAPIError,
    DatabaseError,
    PermissionError,
    StrategyError,
    DecisionError,
    ExecutionError,
)

ALL_SUBCLASSES = (
    ConfigurationError,
    ValidationError,
    DataError,
    ExternalAPIError,
    DatabaseError,
    PermissionError,
    StrategyError,
    DecisionError,
    ExecutionError,
)


def test_goldbot_error_is_a_real_exception():
    assert issubclass(GoldBotError, Exception)


@pytest.mark.parametrize("subclass", ALL_SUBCLASSES)
def test_every_subclass_inherits_from_goldbot_error(subclass):
    assert issubclass(subclass, GoldBotError)


def test_all_nine_required_subclasses_exist():
    assert len(ALL_SUBCLASSES) == 9


@pytest.mark.parametrize("subclass", ALL_SUBCLASSES)
def test_subclass_can_be_raised_and_caught_as_goldbot_error(subclass):
    with pytest.raises(GoldBotError):
        raise subclass(code="TEST_001", message="test", module="TestModule")


@pytest.mark.parametrize("subclass", ALL_SUBCLASSES)
def test_subclass_can_be_caught_by_its_own_type(subclass):
    with pytest.raises(subclass):
        raise subclass(code="TEST_001", message="test", module="TestModule")


def test_subclasses_are_distinct_types():
    """A DataError must not be catchable as a ConfigurationError -- distinct type identity, not just a shared base."""
    with pytest.raises(DataError):
        try:
            raise DataError(code="DATA_001", message="x", module="M")
        except ConfigurationError:
            pytest.fail("DataError should not be caught by except ConfigurationError")


def test_error_carries_code_message_module_timestamp():
    error = DataError(code="DATA_001", message="Invalid candle", module="MarketData")

    assert error.code == "DATA_001"
    assert error.message == "Invalid candle"
    assert error.module == "MarketData"
    assert error.timestamp is not None


def test_error_str_includes_code_message_and_module():
    error = DataError(code="DATA_001", message="Invalid candle", module="MarketData")
    rendered = str(error)

    assert "DATA_001" in rendered
    assert "Invalid candle" in rendered
    assert "MarketData" in rendered


def test_details_defaults_to_empty_dict_not_none():
    error = DataError(code="DATA_001", message="x", module="M")
    assert error.details == {}


def test_details_can_be_supplied():
    error = DataError(code="DATA_001", message="x", module="M", details={"offending_value": -1})
    assert error.details == {"offending_value": -1}


def test_goldbot_error_cannot_be_raised_without_required_arguments():
    with pytest.raises(TypeError):
        GoldBotError()  # code/message/module are required, no defaults
