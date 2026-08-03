"""
StreamValidator -- canonical per-tick validation for the Live Data
stream (TASK-ARCH-101, migrated from the legacy `stream/stream_validator.py`,
TASK-CORE-004).

Checks each canonical `data_layer.live_data.stream_event.StreamEvent` (a price
TICK: asset/price/timestamp/volume/source) for cleanliness BEFORE it is
forwarded to a sink, and returns a `ValidationResult` (valid + code +
reason) -- never raises for a data-driven problem, the same
"structured absence, not exception" posture the rest of `data/` uses.
A caller (`PriceStream`, via its optional `validator=`) drops invalid
events rather than forwarding them.

Reuse-First note (Constitution Article 7): the legacy validator also
did OHLC integrity checks, because the legacy `StreamEvent` carried
OHLC. The canonical `StreamEvent` is a single-price tick with no OHLC,
so OHLC-candle validation is NOT duplicated here -- it already lives at
its correct canonical layer, the candle level (`data_layer.live_data.market_data`'s
`_validate_and_clean` and `data_layer.data_validation.data_quality.assess_data_quality`).
This module migrates only the tick-level checks that had no canonical
home: empty, price integrity, future timestamp, duplicate, and
out-of-sequence -- preserving the legacy `ValidationResult(valid, code,
reason)` contract shape (`code` values: `empty`/`price`/`timestamp`/
`duplicate`/`sequence`).

This module never imports from any layer above data/.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from data_layer.live_data.stream_event import StreamEvent


@dataclass(frozen=True)
class ValidationResult:
    """valid: whether the event may proceed. code/reason: a short
    machine + human tag when invalid ("" when valid)."""
    valid: bool
    code: str = ""
    reason: str = ""

    def __bool__(self) -> bool:
        return self.valid


_OK = ValidationResult(True)

# How far into the future a tick timestamp may be before rejection --
# absorbs minor clock skew vs. a provider without accepting a clearly
# wrong (e.g. far-future) timestamp. Same tolerance as the legacy
# validator.
_FUTURE_TOLERANCE = timedelta(minutes=5)


class StreamValidator:
    """Stateless canonical tick checker -- the caller supplies the
    previous event for duplicate/sequence checks, so one instance is
    safe to share across assets/streams."""

    def validate(
        self,
        event: Optional[StreamEvent],
        previous: Optional[StreamEvent] = None,
        expected_asset: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> ValidationResult:
        # -- empty ----------------------------------------------------
        if event is None:
            return ValidationResult(False, "empty", "event is None")
        if not event.asset or event.timestamp is None:
            return ValidationResult(False, "empty", "missing asset or timestamp")

        # -- asset (symbol mismatch) ----------------------------------
        if expected_asset is not None and event.asset != expected_asset:
            return ValidationResult(
                False, "asset", f"asset {event.asset!r} != expected {expected_asset!r}"
            )

        # -- price integrity ------------------------------------------
        price = event.price
        if price is None or not isinstance(price, (int, float)) or not math.isfinite(price):
            return ValidationResult(False, "price", "missing or non-finite price")
        if price <= 0:
            return ValidationResult(False, "price", "non-positive price")
        if event.volume is not None and event.volume < 0:
            return ValidationResult(False, "price", "negative volume")

        # -- timestamp (future) ---------------------------------------
        reference = now or datetime.now(timezone.utc)
        ts = event.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts > reference + _FUTURE_TOLERANCE:
            return ValidationResult(False, "timestamp", "timestamp is in the future")

        # -- duplicate / sequence (vs previous) -----------------------
        if previous is not None and previous.timestamp is not None:
            prev_ts = previous.timestamp
            if prev_ts.tzinfo is None:
                prev_ts = prev_ts.replace(tzinfo=timezone.utc)
            if previous.asset == event.asset:
                if ts == prev_ts:
                    return ValidationResult(False, "duplicate", "same timestamp as previous event")
                if ts < prev_ts:
                    return ValidationResult(False, "sequence", "timestamp older than previous event")

        return _OK
