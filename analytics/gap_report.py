"""
Analytics Layer — Gap Report (Phase 59.5: Historical Data Collection &
Validation Foundation, TASK 4).

Enumerates every individual missing/duplicate timestamp in an
already-collected List[RawCandle], matching this task's own worked
example shape:

    XAUUSD
    M15
    2026-07-01
    02:15 missing
    04:30 missing
    17:45 duplicate

Distinct from data_layer/data_validation/historical_validator.py (same phase, TASK 3):
that module answers "how many gap EVENTS/duplicate timestamps exist"
(a single ValidationReport count per issue type, for a pass/fail
audit). This module answers "which exact timestamps" -- a per-entry
enumeration for a human reading a report, not a count for an
automated check. Reuses data_layer.data_validation.data_quality.INTERVAL_DELTAS (the same
public, same-package constant historical_validator.py already reuses)
rather than a third copy of the timeframe->step mapping.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Tuple, TYPE_CHECKING

from data_layer.data_validation.data_quality import INTERVAL_DELTAS

if TYPE_CHECKING:
    from database.raw_candle_models import RawCandle

# A safety cap on how many individual "missing" timestamps one gap
# report will enumerate -- a single, absurdly large gap (e.g. months
# of no data) should not make this function iterate millions of
# synthetic timestamps. Capped, not raised: the report simply stops
# enumerating and GapReport.truncated reports the fact honestly.
MAX_GAP_ENTRIES = 1000


@dataclass(frozen=True)
class GapEntry:
    """gap_type: "missing" (an expected candle never arrived) or "duplicate" (a timestamp appears more than once, reported once per distinct duplicated timestamp, not once per extra occurrence)."""
    timestamp: datetime
    gap_type: str


@dataclass(frozen=True)
class GapReport:
    """
    gaps: chronologically ascending, "missing" and "duplicate" entries
        interleaved by timestamp -- not grouped by type.
    truncated: True if MAX_GAP_ENTRIES was hit while enumerating
        missing candles (duplicates are never truncated -- there can
        be at most len(candles) of them, already bounded).
    """
    symbol: str
    timeframe: str
    gaps: Tuple[GapEntry, ...]
    truncated: bool = False


def build_gap_report(
    candles: Sequence['RawCandle'],
    symbol: str,
    timeframe: str,
) -> GapReport:
    """
    Never raises: an empty `candles` list, or a `timeframe` not in
    INTERVAL_DELTAS, both produce a GapReport with no missing entries
    (nothing to enumerate against) -- duplicates are still detected
    either way, since that check needs no expected-interval knowledge.
    """
    if not candles:
        return GapReport(symbol=symbol, timeframe=timeframe, gaps=())

    ordered = sorted(candles, key=lambda c: c.timestamp)

    seen = set()
    duplicate_entries = []
    for c in ordered:
        if c.timestamp in seen:
            continue  # report each duplicated timestamp once, not once per extra occurrence
        count = sum(1 for other in ordered if other.timestamp == c.timestamp)
        if count > 1:
            duplicate_entries.append(GapEntry(timestamp=c.timestamp, gap_type="duplicate"))
        seen.add(c.timestamp)

    missing_entries = []
    truncated = False
    expected_delta = INTERVAL_DELTAS.get(timeframe)
    if expected_delta is not None:
        for previous, current in zip(ordered, ordered[1:]):
            cursor = previous.timestamp + expected_delta
            while cursor < current.timestamp:
                if len(missing_entries) >= MAX_GAP_ENTRIES:
                    truncated = True
                    break
                missing_entries.append(GapEntry(timestamp=cursor, gap_type="missing"))
                cursor += expected_delta
            if truncated:
                break

    all_entries = sorted(missing_entries + duplicate_entries, key=lambda e: e.timestamp)

    return GapReport(symbol=symbol, timeframe=timeframe, gaps=tuple(all_entries), truncated=truncated)


def format_gap_report(report: GapReport) -> str:
    """
    Text-format rendering matching this task's own worked example
    exactly: symbol, timeframe, then one date header per distinct day
    with "HH:MM gap_type" lines beneath it, in chronological order.
    """
    lines = [report.symbol, report.timeframe]

    if not report.gaps:
        lines.append("No gaps detected.")
        return "\n".join(lines)

    current_date: Optional[str] = None
    for entry in report.gaps:
        entry_date = entry.timestamp.date().isoformat()
        if entry_date != current_date:
            lines.append(entry_date)
            current_date = entry_date
        lines.append(f"{entry.timestamp.strftime('%H:%M')} {entry.gap_type}")

    if report.truncated:
        lines.append(f"... truncated at {MAX_GAP_ENTRIES} missing entries")

    return "\n".join(lines)
