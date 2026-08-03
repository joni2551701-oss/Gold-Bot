"""
Phase 59.3, TASK 1 -- data_layer/normalization/timeframe_mapper.py tests.
"""

from data_layer.normalization.timeframe_mapper import (
    from_provider_timeframe,
    is_known_timeframe,
    to_provider_timeframe,
)
from data_layer.providers.twelve_data_client import TwelveDataClient


def test_to_provider_timeframe_twelvedata_matches_the_real_client():
    """Cross-checked against TwelveDataClient.INTERVAL_MAP itself -- must never drift."""
    client = TwelveDataClient()
    for canonical, real_value in client.INTERVAL_MAP.items():
        assert to_provider_timeframe(canonical, "twelvedata") == real_value


def test_to_provider_timeframe_binance():
    assert to_provider_timeframe("M15", "binance") == "15m"


def test_to_provider_timeframe_unmapped_falls_back_unchanged():
    assert to_provider_timeframe("W1", "twelvedata") == "W1"


def test_from_provider_timeframe_is_the_exact_inverse():
    assert from_provider_timeframe("15min", "twelvedata") == "M15"
    assert from_provider_timeframe("15m", "binance") == "M15"


def test_is_known_timeframe_true_for_mapped_pair():
    assert is_known_timeframe("Daily", "twelvedata") is True


def test_is_known_timeframe_false_for_unmapped_pair():
    assert is_known_timeframe("W1", "twelvedata") is False


def test_never_raises_on_empty_strings():
    to_provider_timeframe("", "")
    from_provider_timeframe("", "")
    is_known_timeframe("", "")
