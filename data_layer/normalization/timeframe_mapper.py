"""
Data Layer — Timeframe Mapper (Phase 59.3, TASK 1: Provider
Normalization).

Same rationale as symbol_mapper.py (same package) -- GoldBot's own
canonical timeframe vocabulary ("M5"/"M15"/"H1"/"H4"/"Daily") already
flows through MarketCandle.timeframe unchanged, translated internally
by each provider's own adapter (TwelveDataClient.INTERVAL_MAP,
untouched). This module centralizes the per-provider timeframe tables
for lookup/documentation and for a future provider (Binance, once
real) to reuse instead of hardcoding its own copy.
"""

from typing import Dict

# Mirrors data_layer.providers.twelve_data_client.TwelveDataClient.INTERVAL_MAP
# exactly (not imported from there -- that dict is a private
# implementation detail of TwelveDataClient's own request-building
# code, not a public contract; this is a small, disclosed, read-only
# duplication, same reasoning as compute_r_multiple() mirroring
# database/signal_record.py's _calculate_rr_ratio() formula in Phase
# 59 Preparation).
_TWELVEDATA_TIMEFRAMES: Dict[str, str] = {
    "M5": "5min",
    "M15": "15min",
    "H1": "1h",
    "H4": "4h",
    "Daily": "1day",
}

# Binance's own kline interval vocabulary for the subset
# data_layer/providers/binance_provider.py's SUPPORTED_TIMEFRAMES documents.
_BINANCE_TIMEFRAMES: Dict[str, str] = {
    "M5": "5m",
    "M15": "15m",
    "H1": "1h",
    "H4": "4h",
    "Daily": "1d",
}

_PROVIDER_TIMEFRAMES: Dict[str, Dict[str, str]] = {
    "twelvedata": _TWELVEDATA_TIMEFRAMES,
    "binance": _BINANCE_TIMEFRAMES,
}


def to_provider_timeframe(canonical_timeframe: str, provider_name: str) -> str:
    """Translates a GoldBot canonical timeframe (e.g. "M15") into a provider's own wire format (e.g. "15min"/"15m"). Falls back to the canonical value unchanged if unmapped -- never raises."""
    provider_table = _PROVIDER_TIMEFRAMES.get(provider_name.strip().lower(), {})
    return provider_table.get(canonical_timeframe, canonical_timeframe)


def from_provider_timeframe(provider_timeframe: str, provider_name: str) -> str:
    """The exact inverse of to_provider_timeframe() -- reverse lookup. Falls back to the input unchanged if not found."""
    provider_table = _PROVIDER_TIMEFRAMES.get(provider_name.strip().lower(), {})
    reverse_table = {v: k for k, v in provider_table.items()}
    return reverse_table.get(provider_timeframe, provider_timeframe)


def is_known_timeframe(canonical_timeframe: str, provider_name: str) -> bool:
    """True only if this exact (timeframe, provider) pair has a real translation entry."""
    provider_table = _PROVIDER_TIMEFRAMES.get(provider_name.strip().lower(), {})
    return canonical_timeframe in provider_table
