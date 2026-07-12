import os
from datetime import timezone


class Config:
    # Timezone Config
    TIMEZONE = timezone.utc

    # Environment Detection
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Database path
    DB_PATH = os.path.join(BASE_DIR, "database", "goldbot.db")

    # Timeframe fetching configuration
    TIMEFRAME_HISTORY = {
        "M5": 200,
        "M15": 200,
        "H1": 200,
        "H4": 100
    }
