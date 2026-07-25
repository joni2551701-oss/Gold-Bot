"""
Gateway request/response model (v1.1 Phase 1, module 10).

Transport-independent (Director Decision 2): a GatewayRequest is a plain
in-process value, so the same request works whether it later arrives over
HTTP, WebSocket, gRPC or IPC. The Gateway never inspects trading content --
`payload` is opaque to it.

Pure/dependency-free within the repo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Tuple


class GatewayStatus(Enum):
    OK = "ok"
    UNAUTHENTICATED = "unauthenticated"   # caller could not be identified
    FORBIDDEN = "forbidden"               # identified, but not permitted
    NOT_FOUND = "not_found"               # no such service/capability
    UNAVAILABLE = "unavailable"           # service not READY / circuit open
    RATE_LIMITED = "rate_limited"         # too many requests
    ERROR = "error"                       # service handler raised


@dataclass(frozen=True)
class Principal:
    """Who is calling. Identity only -- no trading authority."""
    id: str = "anonymous"
    roles: Tuple[str, ...] = ()
    display: str = ""
    authenticated: bool = False

    def has_role(self, role: str) -> bool:
        return role in self.roles


ANONYMOUS = Principal()


@dataclass(frozen=True)
class GatewayRequest:
    service: str = ""                     # target service name (or "" + capability)
    action: str = ""                      # optional sub-action for the handler
    payload: Any = None                   # opaque to the Gateway
    capability: Optional[str] = None      # discover by capability instead of name
    token: Optional[str] = None           # for authentication
    correlation_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class GatewayResponse:
    status: GatewayStatus
    payload: Any = None
    error: str = ""
    service: str = ""
    request_id: str = ""
    correlation_id: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.status is GatewayStatus.OK
