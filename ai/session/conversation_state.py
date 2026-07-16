"""
AI Layer — Conversation State (Phase 61.0: AI Infrastructure
Foundation, TASK 7).

A `ConversationState` is one temporary conversation's turns --
explicitly not `ai/memory/context_memory.py`'s `ContextMemory`, which
is a longer-lived, arbitrary per-key store. "Session != Memory,
Session vaqtinchalik" (a session is temporary) is the brief's own
distinction; this module never imports or wraps `ContextMemory`.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Tuple


@dataclass(frozen=True)
class ConversationTurn:
    """role: "user" or "assistant" -- free text, no fixed enum, matching this module's own low-ceremony foundation posture."""
    role: str
    content: str
    at: datetime


@dataclass
class ConversationState:
    """
    Mutable (unlike most `ai/` dataclasses) because a session
    genuinely accumulates turns over its lifetime -- `session_manager.py`
    is the only intended mutator.
    """
    session_id: str
    telegram_id: str
    created_at: datetime
    turns: List[ConversationTurn] = field(default_factory=list)
    last_activity: datetime = None

    def add_turn(self, role: str, content: str) -> None:
        now = datetime.now(timezone.utc)
        self.turns.append(ConversationTurn(role=role, content=content, at=now))
        self.last_activity = now

    def history(self) -> Tuple[ConversationTurn, ...]:
        return tuple(self.turns)
