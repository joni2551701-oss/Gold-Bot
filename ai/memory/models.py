"""
AI Layer — Memory Model (Phase 63.3, TASK 2).

A structured record shape for `ai/memory/memory_runtime.py`'s new
`store()`/`recall()`/`search()`/`filter()` surface, alongside (not
replacing) `MemoryRuntime`'s existing raw `MemoryLayer`-keyed
save/load API. `MemoryEntry`'s own fields are primitives/enums only,
matching this phase's own constraint -- no `DecisionResult`,
`RiskResult`, `Trade`, `Execution`, `Position`, or MT5 object is a
valid field type here, and `ai/memory/` itself never imports any of
those (verified by the AST regression test this phase adds, same
pattern `ai/explanation/explanation_input.py`'s own regression guard
already established in Phase 63.1).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MemoryType(Enum):
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"


class MemoryPriority(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class MemoryScope(Enum):
    CONVERSATION = "CONVERSATION"
    MARKET = "MARKET"
    EDUCATION = "EDUCATION"
    USER_PREFERENCE = "USER_PREFERENCE"
    EXPLANATION_HISTORY = "EXPLANATION_HISTORY"
    KNOWLEDGE_REFERENCE = "KNOWLEDGE_REFERENCE"


@dataclass(frozen=True)
class MemoryEntry:
    """
    `value` stays `Any` -- the same permissive shape
    `ai/memory/context_memory.py`'s `ContextMemory` already commits to
    -- since a memory store cannot usefully restrict what a caller
    stores without knowing every future use case. The real,
    mechanically-checked constraint is that `ai/memory/` itself never
    imports a trading-layer type to begin with (Constitution Article
    3), not a runtime check on every stored value.
    """
    key: str
    scope: MemoryScope
    memory_type: MemoryType
    value: Any
    priority: MemoryPriority = MemoryPriority.NORMAL
