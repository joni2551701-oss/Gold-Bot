"""
Gateway request context (v1.1 Phase 1, module 10; ORDER-064 amendment 4).

Every dispatched request is wrapped in a GatewayContext carrying the
standard fields Logging and Monitoring need: request id, correlation id,
principal, timestamp, versions and metadata. Handlers receive the context
as their first argument, so cross-cutting concerns never leak into service
logic.

Pure; imports only sibling gateway value types.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

from core.gateway.gateway_request import Principal

_COUNTER = itertools.count(1)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _default_request_id() -> str:
    return f"gw-{next(_COUNTER)}"


@dataclass(frozen=True)
class GatewayContext:
    request_id: str
    correlation_id: str
    principal: Principal
    timestamp: datetime
    service: str
    core_version: str = ""
    api_version: str = ""
    metadata: dict = field(default_factory=dict)


def new_context(service: str, principal: Principal, now: datetime,
                correlation_id: Optional[str] = None,
                core_version: str = "", api_version: str = "",
                request_id_factory: Callable[[], str] = _default_request_id,
                metadata: Optional[dict] = None) -> GatewayContext:
    request_id = request_id_factory()
    return GatewayContext(
        request_id=request_id,
        correlation_id=correlation_id or request_id,
        principal=principal, timestamp=now, service=service,
        core_version=core_version, api_version=api_version,
        metadata=dict(metadata or {}))
