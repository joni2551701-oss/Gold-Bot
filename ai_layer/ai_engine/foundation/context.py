"""
AI Foundation — AI Context (TASK-AI-001: AI Foundation Activation).

The lightweight, session-scoped context the Foundation threads through
a session: exactly the Director's five fields (session_id, user_id,
language, persona_id, metadata). Immutable value object -- no
behavior, no I/O.

Naming note: the class is `FoundationContext`, not `AIContext`. A
different, unrelated `AIContext` (the AI *analysis* context carrying
market/signal/profile/history) already exists at
`ai_layer.ai_engine.context.context_snapshot.AIContext`. Per the duplicate-class-name
discipline established in TASK-AI-000A, the Foundation's context takes
a distinct, non-colliding name. `persona_id` here is a plain string
reference only -- the Foundation never builds a Persona (that is
Forbidden this task); it merely carries the id a future layer may use.

Depends only on stdlib.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class FoundationContext:
    session_id: str
    user_id: Optional[str] = None
    language: str = "en"
    persona_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
