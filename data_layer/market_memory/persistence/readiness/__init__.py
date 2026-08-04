"""data_layer/market_memory/persistence/readiness -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `readiness.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `readiness.py`.
"""
from data_layer.market_memory.persistence.readiness.readiness import (
    annotations,
    Enum,
    Any,
    Callable,
    Optional,
    Set,
    BootstrapState,
    Readiness,
    ReadinessService,
)

__all__ = [
    "annotations",
    "Enum",
    "Any",
    "Callable",
    "Optional",
    "Set",
    "BootstrapState",
    "Readiness",
    "ReadinessService",
]
