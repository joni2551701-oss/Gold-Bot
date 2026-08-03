"""
GoldBot central configuration (config.py).

TASK-CORE-001 -- Configuration Foundation.

This module is the single, central configuration source for GoldBot.
It has two layers that coexist by design:

1. `Config` (unchanged) -- the original flat settings class. Twelve
   modules and the whole test suite read `Config.DB_PATH`,
   `Config.TIMEZONE`, `Config.APP_ENV`, `Config.MARKET_DATA_PROVIDER`,
   `Config.TIMEFRAME_HISTORY`, etc. It is preserved verbatim for
   backward compatibility -- this task is additive, never a rewrite
   (CLAUDE.md: "No breaking changes", "No unnecessary refactor").

2. `Settings` (new) -- the structured, typed, go-forward central
   config the next phases (providers/, stream/, market/, context/, ...)
   build on. It is organised into the blocks the task specifies
   (Core/Provider/Stream/Market/Database/Telegram/AI/Platform/
   Monitoring/Security/FeatureFlags) and exposes a single `SETTINGS`
   singleton.

Module Reuse note (CLAUDE.md Module Reuse Principle): a structured
settings layer already existed in `configuration/settings.py`
(`ApplicationSettings`) but only carried four fields. Rather than
create a third settings home, this task grows the canonical `config.py`
the Director named, keeps `Config` for compatibility, and leaves the
existing `configuration.environment.Environment` enum as the typed
companion for `CoreConfig.mode` (its `resolve_environment()` already
maps the same raw APP_ENV string -- not duplicated here).

Secret handling: secrets are wrapped in `MaskedSecret`, whose repr/str
render `***`, so a secret value can never appear in a log line, a
`repr(settings)`, or a stack trace. Only an explicit `.reveal()` call
returns the real value. `core_layer.secrets.Secrets` remains the runtime
secret accessor existing modules use; both read the same process
environment, so there is one environment source, not two.

Environment source: `.env` (if present) is read ONLY here, by
`_load_env_file()`, and only fills variables not already set in the
process environment -- so systemd `EnvironmentFile` (VPS) and GitHub
Secrets (CI) always win. No other module reads a `.env` file. (A few
runtime modules still read individual `os.environ` values directly;
routing those through `Settings` is a follow-up migration the next
phases pick up -- see the report.)
"""

import os
from dataclasses import dataclass
from datetime import timezone
from typing import List, Optional


# ---------------------------------------------------------------------------
# .env loading (dev convenience only; production uses systemd EnvironmentFile
# and CI uses GitHub Secrets, both of which populate os.environ directly).
# ---------------------------------------------------------------------------
def _load_env_file(path: Optional[str] = None) -> None:
    """
    Load a `.env` file into os.environ IF one exists, without ever
    overriding a variable already present in the environment (so a real
    deployment's systemd/CI-provided values always take precedence). No
    external dependency (python-dotenv is intentionally not a project
    dependency). Never logs a value; failures are swallowed silently so
    a malformed dev file can never crash import of this root module.
    """
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        return


# Read .env before anything below (including the legacy Config class) reads
# the environment, so a dev .env is honoured uniformly.
_load_env_file()


# ---------------------------------------------------------------------------
# Parse helpers -- typed, defensive, never raise on bad input.
# ---------------------------------------------------------------------------
_TRUE = {"true", "1", "yes", "on", "y", "t"}
_FALSE = {"false", "0", "no", "off", "n", "f"}


def parse_bool(value: Optional[str], default: bool = False) -> bool:
    """Parse a truthy/falsey string; unknown/empty/None -> default."""
    if value is None:
        return default
    token = value.strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    return default


def parse_int(value: Optional[str], default: int = 0) -> int:
    """Parse an int; empty/None/non-numeric -> default (never raises)."""
    if value is None or value.strip() == "":
        return default
    try:
        return int(value.strip())
    except (TypeError, ValueError):
        return default


