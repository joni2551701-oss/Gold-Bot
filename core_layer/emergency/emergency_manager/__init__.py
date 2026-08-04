"""core_layer/emergency/emergency_manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `emergency_manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `emergency_manager.py`.
"""
from core_layer.emergency.emergency_manager.emergency_manager import (
    Optional,
    EmergencyState,
    EmergencyStateRecord,
    create_emergency_state_record,
    AuditLogRepository,
    EmergencyRepository,
    setup_logger,
    logger,
    EmergencyManager,
)

__all__ = [
    "Optional",
    "EmergencyState",
    "EmergencyStateRecord",
    "create_emergency_state_record",
    "AuditLogRepository",
    "EmergencyRepository",
    "setup_logger",
    "logger",
    "EmergencyManager",
]
