"""core_layer/gateway/service_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `service_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `service_state.py`.
"""
from core_layer.gateway.service_state.service_state import (
    annotations,
    Enum,
    Dict,
    Set,
    ServiceState,
    ServiceStateError,
    can_transition,
    assert_transition,
)

__all__ = [
    "annotations",
    "Enum",
    "Dict",
    "Set",
    "ServiceState",
    "ServiceStateError",
    "can_transition",
    "assert_transition",
]
