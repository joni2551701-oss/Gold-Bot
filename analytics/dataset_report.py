"""
Analytics Layer — Dataset Report (Phase 59.5: Historical Data
Collection & Validation Foundation, TASK 5).

An overview across an entire collected List[RawCandle] -- possibly
spanning multiple symbols/timeframes/providers -- matching this task's
own worked example shape:

    Provider
    Symbols
    Timeframes
    Candles
    Oldest candle
    Newest candle
    Coverage %
    Duplicates
    Missing
    Invalid

Reuses data_layer.data_validation.historical_validator.validate_historical_candles() (same
phase, TASK 3) for the duplicate/missing/invalid counts -- computed
per (symbol, timeframe) group (validate_historical_candles()'s own
missing-candle check needs one timeframe to compare against) and
summed, rather than re-implementing those three checks a third time.
coverage_pct is the one genuinely new computation here: how complete
each group's series is against how many candles the span implies,
averaged (simple mean, not candle-count-weighted -- disclosed below)
across every group.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING

from data_layer.data_validation.data_quality import INTERVAL_DELTAS
from data_layer.data_validation.historical_validator import validate_historical_candles

if TYPE_CHECKING:
    from database.raw_candle_models import RawCandle


@dataclass(frozen=True)
class DatasetReport:
    """
    providers/symbols/timeframes: sorted, distinct values present in
        the given candles -- not a catalog of what COULD exist, only
        what actually does in this dataset.
    coverage_pct: mean, across every (symbol, timeframe) group, of
        (actual candle count / expected candle count for that group's
        own [oldest, newest] span) * 100, capped at 100 per group. A
        simple mean, not weighted by each group's candle count -- a
        thin, mostly-empty group and a dense, complete group count
        equally toward this average, the same "disclosed, not hidden"
        simplification as duplicate/missing/invalid_count's own
        cross-group summation. 0.0 when no group has a recognized
        timeframe (INTERVAL_DELTAS has no entry) to compute an
        expected count against.
    """
    providers: Tuple[str, ...]
    symbols: Tuple[str, ...]
    timeframes: Tuple[str, ...]
    total_candles: int
    oldest_candle: Optional[datetime]
    newest_candle: Optional[datetime]
    coverage_pct: float
    duplicate_count: int
    missing_count: int
    invalid_count: int


def _group_key(candle: 'RawCandle') -> Tuple[str, str]:
    return (candle.symbol, candle.timeframe)


def build_dataset_report(candles: Sequence['RawCandle']) -> DatasetReport:
    """Never raises: an empty `candles` list produces an all-zero report with no oldest/newest candle, not an exception."""
    if not candles:
        return DatasetReport(
            providers=(), symbols=(), timeframes=(), total_candles=0,
            oldest_candle=None, newest_candle=None, coverage_pct=0.0,
            duplicate_count=0, missing_count=0, invalid_count=0,
        )

    providers = tuple(sorted({c.provider for c in candles}))
    symbols = tuple(sorted({c.symbol for c in candles}))
    timeframes = tuple(sorted({c.timeframe for c in candles}))

    timestamps = [c.timestamp for c in candles]
    oldest_candle = min(timestamps)
    newest_candle = max(timestamps)

    groups: Dict[Tuple[str, str], List['RawCandle']] = {}
    for c in candles:
        groups.setdefault(_group_key(c), []).append(c)

    duplicate_count = 0
    missing_count = 0
    invalid_count = 0
    coverage_values: List[float] = []

    for (symbol, timeframe), group_candles in groups.items():
        report = validate_historical_candles(group_candles, timeframe=timeframe)
        duplicate_count += report.duplicate_count
        missing_count += report.missing_count
        invalid_count += report.invalid_ohlc_count

        expected_delta = INTERVAL_DELTAS.get(timeframe)
        if expected_delta is not None and len(group_candles) >= 2:
            group_timestamps = [c.timestamp for c in group_candles]
            span = max(group_timestamps) - min(group_timestamps)
            expected_count = int(span / expected_delta) + 1
            actual_count = len(set(group_timestamps))
            if expected_count > 0:
                coverage_values.append(min(100.0, (actual_count / expected_count) * 100.0))

    coverage_pct = sum(coverage_values) / len(coverage_values) if coverage_values else 0.0

    return DatasetReport(
        providers=providers,
        symbols=symbols,
        timeframes=timeframes,
        total_candles=len(candles),
        oldest_candle=oldest_candle,
        newest_candle=newest_candle,
        coverage_pct=coverage_pct,
        duplicate_count=duplicate_count,
        missing_count=missing_count,
        invalid_count=invalid_count,
    )


def format_dataset_report(report: DatasetReport) -> str:
    """Text-format rendering matching this task's own worked example field order exactly -- a pure formatting function, no computation."""
    lines = [
        f"Provider: {', '.join(report.providers) if report.providers else 'N/A'}",
        f"Symbols: {', '.join(report.symbols) if report.symbols else 'N/A'}",
        f"Timeframes: {', '.join(report.timeframes) if report.timeframes else 'N/A'}",
        f"Candles: {report.total_candles}",
        f"Oldest candle: {report.oldest_candle.isoformat() if report.oldest_candle else 'N/A'}",
        f"Newest candle: {report.newest_candle.isoformat() if report.newest_candle else 'N/A'}",
        f"Coverage %: {report.coverage_pct:.1f}",
        f"Duplicates: {report.duplicate_count}",
        f"Missing: {report.missing_count}",
        f"Invalid: {report.invalid_count}",
    ]
    return "\n".join(lines)
