"""
Service registry + discovery (v1.1 Phase 1, module 10; ORDER-064
amendments 2, 3).

The Gateway's directory of Core services: register a manifest+handler, look
one up by name (discovery) or by capability (amendment 2), and validate the
dependency graph (amendment 3) before startup.

Foundation Reuse Audit (Constitution Art. 11): mirrors the established
registry *shape* (`assets/asset_registry.py`, `platforms/
platform_registry.py`) -- dataclass/record + register/get/list + a factory
-- but registers Core *services*, which no existing registry does. Pattern
reused, instance new.

Imports only sibling gateway modules -- no data/, no trading layers.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from core_layer.gateway.service_manifest import ServiceManifest, ServiceKind
from core_layer.gateway.service import RegisteredService, ServiceHandler
from core_layer.gateway.dependency_graph import build_graph, validate, resolution_order


class DuplicateServiceError(ValueError):
    """Raised when registering a service name that already exists."""


class ServiceNotFoundError(KeyError):
    """Raised when discovering an unregistered service."""


class ServiceRegistry:
    def __init__(self):
        self._services: Dict[str, RegisteredService] = {}

    # -- registration ---------------------------------------------------
    def register(self, manifest: ServiceManifest,
                 handler: ServiceHandler) -> RegisteredService:
        if manifest.name in self._services:
            raise DuplicateServiceError(manifest.name)
        service = RegisteredService(manifest, handler)
        self._services[manifest.name] = service
        return service

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    # -- discovery ------------------------------------------------------
    def get(self, name: str) -> Optional[RegisteredService]:
        return self._services.get(name)

    def discover(self, name: str) -> RegisteredService:
        service = self._services.get(name)
        if service is None:
            raise ServiceNotFoundError(name)
        return service

    def all(self) -> List[RegisteredService]:
        return list(self._services.values())

    def find(self, capability: Optional[str] = None,
             kind: Optional[ServiceKind] = None) -> List[RegisteredService]:
        out = self.all()
        if capability is not None:
            out = [s for s in out if s.manifest.has_capability(capability)]
        if kind is not None:
            out = [s for s in out if s.manifest.kind is kind]
        return out

    # -- dependency graph (amendment 3) --------------------------------
    def _graph(self):
        return build_graph(s.manifest for s in self._services.values())

    def validate_dependencies(self) -> None:
        validate(self._graph())

    def startup_order(self) -> List[str]:
        return resolution_order(self._graph())
