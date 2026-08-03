"""
Core Errors — standard error code registry (Phase A18).

Every code follows the same format: an uppercase category prefix, an
underscore, and a zero-padded three-digit number
(CODE_PATTERN below) -- e.g. "DATA_001". CODE_REGISTRY is the single
source of truth mapping every defined code to a short description;
tests/errors/test_error_codes.py verifies no two codes collide and
every one matches the format.

Six categories (Configuration/Data/API/Database/Validation/
Permission) come directly from this phase's own brief. Three more
(Strategy/Decision/Execution) are added here for consistency with the
nine-class GoldBotError hierarchy (core_layer/errors/exceptions.py) --
the brief's own Section 3 code list only names six categories despite
Section 1's hierarchy naming nine exception classes; without a code
prefix for Strategy/Decision/Execution, those three exception classes
would have no valid code to raise with. See
docs/ERROR_HANDLING.md's "A completed gap" note.
"""

import re
from typing import Dict

CODE_PATTERN = re.compile(r"^[A-Z]+_\d{3}$")

# Configuration
CONFIG_001 = "CONFIG_001"  # missing environment variable
CONFIG_002 = "CONFIG_002"  # invalid config value

# Data
DATA_001 = "DATA_001"  # empty/missing candle data
DATA_002 = "DATA_002"  # invalid OHLC values

# External API
API_001 = "API_001"  # request timeout
API_002 = "API_002"  # rate limit exceeded
# Added for Phase 59.1 (Market Data Provider Abstraction) TASK 5 --
# data/api_error_classifier.py's classify_empty_response()/
# classify_api_error() are the callers. The brief's own "API_TIMEOUT"/
# "API_LIMIT" labels map onto the two pre-existing codes above
# (already exactly "request timeout"/"rate limit exceeded") rather
# than being duplicated as new codes.
API_003 = "API_003"  # invalid or unsupported symbol requested
API_004 = "API_004"  # empty response (provider returned no candle data)

# Database
DB_001 = "DB_001"  # connection failed
DB_002 = "DB_002"  # migration error

# Validation
VALIDATION_001 = "VALIDATION_001"  # required field missing
VALIDATION_002 = "VALIDATION_002"  # invalid field value

# Permission
PERMISSION_001 = "PERMISSION_001"  # unauthorized action

# Strategy (not in the brief's own Section 3 list -- added for
# consistency, see module docstring)
STRATEGY_001 = "STRATEGY_001"  # strategy failed to evaluate a setup

# Decision
DECISION_001 = "DECISION_001"  # decision evaluation failed

# Execution
EXECUTION_001 = "EXECUTION_001"  # dispatch failed

# The single source of truth: every defined code, mapped to a short
# description. Adding a new code means adding it here too --
# test_error_codes.py checks CODE_REGISTRY's keys have no duplicates
# and all match CODE_PATTERN, so a typo'd or malformed code is caught
# immediately rather than discovered at raise time.
CODE_REGISTRY: Dict[str, str] = {
    CONFIG_001: "Missing environment variable",
    CONFIG_002: "Invalid configuration value",
    DATA_001: "Empty or missing candle data",
    DATA_002: "Invalid OHLC values",
    API_001: "External API request timeout",
    API_002: "External API rate limit exceeded",
    API_003: "External API invalid or unsupported symbol requested",
    API_004: "External API returned an empty response (no candle data)",
    DB_001: "Database connection failed",
    DB_002: "Database migration error",
    VALIDATION_001: "Required field missing",
    VALIDATION_002: "Invalid field value",
    PERMISSION_001: "Unauthorized action",
    STRATEGY_001: "Strategy failed to evaluate a setup",
    DECISION_001: "Decision evaluation failed",
    EXECUTION_001: "Execution dispatch failed",
}


def is_valid_code_format(code: str) -> bool:
    """True if `code` matches CODE_PATTERN -- never raises on a malformed input."""
    return bool(CODE_PATTERN.match(code))


def is_known_code(code: str) -> bool:
    """True if `code` is registered in CODE_REGISTRY."""
    return code in CODE_REGISTRY
