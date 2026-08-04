"""data_layer/event_system/event_model -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `event_model.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `event_model.py`.
"""
from data_layer.event_system.event_model.event_model import (
    annotations,
    dataclass,
    field,
    datetime,
    Enum,
    Any,
    Optional,
    EVENT_SCHEMA_VERSION,
    EventPriority,
    EventType,
    EventValidationError,
    Event,
    validate_event,
)

__all__ = [
    "annotations",
    "dataclass",
    "field",
    "datetime",
    "Enum",
    "Any",
    "Optional",
    "EVENT_SCHEMA_VERSION",
    "EventPriority",
    "EventType",
    "EventValidationError",
    "Event",
    "validate_event",
]
