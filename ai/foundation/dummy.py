"""
AI Foundation — Dummy AI Component (TASK-AI-001: AI Foundation Activation).

The Director's explicit "Current AI may remain Dummy" component: it has
no intelligence -- `status()` returns "READY" and `echo()` returns its
input unchanged. Its only job is to be a *real* `AIComponent` the
Foundation can register, create, run through its lifecycle, and
health-check, proving the Foundation works end-to-end without any LLM,
provider, or trading logic (all Forbidden this task).

Depends only on stdlib and `ai.foundation.{interfaces, lifecycle}`.
"""

from ai.foundation.interfaces import AIComponent, HealthReport, HealthState
from ai.foundation.lifecycle import LifecycleState, is_valid_transition


class DummyAIComponent(AIComponent):
    """No intelligence. status() -> "READY", echo(x) -> x. A faithful lifecycle citizen."""

    def __init__(self, name: str = "dummy") -> None:
        self._name = name
        self._state = LifecycleState.CREATED

    @property
    def name(self) -> str:
        return self._name

    def _to(self, target: LifecycleState) -> None:
        if not is_valid_transition(self._state, target):
            raise ValueError(f"{self._name}: illegal transition {self._state.value} -> {target.value}")
        self._state = target

    def initialize(self) -> None:
        self._to(LifecycleState.INITIALIZED)

    def start(self) -> None:
        self._to(LifecycleState.STARTED)

    def stop(self) -> None:
        self._to(LifecycleState.STOPPED)

    def shutdown(self) -> None:
        self._to(LifecycleState.SHUTDOWN)

    def status(self) -> str:
        return "READY" if self._state is LifecycleState.STARTED else self._state.value

    def echo(self, text: str) -> str:
        """The whole of this Dummy's 'intelligence': give back exactly what it was given."""
        return text

    def health(self) -> HealthReport:
        healthy = self._state in (LifecycleState.STARTED, LifecycleState.INITIALIZED)
        return HealthReport(
            component=self._name,
            state=HealthState.HEALTHY if healthy else HealthState.DEGRADED,
            detail=f"dummy component is {self._state.value}",
        )
