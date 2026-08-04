"""
Data Layer — Multi-Provider Validation (Phase 59.5: Historical Data
Collection & Validation Foundation, TASK 6).

Compares two providers' already-collected RawCandle lists for the
same symbol/timeframe, timestamp by timestamp, reporting close/high/
low/spread differences. Foundation only, per this task's own brief:
this module never merges, corrects, or picks a "winning" candle
between the two providers -- it only reports what it observed. Any
future auto-reconciliation (e.g. "prefer provider X when they
disagree") is explicitly out of scope here.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from database_layer.market_repository.raw_candle_models import RawCandle

# A default informational threshold for `within_tolerance` -- not
# enforced anywhere, not a validation gate, just a convenience flag a
# caller/report can filter on. 0.5 is a round number for XAUUSD's own
# price scale (a few thousand USD), not derived from any real
# cross-provider study -- a caller with a more informed tolerance
# should pass it explicitly.
DEFAULT_TOLERANCE = 0.5


@dataclass(frozen=True)
class ProviderComparison:
    """
    One row per timestamp present in BOTH candle lists -- a timestamp
    only one provider has is not comparable and is silently excluded
    (not reported as a "missing" issue; that is
    data_layer/data_validation/historical_validator.py's/backtesting_layer/statistics/gap_report.py's job, not
    this module's).
    spread_a/spread_b: each provider's own (high - low) for that
        candle -- a same-provider intra-candle range, not a bid/ask
        spread (neither provider's data in this codebase includes
        bid/ask).
    within_tolerance: abs(close_diff) <= tolerance -- informational
        only, see module docstring on why nothing acts on this flag.
    """
    symbol: str
    timeframe: str
    timestamp: datetime
    provider_a: str
    provider_b: str
    close_a: float
    close_b: float
    close_diff: float
    high_diff: float
    low_diff: float
    spread_a: float
    spread_b: float
    spread_diff: float
    within_tolerance: bool


def compare_providers(
    candles_a: Sequence['RawCandle'],
    candles_b: Sequence['RawCandle'],
    tolerance: float = DEFAULT_TOLERANCE,
) -> List[ProviderComparison]:
    """
    Never raises: no overlapping timestamps (or either list empty)
    returns an empty list, not an exception. Assumes `candles_a` and
    `candles_b` each already share one symbol/timeframe internally (a
    caller should pass one (symbol, timeframe) group per side, the
    same "caller decides the grouping" posture
    backtesting_layer/statistics/dataset_report.py's per-group loop already uses) -- if
    they don't, each pair still compares by timestamp alone and simply
    reports whichever symbol/timeframe candles_a's own candle carries.
    """
    by_timestamp: Dict[datetime, 'RawCandle'] = {c.timestamp: c for c in candles_b}

    comparisons: List[ProviderComparison] = []
    for candle_a in candles_a:
        candle_b = by_timestamp.get(candle_a.timestamp)
        if candle_b is None:
            continue

        close_diff = abs(candle_a.close - candle_b.close)
        high_diff = abs(candle_a.high - candle_b.high)
        low_diff = abs(candle_a.low - candle_b.low)
        spread_a = candle_a.high - candle_a.low
        spread_b = candle_b.high - candle_b.low

        comparisons.append(ProviderComparison(
            symbol=candle_a.symbol,
            timeframe=candle_a.timeframe,
            timestamp=candle_a.timestamp,
            provider_a=candle_a.provider,
            provider_b=candle_b.provider,
            close_a=candle_a.close,
            close_b=candle_b.close,
            close_diff=close_diff,
            high_diff=high_diff,
            low_diff=low_diff,
            spread_a=spread_a,
            spread_b=spread_b,
            spread_diff=abs(spread_a - spread_b),
            within_tolerance=close_diff <= tolerance,
        ))

    return sorted(comparisons, key=lambda c: c.timestamp)
