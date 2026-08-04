"""
Data Layer — Candle Normalizer (Phase 59.3, TASK 1: Provider
Normalization).

Does NOT introduce a new candle type. Audit finding (see this
package's own module docstrings): data_layer/providers/base_provider.py's
MarketCandle is already GoldBot's single standard candle shape,
already carrying the caller's canonical symbol/timeframe -- adding a
second, competing "NormalizedCandle" type would duplicate it for no
reason. What MarketCandle was missing was `provider` (added in this
same phase, additive field) -- this module provides the reusable
function that stamps it, plus a batch helper, so a future provider's
own get_candles() (or a caller wrapping an older MarketCandle that
predates the `provider` field) doesn't need to hand-write the same
three-line loop.
"""

from dataclasses import replace
from typing import List

from data_layer.providers.base_provider import MarketCandle


def stamp_provider(candle: MarketCandle, provider_name: str) -> MarketCandle:
    """
    Returns a copy of `candle` with `provider` set to `provider_name`
    -- MarketCandle is frozen, so this cannot mutate in place.
    Overwrites any existing value (last stamp wins), same "swap, don't
    guard" posture as data_layer/providers/registry.py's register().
    """
    return replace(candle, provider=provider_name)


def normalize_candle_list(candles: List[MarketCandle], provider_name: str) -> List[MarketCandle]:
    """Stamps every candle in `candles` with `provider_name`. Never raises: an empty list produces an empty list."""
    return [stamp_provider(candle, provider_name) for candle in candles]
