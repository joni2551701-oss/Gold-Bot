"""
AI Foundation — Interfaces (TASK-AI-001: AI Foundation Activation).

Common Foundation contracts only -- **no business logic** (per the
Director's "AI Interfaces: Define common interfaces only" rule). These
are the abstractions the rest of the Foundation depends on
(Dependency Inversion): the `AIManager`, `FoundationRegistry`, and
`FoundationFactory` all speak in terms of `AIComponent`/
`LifecycleComponent`, never a concrete implementation. A future real
AI capability becomes Foundation-managed simply by implementing
`AIComponent`; today a `DummyAIComponent` does.

Depends only on stdlib.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple


class HealthState(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"


@dataclass(frozen=True)
class HealthReport:
    """
    component: the name of the component this report is about.
    state: HEALTHY / DEGRADED / UNHEALTHY.
    detail: short human-readable explanation.
    children: sub-reports, when a component aggregates others (e.g.
        `AIManager` rolls up every registered component's health).
    """
    component: str
    state: HealthState
    detail: str = ""
    children: Tuple["HealthReport", ...] = field(default_factory=tuple)


class LifecycleComponent(ABC):
    """
    The lifecycle contract every Foundation-managed unit follows.
    Implementations move through `ai.foundation.lifecycle.LifecycleState`.
    """

    @abstractmethod
    def initialize(self) -> None:
        """CREATED -> INITIALIZED. Acquire/prepare resources; do no work yet."""

    @abstractmethod
    def start(self) -> None:
        """INITIALIZED/STOPPED -> STARTED. Become ready to serve."""

    @abstractmethod
    def stop(self) -> None:
        """STARTED -> STOPPED. Pause serving; keep resources."""

    @abstractmethod
    def shutdown(self) -> None:
        """-> SHUTDOWN (terminal). Release resources; not restartable."""

    @abstractmethod
    def health(self) -> HealthReport:
        """Never raises: reports UNHEALTHY rather than throwing."""


class AIComponent(LifecycleComponent):
    """
    A registrable AI capability the `FoundationFactory` creates and the
    `FoundationRegistry` holds. Adds identity (`name`) and a
    Foundation-level readiness signal (`status`) on top of the
    lifecycle contract. Intentionally minimal -- the Foundation manages
    *capabilities* without knowing what any capability does.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique registry key for this component."""

    @abstractmethod
    def status(self) -> str:
        """A short status token (e.g. "READY"). Dummy components return "READY"."""
