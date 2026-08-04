"""
Configuration Layer — settings model (Phase A13).

ApplicationSettings is a standard model that could, in the future,
replace ad-hoc config.Config.* attribute reads across the codebase.
config.py itself is untouched by this phase -- see
docs/CONFIGURATION_MANAGEMENT.md's "Existing config compatibility"
section for why this is additive, not a rewrite.
"""

from dataclasses import dataclass

from config import Config
from core_layer.configuration.environment import Environment, resolve_environment

# The real symbol/timeframe this codebase already runs today
# (main.py's TradingPipeline(symbol="XAUUSD", interval="M15", ...),
# also reused by strategies/lifecycle/ (Phase A11) and assets/
# (Phase A12)). config.py has no SYMBOL/DEFAULT_TIMEFRAME constant of
# its own to read -- these are the same literals main.py itself uses,
# not a new invention.
_DEFAULT_SYMBOL = "XAUUSD"
_DEFAULT_TIMEFRAME = "M15"


@dataclass(frozen=True)
class ApplicationSettings:
    """
    environment: Environment (DEVELOPMENT/TESTING/PRODUCTION).
    symbol: the real ticker this codebase trades (e.g. "XAUUSD").
    default_timeframe: the real execution interval (e.g. "M15").
    timezone: a string (e.g. "UTC") -- config.Config.TIMEZONE is a
        datetime.timezone object; build_settings_from_config() below
        converts it via str(), never inventing a new value.
    """
    environment: Environment
    symbol: str
    default_timeframe: str
    timezone: str


def build_settings_from_config() -> ApplicationSettings:
    """
    The minimal adapter from the existing config.Config to
    ApplicationSettings (see docs/CONFIGURATION_MANAGEMENT.md section
    7) -- reads real, already-set values (Config.APP_ENV,
    Config.TIMEZONE) rather than inventing new ones. Never raises: an
    unrecognized Config.APP_ENV value degrades to
    Environment.DEVELOPMENT (see environment.resolve_environment()).
    """
    return ApplicationSettings(
        environment=resolve_environment(Config.APP_ENV),
        symbol=_DEFAULT_SYMBOL,
        default_timeframe=_DEFAULT_TIMEFRAME,
        timezone=str(Config.TIMEZONE),
    )
