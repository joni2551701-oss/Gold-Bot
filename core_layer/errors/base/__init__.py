"""core_layer/errors/base -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `base.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `base.py`.
"""
from core_layer.errors.base.base import (
    datetime,
    timezone,
    Any,
    Dict,
    Optional,
    GoldBotError,
)

__all__ = [
    "datetime",
    "timezone",
    "Any",
    "Dict",
    "Optional",
    "GoldBotError",
]
