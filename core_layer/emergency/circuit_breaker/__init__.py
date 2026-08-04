"""core_layer/emergency/circuit_breaker -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `circuit_breaker.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `circuit_breaker.py`.
"""
from core_layer.emergency.circuit_breaker.circuit_breaker import (
    dataclass,
    Enum,
    Optional,
    DEFAULT_MAX_CONSECUTIVE_LOSSES,
    DEFAULT_MAX_DAILY_DRAWDOWN,
    CircuitDecision,
    CircuitBreakerInput,
    CircuitBreakerResult,
    evaluate_circuit,
)

__all__ = [
    "dataclass",
    "Enum",
    "Optional",
    "DEFAULT_MAX_CONSECUTIVE_LOSSES",
    "DEFAULT_MAX_DAILY_DRAWDOWN",
    "CircuitDecision",
    "CircuitBreakerInput",
    "CircuitBreakerResult",
    "evaluate_circuit",
]
