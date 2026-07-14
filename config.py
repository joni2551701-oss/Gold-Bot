import os
from datetime import timezone


class Config:
    # Timezone Config
    TIMEZONE = timezone.utc

    # Environment Detection
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False") == "True"

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
