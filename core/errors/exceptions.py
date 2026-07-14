"""
Core Errors — the nine GoldBotError subclasses (Phase A18).

One subclass per category named in this phase's brief. Each is a pure
type marker over GoldBotError -- none overrides __init__ or adds a
field; raising the right subclass is what makes `except DataError`
(vs. `except GoldBotError`) meaningful, matching
docs/ERROR_HANDLING.md's category table and
contracts/error_contract.md's proposed hierarchy (which this phase
implements).

Usage (see docs/ERROR_HANDLING.md):
    raise DataError(
        code=codes.DATA_001,
        message="Missing candle data",
        module="MarketDataLayer",
    )
"""

from core.errors.base import GoldBotError


class ConfigurationError(GoldBotError):
    """Bad or missing configuration -- an environment variable, a config.py value, a database path."""


class ValidationError(GoldBotError):
    """A schema/contract check failed -- e.g. SignalSchema, ContextSnapshotSchema."""


class DataError(GoldBotError):
    """Malformed or missing market data."""


class ExternalAPIError(GoldBotError):
    """A third-party call failed -- Twelve Data, the Telegram Bot API, a future AI provider."""


class DatabaseError(GoldBotError):
    """A persistence operation failed -- connection, write, or migration."""


class PermissionError(GoldBotError):
    """
    An actor lacked authorization -- a Telegram command, an admin
    action.

    Note: this name shadows Python's built-in PermissionError within
    any module that does `from core.errors.exceptions import
    PermissionError` (or `import *`). This is deliberate -- the name
    is this phase's own brief's exact hierarchy -- and safe: no code
    in this codebase relies on catching the built-in
    PermissionError (an OS-level file-permission error) anywhere near
    where this one would be imported. Prefer a qualified import
    (`from core.errors import exceptions as errors`) if a caller ever
    needs both in the same scope.
    """


class StrategyError(GoldBotError):
    """A strategy failed to evaluate its setup."""


class DecisionError(GoldBotError):
    """Decision Engine failed to produce a verdict."""


class ExecutionError(GoldBotError):
    """The execution layer failed to dispatch."""
