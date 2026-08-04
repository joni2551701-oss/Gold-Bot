"""
Stream Layer — Stream Validator (TASK-CORE-004).

StreamValidator checks each StreamEvent for cleanliness and
consistency BEFORE it reaches state/router/subscribers. It never
raises for a data-driven problem -- it returns a ValidationResult
(valid + reason + code), the same "structured absence, not exception"
posture the rest of the codebase uses for data conditions. A caller
(price_stream.py) drops invalid events rather than routing them.

Checks (exactly TASK-CORE-004's list):
    empty        -- event/None or missing symbol/timestamp
    symbol       -- symbol mismatch vs the expected symbol (if given)
    candle       -- OHLC broken (non-positive, or high<low, or a
                    high/low that doesn't bound open/close)
    timestamp    -- missing, or implausibly far in the future
    duplicate    -- same symbol+timeframe+timestamp as the previous event
    sequence     -- timestamp older than the previous event (out of order)

No secret is read or logged; no business logic beyond data validity.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from data_layer.live_data.stream.stream_event import StreamEvent


@dataclass(frozen=True)
class ValidationResult:
    """valid: whether the event may proceed. code/reason: a short machine + human tag when invalid ("" when valid)."""
    valid: bool
    code: str = ""
    reason: str = ""

    def __bool__(self) -> bool:
        return self.valid


_OK = ValidationResult(True)

# How far into the future a timestamp may be before it's rejected --
# absorbs minor clock skew between us and a provider without accepting
# a clearly wrong (e.g. year-ahead) timestamp.
_FUTURE_TOLERANCE = timedelta(minutes=5)


class StreamValidator:
    """Stateless checker -- the caller supplies the previous event for duplicate/sequence checks, so one validator instance is safe to share."""

    def validate(
        self,
        event: Optional[StreamEvent],
        previous: Optional[StreamEvent] = None,
        expected_symbol: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> ValidationResult:
        # -- empty ----------------------------------------------------
        if event is None:
            return ValidationResult(False, "empty", "event is None")
        if not event.symbol or event.timestamp is None:
            return ValidationResult(False, "empty", "missing symbol or timestamp")

        # -- symbol ---------------------------------------------------
        if expected_symbol is not None and event.symbol != expected_symbol:
            return ValidationResult(
                False, "symbol", f"symbol {event.symbol!r} != expected {expected_symbol!r}"
            )

        # -- candle (OHLC integrity) ----------------------------------
        ohlc = (event.open, event.high, event.low, event.close)
        if any(v is None for v in ohlc):
            return ValidationResult(False, "candle", "missing OHLC value")
        if any(v <= 0 for v in ohlc):
            return ValidationResult(False, "candle", "non-positive OHLC value")
        if event.high < event.low:
            return ValidationResult(False, "candle", "high < low")
        if event.high < event.open or event.high < event.close:
            return ValidationResult(False, "candle", "high does not bound open/close")
        if event.low > event.open or event.low > event.close:
            return ValidationResult(False, "candle", "low does not bound open/close")
        if event.volume is not None and event.volume < 0:
            return ValidationResult(False, "candle", "negative volume")

        # -- timestamp (future) ---------------------------------------
        reference = now or datetime.now(timezone.utc)
        ts = event.timestamp
        # Compare tz-aware to tz-aware; treat a naive event timestamp as UTC.
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts > reference + _FUTURE_TOLERANCE:
            return ValidationResult(False, "timestamp", "timestamp is in the future")

        # -- duplicate / sequence (vs previous) -----------------------
        if previous is not None and previous.timestamp is not None:
            prev_ts = previous.timestamp
            if prev_ts.tzinfo is None:
                prev_ts = prev_ts.replace(tzinfo=timezone.utc)
            same_series = (
                previous.symbol == event.symbol
                and previous.timeframe == event.timeframe
            )
            if same_series and ts == prev_ts:
                return ValidationResult(False, "duplicate", "same timestamp as previous event")
            if same_series and ts < prev_ts:
                return ValidationResult(False, "sequence", "timestamp older than previous event")

        return _OK
