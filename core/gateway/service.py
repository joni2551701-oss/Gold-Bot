"""
RegisteredService (v1.1 Phase 1, module 10).

Ties a service's manifest (amendments 2/3/6), its handler, its lifecycle
state (amendment 1) and its circuit breaker (amendment 5) into one mutable
record the registry owns. The handler signature is
`handler(context: GatewayContext, payload: Any) -> Any`; the Gateway passes
the standard context and the opaque payload, and never interprets either.

Imports only sibling gateway modules -- no data/, no trading layers.
"""

from __future__ import annotations

from typing import Any, Callable

from core.gateway.service_manifest import ServiceManifest
from core.gateway.service_state import (
    ServiceState, assert_transition,
)
from core.gateway.service_breaker import ServiceCircuitBreaker
from core.gateway.gateway_context import GatewayContext

ServiceHandler = Callable[[GatewayContext, Any], Any]


class RegisteredService:
    def __init__(self, manifest: ServiceManifest, handler: ServiceHandler):
        self.manifest = manifest
        self.handler = handler
        self.state = ServiceState.REGISTERED
        policy = manifest.health_policy
        self.breaker = ServiceCircuitBreaker(
            failure_threshold=policy.max_consecutive_failures,
            recovery_timeout=policy.recovery_timeout)

    # -- identity passthrough ------------------------------------------
    @property
    def name(self) -> str:
        return self.manifest.name

    @property
    def version(self) -> str:
        return self.manifest.version

    @property
    def capabilities(self):
        return self.manifest.capabilities

    @property
    def dependencies(self):
        return self.manifest.dependencies

    @property
    def ready(self) -> bool:
        return self.state is ServiceState.READY

    # -- lifecycle ------------------------------------------------------
    def transition(self, dst: ServiceState) -> None:
        assert_transition(self.state, dst)
        self.state = dst

    def as_dict(self) -> dict:
        return {"manifest": self.manifest.as_dict(),
                "state": self.state.value,
                "breaker": self.breaker.state.value}
