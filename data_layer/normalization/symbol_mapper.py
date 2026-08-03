"""
Data Layer — Symbol Mapper (Phase 59.3, TASK 1: Provider Normalization).

Audit finding this module acts on: GoldBot's own canonical symbol
vocabulary (e.g. "XAUUSD", "BTCUSDT") already flows through
data_layer/providers/*.py's MarketCandle unchanged -- each Provider's own
adapter (TwelveDataProvider.get_candles(), etc.) already sets
MarketCandle.symbol to the caller's own requested value, not the
provider's wire format. TwelveDataClient._format_symbol() (untouched)
already does this translation internally for TwelveData specifically.
There is therefore no cross-provider symbol MISMATCH to fix in
MarketCandle's own output today -- what was missing was a single,
centralized place holding each provider's translation table, instead
of one hardcoded inline in each provider file (TwelveDataClient's
_format_symbol(), BinanceProvider's SUPPORTED_SYMBOLS/no-op format).
This module is that centralized table -- read-only translation
helpers, no new format invented, no existing provider file's own
logic removed or duplicated wholesale.
"""

from typing import Dict

# GoldBot's own canonical symbol vocabulary, per provider, in the
# provider's own wire format. Mirrors, not duplicates, each provider's
# existing logic: TwelveDataClient._format_symbol() already derives
# "XAU/USD" from "XAUUSD" generically (any 6-char symbol, 3+3 split) --
# this table exists for lookup/documentation and for providers (like
# Binance) whose format isn't a generic split (no separator at all).
_TWELVEDATA_FORMAT: Dict[str, str] = {
    "XAUUSD": "XAU/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "BTCUSD": "BTC/USD",
    "ETHUSD": "ETH/USD",
}

# Binance's own format has no separator and suffixes the quote asset
# differently ("USDT", not "USD") -- see data_layer/providers/binance_provider.py's
# own SUPPORTED_SYMBOLS. GoldBot's canonical "BTCUSD" maps to Binance's
# "BTCUSDT", not a simple split.
_BINANCE_FORMAT: Dict[str, str] = {
    "BTCUSD": "BTCUSDT",
    "ETHUSD": "ETHUSDT",
}

_PROVIDER_FORMATS: Dict[str, Dict[str, str]] = {
    "twelvedata": _TWELVEDATA_FORMAT,
    "binance": _BINANCE_FORMAT,
}


def to_provider_symbol(canonical_symbol: str, provider_name: str) -> str:
    """
    Translates a GoldBot canonical symbol (e.g. "XAUUSD") into a
    provider's own wire format (e.g. "XAU/USD" for TwelveData,
    "BTCUSDT" for Binance). Falls back to the canonical symbol
    unchanged for an unmapped (symbol, provider) pair -- never raises,
    same fail-safe posture as every other Phase A/AC/Phase-59 module;
    an unmapped symbol is a caller error a live API call would itself
    reject, not something this pure lookup should crash over.
    """
    provider_table = _PROVIDER_FORMATS.get(provider_name.strip().lower(), {})
    return provider_table.get(canonical_symbol.strip().upper(), canonical_symbol)


def from_provider_symbol(provider_symbol: str, provider_name: str) -> str:
    """The exact inverse of to_provider_symbol() -- reverse lookup. Falls back to the input unchanged if not found."""
    provider_table = _PROVIDER_FORMATS.get(provider_name.strip().lower(), {})
    reverse_table = {v: k for k, v in provider_table.items()}
    return reverse_table.get(provider_symbol, provider_symbol)


def is_known_symbol(canonical_symbol: str, provider_name: str) -> bool:
    """True only if this exact (symbol, provider) pair has a real translation entry -- a genuine capability check, not a guess."""
    provider_table = _PROVIDER_FORMATS.get(provider_name.strip().lower(), {})
    return canonical_symbol.strip().upper() in provider_table
