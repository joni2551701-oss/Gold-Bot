"""core_layer/configuration/environment -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `environment.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `environment.py`.
"""
from core_layer.configuration.environment.environment import (
    Enum,
    Optional,
    Environment,
    resolve_environment,
)

__all__ = [
    "Enum",
    "Optional",
    "Environment",
    "resolve_environment",
]
