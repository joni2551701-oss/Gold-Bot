import time
import requests
from typing import List
from dataclasses import dataclass
from datetime import datetime, timezone
from core.secrets import Secrets
from core.logger import setup_logger

logger = setup_logger("TwelveDataClient")

@dataclass(frozen=True)
class Candle:
    """
    Standardized immutable dataclass for OHLC data.
    Timestamp is strictly timezone-aware (UTC).
    """
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float

class TwelveDataClient:
    """
    Data client for Twelve Data API. 
    Strictly handles data fetching; no analysis logic.
    """
    BASE_URL = "https://api.twelvedata.com/time_series"
    
    # Strictly restricted to GoldBot's approved timeframes to conserve API limits
    INTERVAL_MAP = {
        "M5": "5min",
        "M15": "15min",
        "H1": "1h",
        "H4": "4h"
    }

    def __init__(self):
        self.secrets = Secrets()
        self.api_key = self.secrets.TWELVE_DATA_API_KEY

    def _format_symbol(self, symbol: str) -> str:
        """
        Formats symbol for Twelve Data API.
        Converts "XAUUSD" to "XAU/USD".
        """
        symbol = symbol.strip().upper()
        if len(symbol) == 6 and "/" not in symbol:
            return f"{symbol[:3]}/{symbol[3:]}"
        return symbol

    def fetch_candles(self, symbol: str, interval: str, outputsize: int = 50) -> List[Candle]:
        """
        Fetches OHLC data from Twelve Data. Includes exponential backoff for rate limits.
        Automatically formats symbols like 'XAUUSD' into 'XAU/USD'.
        Raises ValueError if an unsupported interval is requested.
        """
        if interval not in self.INTERVAL_MAP:
            raise ValueError(
                f"Unsupported timeframe '{interval}'. "
                f"GoldBot strictly supports: {', '.join(self.INTERVAL_MAP.keys())}"
            )

        formatted_symbol = self._format_symbol(symbol)
        mapped_interval = self.INTERVAL_MAP[interval]
        
        params = {
            "symbol": formatted_symbol,
            "interval": mapped_interval,
            "outputsize": outputsize,
            "apikey": self.api_key
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "error":
                    error_code = data.get("code")
                    error_message = data.get("message")
                    
                    logger.warning(f"API Error (Attempt {attempt + 1}/{max_retries}): {error_code} - {error_message}")
                    
                    if error_code == 429:  # Rate limit hit
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        raise ValueError(f"Twelve Data API Error: {error_message}")

                values = data.get("values", [])
                if not values:
                    logger.warning(f"No candle data returned for {formatted_symbol} at {interval}")
                    return []

                candles = []
                for v in values:
                    # Twelve Data returns strings like "2023-10-25 14:30:00"
                    dt_obj = datetime.strptime(v["datetime"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    
                    candles.append(Candle(
                        timestamp=dt_obj,
                        open=float(v["open"]),
                        high=float(v["high"]),
                        low=float(v["low"]),
                        close=float(v["close"])
                    ))
                
                # Reverse to chronologically ascending (oldest -> newest)
                return candles[::-1]

            except requests.exceptions.RequestException as e:
                logger.error(f"Network request failed (Attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise ConnectionError(f"Failed to fetch data from Twelve Data after {max_retries} attempts.") from e
                time.sleep(2 ** attempt)

        return []
