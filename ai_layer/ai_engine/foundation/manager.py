"""
AI Foundation — AI Manager (TASK-AI-001: AI Foundation Activation).

The single top-level entry point the TASK-AI-000 audit found missing.
`AIManager` composes the four Foundation collaborators -- Registry,
Factory, Session Manager, Runtime -- and drives every registered
`AIComponent` through one shared lifecycle
(initialize/start/stop/shutdown) plus an aggregate `health()`. It is
the unification point: any AI capability that implements `AIComponent`
becomes Foundation-managed by being registered here, without the
Manager knowing what that capability does.

SOLID / Dependency Inversion: the Manager depends only on Foundation
interfaces and its own collaborators, all injectable (constructor
arguments default to fresh instances). It imports nothing outside
`ai/foundation/`.
"""

from typing import Optional

from ai_layer.ai_engine.foundation.factory import FoundationFactory
from ai_layer.ai_engine.foundation.interfaces import HealthReport, HealthState, LifecycleComponent
from ai_layer.ai_engine.foundation.lifecycle import LifecycleState
from ai_layer.ai_engine.foundation.registry import FoundationRegistry
from ai_layer.ai_engine.foundation.runtime import FoundationRuntime
from ai_layer.ai_engine.foundation.session import FoundationSessionManager

_WORST_FIRST = (HealthState.UNHEALTHY, HealthState.DEGRADED, HealthState.HEALTHY)


class AIManager(LifecycleComponent):
    """The AI Foundation facade. initialize/start/stop/shutdown/health drive all registered components."""

    def __init__(
        self,
        registry: Optional[FoundationRegistry] = None,
        factory: Optional[FoundationFactory] = None,
        sessions: Optional[FoundationSessionManager] = None,
        runtime: Optional[FoundationRuntime] = None,
    ) -> None:
        self.registry = registry or FoundationRegistry()
        self.factory = factory or FoundationFactory()
        self.sessions = sessions or FoundationSessionManager()
        self.runtime = runtime or FoundationRuntime()

    # -- lifecycle -----------------------------------------------------

    def initialize(self) -> None:
        """CREATED -> INITIALIZED. Initialize every registered component."""
        self.runtime.transition(LifecycleState.INITIALIZED)
        for component in self.registry.components():
            component.initialize()

    def start(self) -> None:
        """INITIALIZED/STOPPED -> STARTED. Start every registered component."""
        self.runtime.transition(LifecycleState.STARTED)
        for component in self.registry.components():
            component.start()

    def stop(self) -> None:
        """STARTED -> STOPPED. Stop every registered component."""
        self.runtime.transition(LifecycleState.STOPPED)
        for component in self.registry.components():
            component.stop()

    def shutdown(self) -> None:
        """-> SHUTDOWN (terminal). Shut every component down and clear sessions. Best-effort: one bad component never blocks the rest."""
        self.runtime.transition(LifecycleState.SHUTDOWN)
        for component in self.registry.components():
            try:
                component.shutdown()
            except Exception:
                pass
        self.sessions.clear()

    # -- health --------------------------------------------------------

    def health(self) -> HealthReport:
        """Aggregate health: rolls up every registered component, worst state wins. Never raises."""
        children = []
        for component in self.registry.components():
            try:
                children.append(component.health())
            except Exception as exc:  # a component that cannot even self-report is UNHEALTHY
                children.append(
                    HealthReport(component=component.name, state=HealthState.UNHEALTHY, detail=str(exc))
                )
        overall = self._roll_up(children)
        return HealthReport(
            component="AIManager",
            state=overall,
            detail=f"{len(children)} component(s); runtime {self.runtime.state.value}",
            children=tuple(children),
        )

    @staticmethod
    def _roll_up(children) -> HealthState:
        if not children:
            return HealthState.HEALTHY
        for state in _WORST_FIRST:
            if any(c.state is state for c in children):
                return state
        return HealthState.HEALTHY
