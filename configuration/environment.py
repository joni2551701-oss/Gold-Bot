"""
Configuration Layer — environment enum (Phase A13).

Three values only, per the roadmap's explicit scope -- no other value
is added. See docs/CONFIGURATION_MANAGEMENT.md for the full contract.
"""

from enum import Enum
from typing import Optional


class Environment(Enum):
    """
    DEVELOPMENT/TESTING/PRODUCTION -- lowercase values matching
    config.py's existing APP_ENV convention
    (os.getenv("APP_ENV", "development")), so Environment(value)
    round-trips with the real, already-set environment variable.
    """
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


def resolve_environment(
    raw: Optional[str],
    default: Environment = Environment.DEVELOPMENT,
) -> Environment:
    """
    Maps a raw string (e.g. config.Config.APP_ENV) to Environment.
    Never raises: a missing (None) or unrecognized value degrades to
    `default` (DEVELOPMENT) rather than crashing application startup
    -- the same fail-safe posture every other Phase A foundation
    module uses for a missing/invalid input (e.g. HTFBias.UNKNOWN,
    MarketRegime.UNKNOWN). Case-insensitive, since environment
    variables are conventionally typed in either case by operators.

    Environment(raw) itself (the enum constructor) is unchanged and
    still raises ValueError for an unrecognized value -- this function
    is a separate, explicit adapter for callers that want a safe
    default instead (see settings.py's build_settings_from_config()).
    """
    if raw is None:
        return default
    try:
        return Environment(raw.lower())
    except ValueError:
        return default
