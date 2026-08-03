"""
AI Layer — Context Window (Phase 61.0: AI Infrastructure Foundation,
TASK 7).

Bounds how many recent `ConversationTurn`s a caller sends to a future
provider call -- pure trimming logic, no I/O, no provider awareness.
"""

from typing import Sequence, Tuple

from ai_layer.ai_service.session.conversation_state import ConversationTurn


class ContextWindow:
    """`max_turns` caps the *pairs* of context sent, not a token budget -- a future phase (Phase 61.1+ Prompt System) is where token-aware trimming belongs, per the Module Reuse Principle (extend this class then, not duplicate it now)."""

    def __init__(self, max_turns: int = 20) -> None:
        if max_turns <= 0:
            raise ValueError("max_turns must be positive")
        self._max_turns = max_turns

    def trim(self, turns: Sequence[ConversationTurn]) -> Tuple[ConversationTurn, ...]:
        """Returns the most recent `max_turns` turns, oldest-first order preserved. Never raises: an empty/short `turns` is returned unchanged."""
        if len(turns) <= self._max_turns:
            return tuple(turns)
        return tuple(turns[-self._max_turns:])
