"""
Gateway events (v1.1 Phase 1, module 10).

The Gateway announces what it does through a sink of small, self-describing
GatewayEvent values. The sink is injected (default: none), so the Gateway
never imports the Event Bus (`data/events`) directly -- that would invert
the dependency, since `core/` is imported by `data/`, not the reverse. A
future data-layer bridge maps these onto the bus's canonical `GATEWAY.*`
`EventType`s (already reserved in `data/events/event_model.py`), exactly as
network transport is deferred: the Gateway stays infrastructure-independent.

Imports only the stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, Optional


class GatewayEventName(Enum):
    REQUEST_RECEIVED = "GATEWAY.REQUEST_RECEIVED"
    AUTHENTICATED = "GATEWAY.AUTHENTICATED"
    REJECTED = "GATEWAY.REJECTED"
    DISPATCHED = "GATEWAY.DISPATCHED"
    COMPLETED = "GATEWAY.COMPLETED"
    RATE_LIMITED = "GATEWAY.RATE_LIMITED"
    CIRCUIT_OPENED = "GATEWAY.CIRCUIT_OPENED"
    SERVICE_REGISTERED = "GATEWAY.SERVICE_REGISTERED"
    SERVICE_UNAVAILABLE = "GATEWAY.SERVICE_UNAVAILABLE"


@dataclass(frozen=True)
class GatewayEvent:
    name: GatewayEventName
    request_id: str = ""
    correlation_id: str = ""
    service: str = ""
    status: str = ""
    timestamp: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)


EventSink = Callable[[GatewayEvent], None]
