"""
Service manifest (v1.1 Phase 1, module 10; ORDER-064 amendments 2, 3, 6).

Every service registers with a manifest describing what it is, what it can
do (capabilities, amendment 2), what it needs (dependencies, amendment 3)
and how it is governed (health policy). The manifest (amendment 6) makes
Service Discovery and future Platform integration declarative.

Foundation Reuse Audit (Constitution Art. 11): no existing model describes
a registrable Core service. `platforms/platform_model.py` /
`capability_model.py` describe *platforms* (Telegram/Web/Mobile) and their
UI capabilities -- the client side -- not a Core service contract. So a new
model is created.

Pure/dependency-free within the repo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Tuple


class ServiceKind(Enum):
    INTERNAL = "internal"   # for other Core modules only
    EXTERNAL = "external"   # reachable by platforms / external clients


@dataclass(frozen=True)
class HealthPolicy:
    """How the Gateway's circuit breaker should govern this service."""
    max_consecutive_failures: int = 3
    recovery_timeout: timedelta = timedelta(seconds=30)


@dataclass(frozen=True)
class ServiceManifest:
    name: str
    version: str = "1.0.0"
    capabilities: Tuple[str, ...] = ()
    dependencies: Tuple[str, ...] = ()
    kind: ServiceKind = ServiceKind.INTERNAL
    health_policy: HealthPolicy = field(default_factory=HealthPolicy)
    owner: str = ""
    description: str = ""

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": list(self.capabilities),
            "dependencies": list(self.dependencies),
            "kind": self.kind.value,
            "health_policy": {
                "max_consecutive_failures":
                    self.health_policy.max_consecutive_failures,
                "recovery_timeout_seconds":
                    self.health_policy.recovery_timeout.total_seconds(),
            },
            "owner": self.owner,
            "description": self.description,
        }
