"""
ReadinessService -- the cross-cutting Readiness API (DD-065). v1.1 Phase 1,
module 6.

`get_readiness(asset)` returns one of BOOTSTRAPPING / READY / RECOVERING /
FAILED / CANCELLED. Module 6, the Event Bus (module 7), Replay (module 8)
and the Platform layer all read this one API to answer "is this asset
usable?".

Aggregates the bootstrap completion barrier (DD-063) with an explicit
"recovering" marker (set while a restore/gap-recovery is in flight). The
bootstrap object is duck-typed: it must expose `bootstrap_ready: bool` and
`progress().status` (a BootstrapState). This module never imports from any
layer above data/.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Optional, Set

from data.bootstrap.bootstrap_state import BootstrapState


class Readiness(Enum):
    BOOTSTRAPPING = "bootstrapping"
    READY = "ready"
    RECOVERING = "recovering"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReadinessService:
    """Aggregates bootstrap + recovery state into a single readiness view."""

    def __init__(self,
                 bootstrap_lookup: Optional[Callable[[str], Any]] = None):
        # bootstrap_lookup(asset) -> bootstrap object (or None)
        self._lookup = bootstrap_lookup or (lambda asset: None)
        self._recovering: Set[str] = set()

    def mark_recovering(self, asset: str) -> None:
        self._recovering.add(asset)

    def clear_recovering(self, asset: str) -> None:
        self._recovering.discard(asset)

    def get_readiness(self, asset: str) -> Readiness:
        if asset in self._recovering:
            return Readiness.RECOVERING
        bootstrap = self._lookup(asset)
        if bootstrap is None:
            return Readiness.BOOTSTRAPPING
        if getattr(bootstrap, "bootstrap_ready", False):
            return Readiness.READY
        status = bootstrap.progress().status
        if status is BootstrapState.CANCELLED:
            return Readiness.CANCELLED
        if status is BootstrapState.FAILED:
            return Readiness.FAILED
        return Readiness.BOOTSTRAPPING
