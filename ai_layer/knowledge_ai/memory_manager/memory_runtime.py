"""
AI Layer — Memory Runtime (Phase 61.3: AI Intelligence Layer, TASK 6;
extended Phase 63.3: AI Memory Intelligence Foundation, TASK 4).

A thin facade over five namespaced `ai_layer.knowledge_ai.memory_manager.context_memory.ContextMemory`
instances -- Conversation/User/Trade/Learning/Market -- not five new
storage implementations. `ContextMemory` (Phase 55, confirmed unused
in production code by this phase's own TASK 1 audit) is unmodified;
this module adds no persistence, no database integration, and no new
storage primitive -- same in-process, in-memory-only posture
`ContextMemory`'s own docstring already commits to.

Phase 63.3 (Article 9 -- LOCKed since Phase 61.3, additive-only
extension): `store()`/`recall()`/`search()`/`filter()`/`list_all()`/
`short_term()`/`long_term()`/`forget()` added alongside the original
`save`/`load`/`clear`/`clear_all`/`MemoryLayer` surface, which is
completely unchanged. Per `docs/PHASE63_3_AUDIT.md`'s own finding,
this extension exists because `MemoryRuntime` is already the one real
Manager for AI memory -- Constitution Article 11 forbids a second,
competing Manager class for the same concern, so the new
`MemoryEntry`-based query surface is added here rather than in a new
file. The brief's own example method name `clear()` is not reused for
the new entry-clearing method (that name and signature already belong
to the original, LOCKed API) -- `forget(key)` is used instead.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence

from ai_layer.knowledge_ai.memory_manager.context_memory import ContextMemory
from ai_layer.knowledge_ai.memory_manager.models import MemoryEntry, MemoryType


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
        self._entries: Dict[str, MemoryEntry] = {}

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

    # --- Phase 63.3 TASK 4: structured MemoryEntry surface, additive only ---

    def store(self, entry: MemoryEntry) -> None:
        """Stores `entry` under its own `key`, overwriting any existing entry with that key."""
        self._entries[entry.key] = entry

    def recall(self, key: str) -> Optional[MemoryEntry]:
        """Never raises: an unknown key returns None rather than a fabricated entry."""
        return self._entries.get(key)

    def search(self, query: str) -> Sequence[MemoryEntry]:
        """Case-insensitive substring match over each entry's own key."""
        normalized = query.lower().strip()
        if not normalized:
            return ()
        return tuple(entry for entry in self._entries.values() if normalized in entry.key.lower())

    def filter(self, predicate: Callable[[MemoryEntry], bool]) -> Sequence[MemoryEntry]:
        return tuple(entry for entry in self._entries.values() if predicate(entry))

    def list_all(self) -> List[MemoryEntry]:
        return list(self._entries.values())

    def short_term(self) -> Sequence[MemoryEntry]:
        return self.filter(lambda entry: entry.memory_type is MemoryType.SHORT_TERM)

    def long_term(self) -> Sequence[MemoryEntry]:
        return self.filter(lambda entry: entry.memory_type is MemoryType.LONG_TERM)

    def forget(self, key: str) -> None:
        """Removes one stored `MemoryEntry` by key. Never raises: forgetting an unknown key is a no-op."""
        self._entries.pop(key, None)
