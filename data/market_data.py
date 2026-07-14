from typing import List, Dict
from dataclasses import dataclass, field
from datetime import timedelta
from config import Config
from data.twelve_data_client import TwelveDataClient, Candle
from core.logger import setup_logger

logger = setup_logger("MarketDataNormalizer")

@dataclass(frozen=True)
class MarketSnapshot:
    """
    Standardized container for multi-timeframe market data.
    Includes data quality metrics for Context Engine awareness.
    """
    symbol: str
    candles: Dict[str, List[Candle]] = field(default_factory=dict)
    quality: Dict[str, str] = field(default_factory=dict)

class MarketDataNormalizer:
    """
    Orchestrates data fetching and sanitizes raw market data.
    Ensures data integrity and alignment before it reaches the Context Engine.
    """
    def __init__(self):
        self.client = TwelveDataClient()
        self.expected_deltas = {
            "M5": timedelta(minutes=5),
            "M15": timedelta(minutes=15),
            "H1": timedelta(hours=1),
            "H4": timedelta(hours=4),
            # "Daily" added for the HTF Bias layer (Phase A2) so
            # get_snapshot()'s existing gap detection covers it too,
            # instead of silently skipping it (the fallback for an
            # interval missing from this dict is "no gap detection
            # performed" -- see _detect_missing_candles()).
            "Daily": timedelta(days=1)
        }

    def _validate_and_clean(self, candles: List[Candle], symbol: str, interval: str) -> List[Candle]:
        """Cleans raw candles (price integrity, OHLC relation, duplicates)."""
        cleaned = []
        seen_timestamps = set()

        for c in candles:
            if c.open <= 0 or c.high <= 0 or c.low <= 0 or c.close <= 0:
                continue
            if (c.high < c.low) or (c.high < max(c.open, c.close)) or (c.low > min(c.open, c.close)):
                continue
            if c.timestamp in seen_timestamps:
                continue

            seen_timestamps.add(c.timestamp)
            cleaned.append(c)

        return cleaned

    def _detect_missing_candles(self, candles: List[Candle], interval: str, symbol: str) -> bool:
        """
        Detects missing candles by comparing time differences against expected deltas.
        Ignores gaps >= 1 day (assumed to be weekends/holidays).
        Returns True if an unexpected intraday gap is found.
        """
        if len(candles) < 2:
            return False
            
        expected_delta = self.expected_deltas.get(interval)
        if not expected_delta:
            return False

        has_gap = False
        for i in range(1, len(candles)):
            delta = candles[i].timestamp - candles[i-1].timestamp
            
            # Agar kutilgan intervaldan katta bo'lsa va bu dam olish kuni bo'lmasa (masalan, 1 kundan kichik gap)
            if expected_delta < delta < timedelta(days=1):
                logger.warning(
                    f"[{symbol}|{interval}] Missing candle(s) detected between "
                    f"{candles[i-1].timestamp} and {candles[i].timestamp}. Gap: {delta}"
                )
                has_gap = True
                
        return has_gap

    def _verify_timeframe_alignment(self, snapshot_data: Dict[str, List[Candle]], symbol: str):
        """
        Verifies logical chronological alignment across timeframes.
        Flags if any TF is severely desynced from the others.
        """
        latest_times = {
            tf: candles[-1].timestamp for tf, candles in snapshot_data.items() if candles
        }
        
        if len(latest_times) > 1:
            max_time = max(latest_times.values())
            min_time = min(latest_times.values())
            
            # H4 eng uzun interval bo'lganligi sababli, 4 soatlik desync mantiqan qabul qilinadi.
            # Agar farq 4 soatdan oshsa, demak qaysidir API call eskirgan keshni qaytargan.
            if (max_time - min_time) > timedelta(hours=4):
                logger.warning(
                    f"[{symbol}] Timeframe misalignment detected! Latest timestamps: {latest_times}"
                )

    def get_candles(self, symbol: str, interval: str, outputsize: int) -> List[Candle]:
        try:
            raw_candles = self.client.fetch_candles(symbol, interval, outputsize)
            if not raw_candles:
                return []
            return self._validate_and_clean(raw_candles, symbol, interval)
        except Exception as e:
            logger.error(f"Failed to get normalized candles for {symbol} at {interval}: {str(e)}")
            return []

    def get_snapshot(self, symbol: str, intervals: List[str]) -> MarketSnapshot:
        """
        Fetches and normalizes data across multiple timeframes using Config sizes.
        Packages them into a MarketSnapshot with quality metrics.
        """
        snapshot_data: Dict[str, List[Candle]] = {}
        quality_data: Dict[str, str] = {}
        
        for interval in intervals:
            # Config.py'dan size'ni olamiz, topilmasa default 50
            outputsize = getattr(Config, "TIMEFRAME_HISTORY", {}).get(interval, 50)
            
            cleaned_candles = self.get_candles(symbol, interval, outputsize)
            
            if not cleaned_candles:
                logger.warning(f"Failed to populate MarketSnapshot for {symbol} at {interval}.")
                quality_data[interval] = "ERROR_NO_DATA"
                continue
                
            snapshot_data[interval] = cleaned_candles
            
            # Gap detection
            has_gap = self._detect_missing_candles(cleaned_candles, interval, symbol)
            quality_data[interval] = "WARNING_GAP" if has_gap else "OK"
            
        # Alignment check
        self._verify_timeframe_alignment(snapshot_data, symbol)
            
        return MarketSnapshot(symbol=symbol, candles=snapshot_data, quality=quality_data)
