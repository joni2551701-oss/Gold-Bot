"""core_layer/pipeline/pipeline_guard -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `pipeline_guard.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `pipeline_guard.py`.
"""
from core_layer.pipeline.pipeline_guard.pipeline_guard import (
    dataclass,
    Optional,
    EmergencyManager,
    EmergencyState,
    setup_logger,
    logger,
    GuardDecision,
    PipelineGuard,
)

__all__ = [
    "dataclass",
    "Optional",
    "EmergencyManager",
    "EmergencyState",
    "setup_logger",
    "logger",
    "GuardDecision",
    "PipelineGuard",
]
