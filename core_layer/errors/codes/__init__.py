"""core_layer/errors/codes -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `codes.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `codes.py`.
"""
from core_layer.errors.codes.codes import (
    re,
    Dict,
    CODE_PATTERN,
    CONFIG_001,
    CONFIG_002,
    DATA_001,
    DATA_002,
    API_001,
    API_002,
    API_003,
    API_004,
    DB_001,
    DB_002,
    VALIDATION_001,
    VALIDATION_002,
    PERMISSION_001,
    STRATEGY_001,
    DECISION_001,
    EXECUTION_001,
    CODE_REGISTRY,
    is_valid_code_format,
    is_known_code,
)

__all__ = [
    "re",
    "Dict",
    "CODE_PATTERN",
    "CONFIG_001",
    "CONFIG_002",
    "DATA_001",
    "DATA_002",
    "API_001",
    "API_002",
    "API_003",
    "API_004",
    "DB_001",
    "DB_002",
    "VALIDATION_001",
    "VALIDATION_002",
    "PERMISSION_001",
    "STRATEGY_001",
    "DECISION_001",
    "EXECUTION_001",
    "CODE_REGISTRY",
    "is_valid_code_format",
    "is_known_code",
]
