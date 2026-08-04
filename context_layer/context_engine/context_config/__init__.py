"""context_layer/context_engine/context_config -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `context_config.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `context_config.py`.
"""
from context_layer.context_engine.context_config.context_config import (
    dataclass,
    ContextConfig,
)

__all__ = [
    "dataclass",
    "ContextConfig",
]
