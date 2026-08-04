"""core_layer/gateway/version_service -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `version_service.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `version_service.py`.
"""
from core_layer.gateway.version_service.version_service import (
    annotations,
    Dict,
    CORE_VERSION,
    GATEWAY_API_VERSION,
    VersionService,
)

__all__ = [
    "annotations",
    "Dict",
    "CORE_VERSION",
    "GATEWAY_API_VERSION",
    "VersionService",
]
