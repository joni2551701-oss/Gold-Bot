"""
Data Layer — Historical Data Integrity Validator (Phase 59.5:
Historical Data Collection & Validation Foundation, TASK 3).

Validates an already-collected List[RawCandle] (the persisted
'raw_candles' table row shape, database_layer/market_repository/raw_candle_models.py) --
missing candles, duplicate candles, timestamp ordering, future
timestamps, timezone mismatches, invalid OHLC, and provider mismatch.
Produces a structured ValidationReport. Does not fetch data, does not
write to the database, does not change data_layer/historical_data/historical_data_collector.py's
behavior.

Relationship to data_layer/data_validation/data_quality.py (Phase A8, read but not modified
here): that module's assess_data_quality() runs on
data_layer.providers.twelve_data_client.Candle (the live pipeline's in-memory,
per-cycle fetch -- no symbol/timeframe/provider of its own) and scores
a single already-fetched batch for the trading pipeline's own
market_data stage. This module runs on database.raw_candle_models.RawCandle
(the persisted, multi-symbol/multi-timeframe/multi-provider historical
archive) for a completely different consumer -- an offline dataset
audit, not a live pipeline gate -- and reports per-issue-type counts
across the whole archive, not a single 0-100 score. Two of the
underlying checks (invalid OHLC, gap detection) are intentionally
re-implemented independently rather than reused, the same "small,
disclosed duplication of intent, not code" precedent
data_layer/data_validation/data_quality.py's own docstring already established for
market_data.py -- forcing this module to depend on data_quality.py's
Candle-shaped, single-report contract would be a worse coupling than
five re-written lines. The one piece that IS safely reused is
data_layer.data_validation.data_quality.INTERVAL_DELTAS -- a public, same-package module
constant (not a private method), so importing it directly here carries
none of the coupling risk market_data.py's private methods would.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence, TYPE_CHECKING

from data_layer.data_validation.data_quality import INTERVAL_DELTAS

if TYPE_CHECKING:
    from database_layer.market_repository.raw_candle_models import RawCandle


@dataclass(frozen=True)
class ValidationReport:
    """
    total_candles: len(candles) as given -- before any de-duplication.
    missing_count: number of gap intervals detected (a single 3-hour
        gap in an M15 series with an expected 15-minute step counts as
        one gap event here -- see analytics/gap_report.py, same phase,
        for an enumeration of every individual missing timestamp).
    duplicate_count: number of timestamps that appear more than once.
    ordering_violations: number of adjacent pairs (in the order the
        list was given, not re-sorted) where the later element's
        timestamp is not strictly after the earlier one's.
    future_timestamp_count: candles whose timestamp is after "now".
    timezone_issues: candles whose timestamp is timezone-naive
        (RawCandle.timestamp is expected tz-aware throughout this
        codebase -- see database_layer/market_repository/raw_candle_models.py).
    invalid_ohlc_count: candles failing the standard OHLC sanity check
        (high must be >= max(open, close); low must be <= min(open, close)).
    provider_mismatch_count: candles whose `.provider` differs from
        `expected_provider`, when one is supplied; always 0 when
        `expected_provider` is None (nothing to compare against).
    valid: True only when every count above is 0.
    """
    total_candles: int
    missing_count: int
    duplicate_count: int
    ordering_violations: int
    future_timestamp_count: int
    timezone_issues: int
    invalid_ohlc_count: int
    provider_mismatch_count: int
    valid: bool


def validate_historical_candles(
    candles: Sequence['RawCandle'],
    timeframe: Optional[str] = None,
    expected_provider: Optional[str] = None,
) -> ValidationReport:
    """
    Never raises: an empty `candles` list produces an all-zero, valid
    report -- "nothing to check" is not an error condition.
    `timeframe` drives the missing-candle check via INTERVAL_DELTAS
    (defaults to each candle's own `.timeframe` when every candle
    shares one, else must be supplied explicitly -- an unrecognized/
    mixed timeframe simply skips the missing-candle check, same
    "unrecognized interval skips the check, doesn't raise" posture as
    data_layer.data_validation.data_quality.assess_data_quality()).
    """
    if not candles:
        return ValidationReport(
            total_candles=0, missing_count=0, duplicate_count=0,
            ordering_violations=0, future_timestamp_count=0,
            timezone_issues=0, invalid_ohlc_count=0,
            provider_mismatch_count=0, valid=True,
        )

    total = len(candles)

    timestamps = [c.timestamp for c in candles]
    duplicate_count = len(timestamps) - len(set(timestamps))

    ordering_violations = sum(
        1 for previous, current in zip(candles, candles[1:])
        if current.timestamp <= previous.timestamp
    )

    now = datetime.now(timezone.utc)
    future_timestamp_count = 0
    timezone_issues = 0
    for c in candles:
        if c.timestamp.tzinfo is None:
            timezone_issues += 1
            continue  # a naive timestamp can't be safely compared against an aware "now"
        if c.timestamp > now:
            future_timestamp_count += 1

    invalid_ohlc_count = sum(
        1 for c in candles
        if c.high < max(c.open, c.close) or c.low > min(c.open, c.close)
    )

    provider_mismatch_count = 0
    if expected_provider is not None:
        provider_mismatch_count = sum(1 for c in candles if c.provider != expected_provider)

    resolved_timeframe = timeframe
    if resolved_timeframe is None:
        distinct_timeframes = {c.timeframe for c in candles}
        resolved_timeframe = distinct_timeframes.pop() if len(distinct_timeframes) == 1 else None

    missing_count = 0
    expected_delta = INTERVAL_DELTAS.get(resolved_timeframe) if resolved_timeframe else None
    if expected_delta is not None:
        ordered = sorted(candles, key=lambda c: c.timestamp)
        for previous, current in zip(ordered, ordered[1:]):
            delta = current.timestamp - previous.timestamp
            if delta > expected_delta:
                missing_count += 1

    valid = (
        missing_count == 0 and duplicate_count == 0 and ordering_violations == 0
        and future_timestamp_count == 0 and timezone_issues == 0
        and invalid_ohlc_count == 0 and provider_mismatch_count == 0
    )

    return ValidationReport(
        total_candles=total,
        missing_count=missing_count,
        duplicate_count=duplicate_count,
        ordering_violations=ordering_violations,
        future_timestamp_count=future_timestamp_count,
        timezone_issues=timezone_issues,
        invalid_ohlc_count=invalid_ohlc_count,
        provider_mismatch_count=provider_mismatch_count,
        valid=valid,
    )
