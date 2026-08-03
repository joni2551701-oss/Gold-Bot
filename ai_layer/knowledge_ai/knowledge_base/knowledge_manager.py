"""
Knowledge Foundation — Knowledge Manager (Phase 63.2, TASK 4).

Read-only facade over `ai_layer/knowledge_ai/knowledge_base/registry.py`'s static catalog, same
Manager-over-Registry shape `ai/persona/persona_manager.py` already
established over `persona_registry.py`. `KnowledgeManager` performs no
AI reasoning, no LLM call, no network call -- lookup, search, category
filter, generic filter, and list only, over data decided at commit
time. It never imports `decision/`, `risk/`, `execution/`,
`database/`, or `telegram/`, the same zero-dependency posture
`knowledge/`'s own README already documents for every other file in
this package.
"""

from typing import Callable, List, Optional, Sequence

from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory, KnowledgeEntry
from ai_layer.knowledge_ai.knowledge_base.registry import all_entries


class KnowledgeManager:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager -- a caller/test never needs the real static registry to exercise this class."""

    def __init__(self, entries: Optional[Sequence[KnowledgeEntry]] = None) -> None:
        self._entries: Sequence[KnowledgeEntry] = tuple(entries) if entries is not None else all_entries()
        self._by_key = {entry.key: entry for entry in self._entries}

    def lookup(self, key: str) -> Optional[KnowledgeEntry]:
        """Never raises: an unknown key returns None rather than a fabricated entry."""
        return self._by_key.get(key)

    def search(self, query: str) -> Sequence[KnowledgeEntry]:
        """Case-insensitive substring match over title, summary, and tags -- same matching rule as `ai_layer/knowledge_ai/knowledge_base/registry.py`'s own module-level `search()`, applied over this instance's own entry set."""
        normalized = query.lower().strip()
        if not normalized:
            return ()
        return tuple(
            entry for entry in self._entries
            if normalized in entry.title.lower()
            or normalized in entry.summary.lower()
            or any(normalized in tag.lower() for tag in entry.tags)
        )

    def by_category(self, category: KnowledgeCategory) -> Sequence[KnowledgeEntry]:
        return tuple(entry for entry in self._entries if entry.category == category)

    def filter(self, predicate: Callable[[KnowledgeEntry], bool]) -> Sequence[KnowledgeEntry]:
        return tuple(entry for entry in self._entries if predicate(entry))

    def list_all(self) -> List[KnowledgeEntry]:
        return list(self._entries)
