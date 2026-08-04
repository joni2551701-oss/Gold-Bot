"""core_layer/gateway/metrics_service -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `metrics_service.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `metrics_service.py`.
"""
from core_layer.gateway.metrics_service.metrics_service import (
    annotations,
    Dict,
    GatewayResponse,
    GatewayStatus,
    GatewayMetrics,
)

__all__ = [
    "annotations",
    "Dict",
    "GatewayResponse",
    "GatewayStatus",
    "GatewayMetrics",
]
