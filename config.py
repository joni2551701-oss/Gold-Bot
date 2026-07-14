import os
from datetime import timezone


class Config:
    # Timezone Config
    TIMEZONE = timezone.utc

    # Environment Detection
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Market Data Provider selection (Phase 59.1: Market Data Provider
    # Abstraction). "twelvedata" is the only implemented provider
    # today -- data/providers/get_provider() reads this to pick which
    # MarketDataProvider to construct. "mt5" is a reserved future
    # value (data/providers/mt5_provider.py is an intentional stub,
    # see docs/MARKET_PROVIDER.md) -- setting MARKET_DATA_PROVIDER=mt5
    # without ENABLE_MT5=True is rejected by get_provider(), not
    # silently accepted.
    MARKET_DATA_PROVIDER = os.getenv("MARKET_DATA_PROVIDER", "twelvedata")
    ENABLE_MT5 = os.getenv("ENABLE_MT5", "False") == "True"
    ENABLE_TWELVEDATA = os.getenv("ENABLE_TWELVEDATA", "True") == "True"

    # Base paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Database path
    DB_PATH = os.path.join(BASE_DIR, "database", "goldbot.db")

    # Timeframe fetching configuration
    TIMEFRAME_HISTORY = {
        "M5": 200,
        "M15": 200,
        "H1": 200,
        "H4": 100,
        # "Daily" added for the HTF Bias layer (Phase A2). 100 daily
        # candles is roughly 4-5 months of history -- comfortably
        # enough for context.market_structure's swing detection to
        # confirm multiple structure points, same reasoning as H4's
        # existing 100.
        "Daily": 100
    }
