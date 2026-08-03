"""
Data Layer — Data Quality Engine foundation (Phase A8).

Assesses the quality of an already-fetched candle series, producing a
structured, scored report (DataQualityResult) instead of the silent
filter-and-log behavior data_layer/live_data/market_data.py's MarketDataNormalizer
already has. It does NOT fetch data, does NOT add a new provider, and
does NOT change how core/pipeline.py's existing market-data stage
behaves -- see docs/DATA_QUALITY.md for the full contract.

Relationship to data_layer/live_data/market_data.py (read, not modified, this phase):
MarketDataNormalizer._validate_and_clean() already silently filters
out invalid-price/bad-OHLC/duplicate-timestamp candles before
core/pipeline.py ever sees them, and _detect_missing_candles() already
logs (but doesn't structurally report) a gap. Both are private
instance methods, not shared constants or reusable standalone
functions -- reusing them directly would mean either changing
market_data.py's public interface or reaching into its "private"
methods, and market_data.py already feeds the live, real M15 pipeline
path (the same caution this codebase applied to context/amd.py and
context/order_block.py in Phase A5 -- see docs/WYCKOFF.md's
"Relationship to AMD" section for the precedent). This module
therefore implements its own, independently-written checks rather
than reusing market_data.py's internals -- a small, deliberate,
documented duplication of *intent* (OHLC validity, duplicate
timestamps, gap detection), not of code. See docs/DATA_QUALITY.md's
"Relationship to market_data.py" section.

Runs on the pipeline's already-fetched, already-cleaned candle list
(post MarketDataNormalizer.get_candles()) -- "Minimal: MarketData
layerdan keyin" per the Phase A8 brief. This means checks that
market_data.py's own cleaning already handles (invalid OHLC,
duplicates) will typically find nothing on real production data; they
remain here as defense-in-depth observability (today invisible for
the M15 path -- Phase A1's audit found exactly this gap) and because
a caller could hand this function any candle list, not only one that
has already passed through MarketDataNormalizer.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Sequence

from data_layer.providers.twelve_data_client import Candle

# Kept in sync with data_layer/live_data/market_data.py's own expected_deltas and
# data_layer/providers/twelve_data_client.py's INTERVAL_MAP -- a small, deliberate,
# documented duplication (see module docstring), not reused directly
# since MarketDataNormalizer.expected_deltas is a private instance
# attribute, not a shared module-level constant.
INTERVAL_DELTAS: Dict[str, timedelta] = {
    "M5": timedelta(minutes=5),
    "M15": timedelta(minutes=15),
    "H1": timedelta(hours=1),
    "H4": timedelta(hours=4),
    "Daily": timedelta(days=1),
}

# Named point-deduction constants -- never hardcoded inline in
# assess_data_quality(), matching this codebase's established
# DecisionWeights/HTF_BIAS_SCORE_MAP convention.
INVALID_OHLC_PENALTY = 25.0
DUPLICATE_CANDLE_PENALTY = 10.0
MISSING_CANDLE_PENALTY = 15.0
TIMEFRAME_MISMATCH_PENALTY = 15.0

_PENALTIES = {
    "invalid_ohlc": INVALID_OHLC_PENALTY,
    "duplicate_candle": DUPLICATE_CANDLE_PENALTY,
    "missing_candle": MISSING_CANDLE_PENALTY,
    "timeframe_mismatch": TIMEFRAME_MISMATCH_PENALTY,
}


@dataclass(frozen=True)
class DataQualityResult:
    """
    valid: True only when `issues` is empty -- any detected issue
        makes the result invalid, regardless of score.
    score: 0-100 (matching HTFBiasResult/MarketRegimeResult's
        convention), 100 minus each detected issue's penalty, floored
        at 0. Distinct from `valid` -- score communicates *how bad*,
        valid communicates *pass/fail*.
    issues: one entry per distinct issue type found this call (not
        one per bad candle -- e.g. 100 duplicate timestamps still
        produce a single "duplicate_candle" entry). See
        docs/DATA_QUALITY.md for the full issue-name list.
    """
    valid: bool
    score: float
    issues: Sequence[str]


def assess_data_quality(candles: Sequence[Candle], interval: str) -> DataQualityResult:
    """
    Never raises: an empty candle list (e.g. the API returned []) is a
    valid, expected input -- not an exception -- and produces
    DataQualityResult(valid=False, score=0.0, issues=["empty_data"]).
    An unrecognized `interval` (not in INTERVAL_DELTAS) simply skips
    the gap/timeframe-consistency checks rather than raising.
    """
    if not candles:
        return DataQualityResult(valid=False, score=0.0, issues=("empty_data",))

    issues: List[str] = []

    for candle in candles:
        if candle.high < max(candle.open, candle.close) or candle.low > min(candle.open, candle.close):
            issues.append("invalid_ohlc")
            break  # one flag reports the issue type; doesn't enumerate every bad candle

    timestamps = [c.timestamp for c in candles]
    if len(timestamps) != len(set(timestamps)):
        issues.append("duplicate_candle")

    expected_delta = INTERVAL_DELTAS.get(interval)
    if expected_delta is not None and len(candles) >= 2:
        ordered = sorted(candles, key=lambda c: c.timestamp)
        has_gap = False
        has_mismatch = False
        for previous, current in zip(ordered, ordered[1:]):
            delta = current.timestamp - previous.timestamp
            if delta <= timedelta(0):
                continue  # same/out-of-order timestamp -- already covered by duplicate_candle above
            if expected_delta < delta < timedelta(days=1):
                has_gap = True
            elif delta < expected_delta:
                has_mismatch = True
        if has_gap:
            issues.append("missing_candle")
        if has_mismatch:
            issues.append("timeframe_mismatch")

    score = max(0.0, 100.0 - sum(_PENALTIES.get(issue, 0.0) for issue in issues))

    return DataQualityResult(valid=(len(issues) == 0), score=score, issues=tuple(issues))
