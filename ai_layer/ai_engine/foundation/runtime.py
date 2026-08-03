"""
AI Foundation — AI Runtime (TASK-AI-001: AI Foundation Activation).

Owns the Foundation's runtime/lifecycle state and exposes a `status()`
snapshot. Transitions are validated against
`ai_layer.ai_engine.foundation.lifecycle.is_valid_transition`; an illegal transition
raises rather than silently corrupting state. The `AIManager` drives
this runtime as it moves through initialize/start/stop/shutdown.

Depends only on stdlib and `ai_layer.ai_engine.foundation.lifecycle`.
"""

from dataclasses import dataclass
from typing import List, Tuple

from ai_layer.ai_engine.foundation.lifecycle import LifecycleState, is_valid_transition


@dataclass(frozen=True)
class FoundationRuntimeStatus:
    """
    lifecycle_state: current `LifecycleState`.
    running: True only in STARTED.
    detail: short human-readable summary.
    """
    lifecycle_state: LifecycleState
    running: bool
    detail: str = ""


class FoundationRuntime:
    """Single-owner lifecycle state machine + status snapshot. Keeps a transition history for introspection."""

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED
        self._history: List[LifecycleState] = [LifecycleState.CREATED]

    @property
    def state(self) -> LifecycleState:
        return self._state

    def transition(self, target: LifecycleState) -> None:
        """Move to `target` if allowed; raise `ValueError` otherwise (no silent corruption)."""
        if not is_valid_transition(self._state, target):
            raise ValueError(f"illegal transition: {self._state.value} -> {target.value}")
        self._state = target
        self._history.append(target)

    def status(self) -> FoundationRuntimeStatus:
        running = self._state is LifecycleState.STARTED
        return FoundationRuntimeStatus(
            lifecycle_state=self._state,
            running=running,
            detail=f"runtime is {self._state.value}",
        )

    def history(self) -> Tuple[LifecycleState, ...]:
        return tuple(self._history)
