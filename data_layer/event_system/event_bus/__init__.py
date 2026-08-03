"""data_layer.event_system.event_bus — canonical module.

Code migrated from the pre-freeze package; internals unchanged (SMR-001).

Canonical documentation: 01_Data_Layer/Event_System/EventBus/README.md
"""

from data_layer.event_system.event_bus.event_bus import (
    EventBus,
    Handler,
    Selector,
    SubscriptionHandle,
    WILDCARD,
    logger,
)

__all__ = [
    "EventBus",
    "Handler",
    "Selector",
    "SubscriptionHandle",
    "WILDCARD",
    "logger",
]
