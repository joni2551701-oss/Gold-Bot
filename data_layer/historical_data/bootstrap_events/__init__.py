"""data_layer/historical_data/bootstrap_events -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `bootstrap_events.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `bootstrap_events.py`.
"""
from data_layer.historical_data.bootstrap_events.bootstrap_events import (
    annotations,
    BootstrapState,
    BootstrapProgress,
    BootstrapEventHook,
)

__all__ = [
    "annotations",
    "BootstrapState",
    "BootstrapProgress",
    "BootstrapEventHook",
]
