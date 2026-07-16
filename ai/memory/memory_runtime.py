"""
AI Layer — Memory Runtime (Phase 61.3: AI Intelligence Layer, TASK 6).

A thin facade over five namespaced `ai.memory.context_memory.ContextMemory`
instances -- Conversation/User/Trade/Learning/Market -- not five new
storage implementations. `ContextMemory` (Phase 55, confirmed unused
in production code by this phase's own TASK 1 audit) is unmodified;
this module adds no persistence, no database integration, and no new
storage primitive -- same in-process, in-memory-only posture
`ContextMemory`'s own docstring already commits to.
"""

from enum import Enum
from typing import Any, Dict, Optional

from ai.memory.context_memory import ContextMemory


class MemoryLayer(Enum):
    CONVERSATION = "CONVERSATION"
    USER = "USER"
    TRADE = "TRADE"
    LEARNING = "LEARNING"
    MARKET = "MARKET"


class MemoryRuntime:
    """Each `MemoryLayer` gets its own `ContextMemory` instance -- a key in one layer never collides with the same key in another, since each is a fully separate in-memory dict."""

    def __init__(self) -> None:
        self._layers: Dict[MemoryLayer, ContextMemory] = {layer: ContextMemory() for layer in MemoryLayer}

    def save(self, layer: MemoryLayer, key: str, value: Any) -> None:
        self._layers[layer].save(key, value)

    def load(self, layer: MemoryLayer, key: str) -> Optional[Any]:
        return self._layers[layer].load(key)

    def clear(self, layer: MemoryLayer, key: Optional[str] = None) -> None:
        """Clears one key within `layer`, or every key within `layer` if `key` is omitted -- never touches another layer."""
        self._layers[layer].clear(key)

    def clear_all(self) -> None:
        """Clears every key in every layer."""
        for memory in self._layers.values():
            memory.clear()
