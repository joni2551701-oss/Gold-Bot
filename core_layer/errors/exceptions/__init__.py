"""core_layer/errors/exceptions -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `exceptions.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `exceptions.py`.
"""
from core_layer.errors.exceptions.exceptions import (
    GoldBotError,
    ConfigurationError,
    ValidationError,
    DataError,
    ExternalAPIError,
    DatabaseError,
    PermissionError,
    StrategyError,
    DecisionError,
    ExecutionError,
)

__all__ = [
    "GoldBotError",
    "ConfigurationError",
    "ValidationError",
    "DataError",
    "ExternalAPIError",
    "DatabaseError",
    "PermissionError",
    "StrategyError",
    "DecisionError",
    "ExecutionError",
]
