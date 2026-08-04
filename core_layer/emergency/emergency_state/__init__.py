"""core_layer/emergency/emergency_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `emergency_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `emergency_state.py`.
"""
from core_layer.emergency.emergency_state.emergency_state import (
    dataclass,
    datetime,
    timezone,
    Enum,
    Optional,
    EmergencyState,
    EmergencyStateRecord,
    create_emergency_state_record,
)

__all__ = [
    "dataclass",
    "datetime",
    "timezone",
    "Enum",
    "Optional",
    "EmergencyState",
    "EmergencyStateRecord",
    "create_emergency_state_record",
]
