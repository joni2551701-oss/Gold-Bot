"""
Core Errors — GoldBotError base (Phase A18).

GoldBotError is the base every module-specific exception
(core_layer/errors/exceptions.py) subclasses, so any error raised anywhere
in GoldBot -- regardless of which module raised it -- carries the
same standard payload (error_code, message, module, timestamp,
details) and serializes the same way. See docs/ERROR_HANDLING.md for
the full error flow and contracts/error_contract.md for the
specification this phase implements.

Never raised directly -- always raise a specific subclass
(ConfigurationError, ValidationError, DataError, ...).
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class GoldBotError(Exception):
    """
    code: a standard error code (e.g. "DATA_001") -- see
        core_layer/errors/codes.py for the registry.
    message: a human-readable description of what went wrong.
    module: the name of the module/component that raised this error
        (e.g. "MarketDataLayer", "TwelveDataClient") -- a plain
        string, not a Python module path, matching this phase's own
        illustrative example.
    timestamp: set automatically to the moment the error was
        constructed (UTC) -- never supplied by the caller, so it
        always reflects when the failure actually happened.
    details: optional extra structured context (e.g. the offending
        value, a request id) -- defaults to an empty dict, never
        None, so to_dict()'s shape is always the same.
    """

    def __init__(
        self,
        code: str,
        message: str,
        module: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.module = module
        self.timestamp = datetime.now(timezone.utc)
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        JSON-safe dict -- timestamp rendered as an ISO-8601 string.
        Used for logging (logger.error(error.to_dict())) and, in the
        future, Telegram alerts/monitoring/a dashboard -- see
        docs/ERROR_HANDLING.md.
        """
        return {
            "type": type(self).__name__,
            "code": self.code,
            "message": self.message,
            "module": self.module,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }

    def __str__(self) -> str:
        return f"[{self.code}] {self.message} (module={self.module})"
