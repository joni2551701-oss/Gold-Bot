"""core_layer/gateway/rate_limiter -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `rate_limiter.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `rate_limiter.py`.
"""
from core_layer.gateway.rate_limiter.rate_limiter import (
    annotations,
    datetime,
    Dict,
    RateLimiter,
)

__all__ = [
    "annotations",
    "datetime",
    "Dict",
    "RateLimiter",
]
