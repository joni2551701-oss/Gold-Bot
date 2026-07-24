"""
Integrity checks for candle series (DD-064). v1.1 Phase 1, module 6.

Detects missing candles, duplicate candles, timestamp ordering violations,
and timeframe continuity. Reusable by bootstrap and by restore (DD-071).
Uses candle_clock for the expected step. This module never imports from
any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import List, Dict

from data.twelve_data_client import Candle
from data.candle_clock import CandleClock
from data.memory.market_memory import MarketMemory


@dataclass
class IntegrityReport:
    """Result of an integrity check over one or more timeframes (DD-064)."""
    ok: bool = True
    missing: int = 0
    duplicates: int = 0
    out_of_order: int = 0
    continuity_ok: bool = True
    per_timeframe: Dict[str, dict] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "ok": self.ok, "missing": self.missing,
            "duplicates": self.duplicates, "out_of_order": self.out_of_order,
            "continuity_ok": self.continuity_ok,
            "per_timeframe": self.per_timeframe,
        }


def _check_series(candles: List[Candle], step_minutes: int) -> dict:
    duplicates = out_of_order = missing = 0
    prev = None
    seen = set()
    step = timedelta(minutes=step_minutes)
    for c in candles:
        if c.timestamp in seen:
            duplicates += 1
        seen.add(c.timestamp)
        if prev is not None:
            if c.timestamp < prev:
                out_of_order += 1
            else:
                gap = (c.timestamp - prev)
                if gap > step:
                    # number of missing windows between prev and c
                    missing += int(gap / step) - 1
        prev = c.timestamp
    return {
        "duplicates": duplicates,
        "out_of_order": out_of_order,
        "missing": missing,
        "continuity_ok": (missing == 0 and duplicates == 0 and out_of_order == 0),
        "count": len(candles),
    }


def check_series(candles: List[Candle], timeframe: str,
                 clock: CandleClock = None) -> IntegrityReport:
    """Integrity of a single timeframe's candle list."""
    clock = clock or CandleClock()
    stats = _check_series(candles, clock.minutes(timeframe))
    report = IntegrityReport(
        ok=stats["continuity_ok"],
        missing=stats["missing"], duplicates=stats["duplicates"],
        out_of_order=stats["out_of_order"],
        continuity_ok=stats["continuity_ok"],
        per_timeframe={timeframe: stats})
    return report


def check_integrity(memory: MarketMemory,
                    clock: CandleClock = None) -> IntegrityReport:
    """Integrity of every timeframe in a MarketMemory (DD-064)."""
    clock = clock or CandleClock()
    report = IntegrityReport()
    for tf in memory.timeframes():
        series = [rec.to_candle() for rec in memory.timeframe(tf).get_series()]
        stats = _check_series(series, clock.minutes(tf))
        report.per_timeframe[tf] = stats
        report.missing += stats["missing"]
        report.duplicates += stats["duplicates"]
        report.out_of_order += stats["out_of_order"]
        if not stats["continuity_ok"]:
            report.continuity_ok = False
    report.ok = report.continuity_ok
    return report
