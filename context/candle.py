from data.twelve_data_client import Candle

class CandleFeatureWrapper:
    """
    Extends the base Candle dataclass with analytical features required
    by the Context Engine.
    """
    def __init__(self, candle: Candle):
        self.candle = candle

    @property
    def is_bullish(self) -> bool:
        return self.candle.close > self.candle.open

    @property
    def is_bearish(self) -> bool:
        return self.candle.close < self.candle.open

    @property
    def body_size(self) -> float:
        return abs(self.candle.close - self.candle.open)

    @property
    def upper_wick(self) -> float:
        return self.candle.high - max(self.candle.open, self.candle.close)

    @property
    def lower_wick(self) -> float:
        return min(self.candle.open, self.candle.close) - self.candle.low

    @property
    def range_size(self) -> float:
        return self.candle.high - self.candle.low

def get_candle_features(candle: Candle) -> CandleFeatureWrapper:
    """
    Utility function to wrap a raw Candle object.
    """
    return CandleFeatureWrapper(candle)
