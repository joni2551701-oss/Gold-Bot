"""
Service lifecycle state machine (v1.1 Phase 1, module 10; ORDER-064
amendment 1).

Every Core service registered with the Gateway moves through an explicit
lifecycle. The Gateway only routes requests to a service in the READY
state; every other state is either not-yet-serving or no-longer-serving.

Foundation Reuse Audit (Constitution Art. 11): no existing module models a
service lifecycle -- `data/snapshots/snapshot_state.py` is a *snapshot*
lifecycle (different domain, different states), and `data/replay/
replay_state.py` is a *replay session* lifecycle. Neither can be extended
without conflating unrelated domains, so a new state machine is created.

This module is pure and dependency-free; it imports nothing from the repo.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Set


class ServiceState(Enum):
    REGISTERED = "registered"   # known to the registry, not yet started
    STARTING = "starting"       # dependencies resolved, coming up
    READY = "ready"             # serving requests (the only routable state)
    DEGRADED = "degraded"       # serving, but health policy flagged it
    STOPPING = "stopping"       # draining, no new requests
    STOPPED = "stopped"         # cleanly down
    FAILED = "failed"           # crashed / failed to start


# Legal lifecycle transitions.
_TRANSITIONS: Dict[ServiceState, Set[ServiceState]] = {
    ServiceState.REGISTERED: {ServiceState.STARTING, ServiceState.STOPPED,
                              ServiceState.FAILED},
    ServiceState.STARTING: {ServiceState.READY, ServiceState.DEGRADED,
                            ServiceState.FAILED, ServiceState.STOPPING},
    ServiceState.READY: {ServiceState.DEGRADED, ServiceState.STOPPING,
                         ServiceState.FAILED},
    ServiceState.DEGRADED: {ServiceState.READY, ServiceState.STOPPING,
                            ServiceState.FAILED},
    ServiceState.STOPPING: {ServiceState.STOPPED, ServiceState.FAILED},
    ServiceState.STOPPED: {ServiceState.STARTING},          # restart
    ServiceState.FAILED: {ServiceState.STARTING, ServiceState.STOPPED},
}


class ServiceStateError(RuntimeError):
    """Raised on an illegal service lifecycle transition."""


def can_transition(src: ServiceState, dst: ServiceState) -> bool:
    return dst in _TRANSITIONS.get(src, set())


def assert_transition(src: ServiceState, dst: ServiceState) -> None:
    if not can_transition(src, dst):
        raise ServiceStateError(
            f"illegal service transition {src.value} -> {dst.value}")
