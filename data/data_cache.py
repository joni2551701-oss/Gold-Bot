import os
import json
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from data.market_data import MarketDataNormalizer, MarketSnapshot, Candle
from core.logger import setup_logger
from config import Config

logger = setup_logger("SmartDataCache")

class SmartDataCache:
    """
    Intelligent caching layer to minimize API calls.
    Persists state to disk for GitHub Actions compatibility.
    """
    def __init__(self):
        self.normalizer = MarketDataNormalizer()
        self.cache: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.request_count = 0
        self.DAILY_WARNING_LIMIT = 700
        
        # Ensure data directory exists
        self.STATE_FILE = os.path.join(Config.BASE_DIR, "data", ".cache_state.json")
        self.load_state()

    def load_state(self):
        """Loads cached candles and API count from disk."""
        if not os.path.exists(self.STATE_FILE):
            logger.info("No existing cache state found. Starting fresh.")
            return

        try:
            with open(self.STATE_FILE, "r") as f:
                data = json.load(f)

            # Reset request count if it's a new UTC day
            last_date = data.get("date_utc")
            current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if last_date == current_date:
                self.request_count = data.get("request_count", 0)
            else:
                self.request_count = 0
                logger.info(f"New UTC day ({current_date}). Resetting API counter.")

            # Deserialize cache
            cache_data = data.get("cache", {})
            for sym, intervals_dict in cache_data.items():
                self.cache[sym] = {}
                for interval, info in intervals_dict.items():
                    self.cache[sym][interval] = {
                        "quality": info["quality"],
                        "expires_at": datetime.fromisoformat(info["expires_at"]),
                        "data": [
                            Candle(
                                timestamp=datetime.fromisoformat(c["timestamp"]),
                                open=c["open"],
                                high=c["high"],
                                low=c["low"],
                                close=c["close"]
                            ) for c in info["data"]
                        ]
                    }
            logger.info("Successfully loaded cache state from disk.")
        except Exception as e:
            logger.error(f"Failed to load cache state, defaulting to fresh cache: {str(e)}")
            self.cache = {}
            self.request_count = 0

    def save_state(self):
        """Saves current cache and API count to disk."""
        try:
            cache_to_save = {}
            for sym, intervals_dict in self.cache.items():
                cache_to_save[sym] = {}
                for interval, info in intervals_dict.items():
                    cache_to_save[sym][interval] = {
                        "quality": info["quality"],
                        "expires_at": info["expires_at"].isoformat(),
                        "data": [
                            {
                                "timestamp": c.timestamp.isoformat(),
                                "open": c.open,
                                "high": c.high,
                                "low": c.low,
                                "close": c.close
                            } for c in info["data"]
                        ]
                    }

            state = {
                "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "request_count": self.request_count,
                "cache": cache_to_save
            }

            os.makedirs(os.path.dirname(self.STATE_FILE), exist_ok=True)
            with open(self.STATE_FILE, "w") as f:
                json.dump(state, f)
                
            logger.info("Successfully saved cache state to disk.")
        except Exception as e:
            logger.error(f"Failed to save cache state: {str(e)}")

    def _get_next_candle_time(self, interval: str, now: datetime) -> datetime:
        """
        Calculates the exact time the next candle opens based on the timeframe,
        adding a 15-second latency buffer for provider generation delays.
        """
        now = now.replace(second=0, microsecond=0)
        
        if interval == "M5":
            minute = (now.minute // 5) * 5
            next_time = now.replace(minute=minute) + timedelta(minutes=5)
        elif interval == "M15":
            minute = (now.minute // 15) * 15
            next_time = now.replace(minute=minute) + timedelta(minutes=15)
        elif interval == "H1":
            next_time = now.replace(minute=0) + timedelta(hours=1)
        elif interval == "H4":
            hour = (now.hour // 4) * 4
            next_time = now.replace(hour=hour, minute=0) + timedelta(hours=4)
        else:
            next_time = now + timedelta(minutes=5)
            
        # 15-second latency buffer
        return next_time + timedelta(seconds=15)

    def _check_api_limit(self, calls_to_make: int):
        """Monitors API usage and triggers warnings near the limit."""
        self.request_count += calls_to_make
        if self.request_count >= self.DAILY_WARNING_LIMIT:
            logger.warning(
                f"API Usage Warning! {self.request_count} requests made today. "
                f"Approaching daily limit of 800."
            )
        else:
            logger.info(f"API Request Count: {self.request_count}/800")

    def get_cached_snapshot(self, symbol: str, intervals: List[str]) -> MarketSnapshot:
        """
        Returns a MarketSnapshot. Fetches new data only for intervals 
        where the candle has closed; otherwise, uses cache.
        """
        now = datetime.now(timezone.utc)
        
        if symbol not in self.cache:
            self.cache[symbol] = {}

        needed_intervals = []
        
        for interval in intervals:
            cached_info = self.cache[symbol].get(interval)
            if not cached_info or now >= cached_info["expires_at"]:
                needed_intervals.append(interval)

        if needed_intervals:
            logger.info(f"[{symbol}] Cache miss/expired for {needed_intervals}. Fetching new data...")
            self._check_api_limit(len(needed_intervals))
            
            fresh_snapshot = self.normalizer.get_snapshot(symbol, needed_intervals)
            
            for interval in needed_intervals:
                self.cache[symbol][interval] = {
                    "data": fresh_snapshot.candles.get(interval, []),
                    "quality": fresh_snapshot.quality.get(interval, "ERROR"),
                    "expires_at": self._get_next_candle_time(interval, now)
                }
            
            # Save state immediately after fetching new data
            self.save_state()
        else:
            logger.info(f"[{symbol}] Cache hit for all requested intervals: {intervals}.")

        final_candles: Dict[str, List[Candle]] = {}
        final_quality: Dict[str, str] = {}
        
        for interval in intervals:
            final_candles[interval] = self.cache[symbol][interval]["data"]
            final_quality[interval] = self.cache[symbol][interval]["quality"]

        return MarketSnapshot(
            symbol=symbol,
            candles=final_candles,
            quality=final_quality
        )