def parse_list(value: Optional[str], default: Optional[List[str]] = None,
               sep: str = ",") -> List[str]:
    """Parse a separated list; empty/None -> a copy of default (or [])."""
    if value is None or value.strip() == "":
        return list(default) if default else []
    return [item.strip() for item in value.split(sep) if item.strip()]


def _env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Single point where a raw environment variable is read for Settings."""
    return os.environ.get(key, default)


# ---------------------------------------------------------------------------
# Secret masking -- a value that can never be logged by accident.
# ---------------------------------------------------------------------------
class MaskedSecret:
    """
    Holds a secret value read from the environment. Its repr/str render
    `***` (or `unset`), so the real value can never leak into a log, a
    `repr(settings)`, or a traceback. Call `.reveal()` to obtain the
    real value explicitly (returns None when unset). Truthiness reflects
    presence, so `if settings.ai.gemini_api_key:` works without
    revealing anything.
    """

    __slots__ = ("_value",)

    def __init__(self, value: Optional[str]) -> None:
        self._value = value if value else None

    @property
    def is_set(self) -> bool:
        return self._value is not None

    def reveal(self) -> Optional[str]:
        return self._value

    def __bool__(self) -> bool:
        return self.is_set

    def __repr__(self) -> str:
        return "MaskedSecret(***)" if self._value else "MaskedSecret(unset)"

    __str__ = __repr__


def _masked(key: str) -> MaskedSecret:
    """Build a MaskedSecret from an environment variable (never logged)."""
    return MaskedSecret(os.environ.get(key) or None)


class ConfigError(Exception):
    """Raised by validate_required() when required settings are missing."""


# ---------------------------------------------------------------------------
# Legacy flat config -- PRESERVED VERBATIM for backward compatibility.
# Twelve modules + the test suite depend on these exact attributes.
# ---------------------------------------------------------------------------
class Config:
    # Timezone Config
    TIMEZONE = timezone.utc

    # Environment Detection
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Market Data Provider selection (Phase 59.1: Market Data Provider
    # Abstraction). "twelvedata" is the only implemented provider
    # today -- data_layer/providers/get_provider() reads this to pick which
    # MarketDataProvider to construct. "mt5" is a reserved future
    # value (data_layer/providers/mt5_provider.py is an intentional stub,
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

    # Phase 60.8 briefly added ENABLE_SIGNALS/ENABLE_AI/ENABLE_EXECUTION/
    # ENABLE_DATABASE here as PipelineGuard stage gates. Phase 60.9
    # (Runtime Registry Separation) removed all four -- Trading-pipeline
    # stage gating is now EmergencyManager's job exclusively
    # (core_layer/pipeline/pipeline_guard.py never reads config.Config for any
    # of its four hooks). See docs/FEATURE_REGISTRY_SEPARATION.md.

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


# ---------------------------------------------------------------------------
# Structured configuration blocks (new). All frozen dataclasses; secret
# fields are MaskedSecret so no block's repr can ever leak a secret.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CoreConfig:
    app_name: str
    mode: str            # development / staging / production (raw APP_ENV)
    version: str
    debug: bool
    timezone: str        # e.g. "UTC" (Config.TIMEZONE is the tz object)


@dataclass(frozen=True)
class ProviderConfig:
    market_data_provider: str
    enable_twelvedata: bool
    enable_mt5: bool
    enable_bitget: bool
    enable_binance: bool
    enable_keynorq: bool
    twelve_data_api_key: MaskedSecret
    bitget_api_key: MaskedSecret
    binance_api_key: MaskedSecret
    keynorq_api_key: MaskedSecret


@dataclass(frozen=True)
class StreamConfig:
    stream_interval: int
    polling_interval: int
    cache_size: int
    reconnect_policy: str


@dataclass(frozen=True)
class MarketConfig:
    default_symbol: str
    supported_symbols: List[str]
    supported_timeframes: List[str]


@dataclass(frozen=True)
class DatabaseConfig:
    path: str
    url: str
    migration_mode: str


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: MaskedSecret
    owner_id: str        # a user id, not a secret
    chat_ids: List[str]
    polling_enabled: bool
    polling_interval: int


@dataclass(frozen=True)
class AIConfig:
    enabled: bool
    provider: str
    model_name: str
    gemini_api_key: MaskedSecret


@dataclass(frozen=True)
class PlatformConfig:
    platform_mode: str
    enable_telegram: bool
    enable_mini_app: bool     # TG Mini App
    enable_ios: bool
    enable_android: bool      # APK / Android
    enable_desktop: bool


@dataclass(frozen=True)
class MonitoringConfig:
    log_level: str
    health_check_interval: int
    metrics_enabled: bool


@dataclass(frozen=True)
class SecurityConfig:
    secret_masking: bool
    allowed_hosts: List[str]
    safe_mode: bool


@dataclass(frozen=True)
class FeatureFlags:
    current_price: bool
    signals: bool
    ai_analysis: bool
    telegram_notifications: bool
    market_history: bool
    chart_support: bool


# The three required secrets (mirrors scripts/health_check.py's own
# required set) -- the minimum a real deployment must provide.
REQUIRED_SECRET_ENV = ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TWELVE_DATA_API_KEY")


@dataclass(frozen=True)
class Settings:
    """
    The single, central, structured configuration object. Built once at
    import as `SETTINGS`; rebuildable via `build_settings()` (tests set
    env then rebuild). Its repr masks every secret (MaskedSecret).
    """
    core: CoreConfig
    providers: ProviderConfig
    stream: StreamConfig
    market: MarketConfig
    database: DatabaseConfig
    telegram: TelegramConfig
    ai: AIConfig
    platform: PlatformConfig
    monitoring: MonitoringConfig
    security: SecurityConfig
    features: FeatureFlags

    def required_missing(self) -> List[str]:
        """Names of REQUIRED_SECRET_ENV variables absent from the environment (names only, never values)."""
        return [name for name in REQUIRED_SECRET_ENV if not (os.environ.get(name) or "").strip()]

    def validate_required(self, raise_error: bool = False) -> List[str]:
        """
        Return the list of missing required variable NAMES. When
        `raise_error` is True and any are missing, raise `ConfigError`
        naming them -- values are never included in the message.
        """
        missing = self.required_missing()
        if missing and raise_error:
            raise ConfigError("Missing required configuration: " + ", ".join(missing))
        return missing


def build_settings() -> Settings:
    """
    Construct a `Settings` from the current process environment. Never
    raises (a real deployment validates explicitly via
    `SETTINGS.validate_required(raise_error=True)` at startup) -- import
    of this root module must always succeed.
    """
    return Settings(
        core=CoreConfig(
            app_name=_env("APP_NAME", "GoldBot"),
            mode=_env("APP_ENV", "development"),
            version=_env("APP_VERSION", "0.4"),
            debug=parse_bool(_env("DEBUG"), False),
            timezone=str(_env("APP_TIMEZONE", "UTC")),
        ),
        providers=ProviderConfig(
            market_data_provider=_env("MARKET_DATA_PROVIDER", "twelvedata"),
            enable_twelvedata=parse_bool(_env("ENABLE_TWELVEDATA"), True),
            enable_mt5=parse_bool(_env("ENABLE_MT5"), False),
            enable_bitget=parse_bool(_env("ENABLE_BITGET"), False),
            enable_binance=parse_bool(_env("ENABLE_BINANCE"), False),
            enable_keynorq=parse_bool(_env("ENABLE_KEYNORQ"), False),
            twelve_data_api_key=_masked("TWELVE_DATA_API_KEY"),
            bitget_api_key=_masked("BITGET_API_KEY"),
            binance_api_key=_masked("BINANCE_API_KEY"),
            keynorq_api_key=_masked("KEYNORQ_API_KEY"),
        ),
        stream=StreamConfig(
            stream_interval=parse_int(_env("STREAM_INTERVAL"), 5),
            polling_interval=parse_int(_env("POLLING_INTERVAL"), 60),
            cache_size=parse_int(_env("CACHE_SIZE"), 500),
            reconnect_policy=_env("RECONNECT_POLICY", "exponential"),
        ),
        market=MarketConfig(
            default_symbol=_env("DEFAULT_SYMBOL", "XAUUSD"),
            supported_symbols=parse_list(_env("SUPPORTED_SYMBOLS"), ["XAUUSD"]),
            supported_timeframes=parse_list(
                _env("SUPPORTED_TIMEFRAMES"), ["M5", "M15", "H1", "H4", "Daily"]),
        ),
        database=DatabaseConfig(
            path=_env("DB_PATH", Config.DB_PATH),
            url=_env("DATABASE_URL", ""),
            migration_mode=_env("DB_MIGRATION_MODE", "auto"),
        ),
        telegram=TelegramConfig(
            bot_token=_masked("TELEGRAM_BOT_TOKEN"),
            owner_id=_env("TELEGRAM_OWNER_ID", ""),
            chat_ids=parse_list(_env("TELEGRAM_CHAT_IDS", _env("TELEGRAM_CHAT_ID", "")), []),
            polling_enabled=parse_bool(_env("TELEGRAM_POLLING_ENABLED"), True),
            polling_interval=parse_int(_env("TELEGRAM_POLLING_INTERVAL"), 2),
        ),
        ai=AIConfig(
            enabled=parse_bool(_env("AI_ENABLED"), False),
            provider=_env("AI_PROVIDER", "gemini"),
            model_name=_env("AI_MODEL", "gemini-2.5-flash"),
            gemini_api_key=_masked("GEMINI_API_KEY"),
        ),
        platform=PlatformConfig(
            platform_mode=_env("PLATFORM_MODE", "telegram"),
            enable_telegram=parse_bool(_env("ENABLE_PLATFORM_TELEGRAM"), True),
            enable_mini_app=parse_bool(_env("ENABLE_PLATFORM_MINI_APP"), False),
            enable_ios=parse_bool(_env("ENABLE_PLATFORM_IOS"), False),
            enable_android=parse_bool(_env("ENABLE_PLATFORM_ANDROID"), False),
            enable_desktop=parse_bool(_env("ENABLE_PLATFORM_DESKTOP"), False),
        ),
        monitoring=MonitoringConfig(
            log_level=_env("LOG_LEVEL", "INFO"),
            health_check_interval=parse_int(_env("HEALTH_CHECK_INTERVAL"), 300),
            metrics_enabled=parse_bool(_env("METRICS_ENABLED"), False),
        ),
        security=SecurityConfig(
            secret_masking=parse_bool(_env("SECRET_MASKING"), True),
            allowed_hosts=parse_list(_env("ALLOWED_HOSTS"), []),
            safe_mode=parse_bool(_env("SAFE_MODE"), True),
        ),
        features=FeatureFlags(
            current_price=parse_bool(_env("FEATURE_CURRENT_PRICE"), True),
            signals=parse_bool(_env("FEATURE_SIGNALS"), True),
            ai_analysis=parse_bool(_env("FEATURE_AI_ANALYSIS"), False),
            telegram_notifications=parse_bool(_env("FEATURE_TELEGRAM_NOTIFICATIONS"), True),
            market_history=parse_bool(_env("FEATURE_MARKET_HISTORY"), True),
            chart_support=parse_bool(_env("FEATURE_CHART_SUPPORT"), False),
        ),
    )


# The single central Settings instance every module can import:
#   from config import SETTINGS
SETTINGS = build_settings()


def get_settings() -> Settings:
    """Clean interface accessor -- returns the central SETTINGS singleton."""
    return SETTINGS
