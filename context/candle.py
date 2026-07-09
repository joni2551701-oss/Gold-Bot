from enum import IntEnum
from data.twelve_data_client import Candle

class CandleDirection(IntEnum):
    BULLISH = 1
    BEARISH = -1
    NEUTRAL = 0

def direction(candle: Candle) -> CandleDirection:
    """Single Source of Truth for candle sentiment."""
    if candle.close > candle.open:
        return CandleDirection.BULLISH
    elif candle.close < candle.open:
        return CandleDirection.BEARISH
    return CandleDirection.NEUTRAL

def is_bullish(candle: Candle) -> bool:
    return direction(candle) == CandleDirection.BULLISH

def is_bearish(candle: Candle) -> bool:
    return direction(candle) == CandleDirection.BEARISH

def is_doji(candle: Candle, threshold: float) -> bool:
    """Returns True if the body is smaller than the provided threshold percentage of the range."""
    r_size = range_size(candle)
    if r_size == 0:
        return True
    return body_size(candle) / r_size <= threshold

def body_size(candle: Candle) -> float:
    return abs(candle.close - candle.open)

def upper_wick(candle: Candle) -> float:
    return max(0.0, candle.high - max(candle.open, candle.close))

def lower_wick(candle: Candle) -> float:
    return max(0.0, min(candle.open, candle.close) - candle.low)

def range_size(candle: Candle) -> float:
    return max(0.0, candle.high - candle.low)

def body_ratio(candle: Candle) -> float:
    r_size = range_size(candle)
    return body_size(candle) / r_size if r_size != 0 else 0.0
