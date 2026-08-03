"""
Phase 59.3, TASK 1 -- data_layer/normalization/symbol_mapper.py tests.
"""

from data_layer.normalization.symbol_mapper import from_provider_symbol, is_known_symbol, to_provider_symbol


def test_to_provider_symbol_twelvedata():
    assert to_provider_symbol("XAUUSD", "twelvedata") == "XAU/USD"


def test_to_provider_symbol_binance():
    assert to_provider_symbol("BTCUSD", "binance") == "BTCUSDT"


def test_to_provider_symbol_is_case_insensitive():
    assert to_provider_symbol("xauusd", "TwelveData") == "XAU/USD"


def test_to_provider_symbol_unmapped_falls_back_unchanged():
    assert to_provider_symbol("UNKNOWNPAIR", "twelvedata") == "UNKNOWNPAIR"


def test_to_provider_symbol_unknown_provider_falls_back_unchanged():
    assert to_provider_symbol("XAUUSD", "some_future_provider") == "XAUUSD"


def test_from_provider_symbol_is_the_exact_inverse():
    assert from_provider_symbol("XAU/USD", "twelvedata") == "XAUUSD"
    assert from_provider_symbol("BTCUSDT", "binance") == "BTCUSD"


def test_from_provider_symbol_unmapped_falls_back_unchanged():
    assert from_provider_symbol("SOMETHING_ELSE", "twelvedata") == "SOMETHING_ELSE"


def test_is_known_symbol_true_for_mapped_pair():
    assert is_known_symbol("XAUUSD", "twelvedata") is True


def test_is_known_symbol_false_for_unmapped_pair():
    assert is_known_symbol("DOGEUSD", "binance") is False


def test_never_raises_on_empty_strings():
    to_provider_symbol("", "")
    from_provider_symbol("", "")
    is_known_symbol("", "")
