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

    # Real Market Validation mode (Phase 59: Real Market Validation
    # Foundation, TASK 1). A foundation flag only -- reading it does
    # not exist anywhere in core/pipeline.py yet, so setting it True
    # or False changes nothing about production behavior today. It
    # exists so a future, separately-approved wiring step (extra
    # dataset-capture logging, gating an owner validation command,
    # etc.) has a single, real switch to read instead of inventing its
    # own. Defaults False -- production behavior is the default,
    # unchanged behavior.
    VALIDATION_MODE = os.getenv("VALIDATION_MODE", "False") == "True"

    # Phase 60.8: Safe Integration Layer -- PipelineGuard stage gates
    # (core/guards/pipeline_guard.py). Each defaults to True so a
    # process with no explicit override reproduces exactly today's
    # pipeline behavior; these are new, additive runtime toggles, not
    # a change to any existing default. Distinct from the pre-existing
    # lowercase `enable_ai` (configuration/feature_flags.py's
    # FeatureFlags, reserved for a future real AI provider decision) --
    # ENABLE_AI here gates whether core/pipeline.py's own `ai` stage
    # runs at all, a different concept under a similar-looking name;
    # see docs/PIPELINE_GUARD.md's "Disclosed Findings" for why both
    # names exist rather than being merged.
    ENABLE_SIGNALS = os.getenv("ENABLE_SIGNALS", "True") == "True"
    ENABLE_AI = os.getenv("ENABLE_AI", "True") == "True"
    ENABLE_EXECUTION = os.getenv("ENABLE_EXECUTION", "True") == "True"
    ENABLE_DATABASE = os.getenv("ENABLE_DATABASE", "True") == "True"

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
