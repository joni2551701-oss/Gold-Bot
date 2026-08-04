"""core_layer/emergency/maintenance -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `maintenance.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `maintenance.py`.
"""
from core_layer.emergency.maintenance.maintenance import (
    dataclass,
    datetime,
    timezone,
    Optional,
    MaintenanceMode,
    enable_maintenance,
    disable_maintenance,
)

__all__ = [
    "dataclass",
    "datetime",
    "timezone",
    "Optional",
    "MaintenanceMode",
    "enable_maintenance",
    "disable_maintenance",
]
