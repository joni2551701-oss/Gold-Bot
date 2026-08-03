"""
Knowledge Foundation — Registry (Phase 61.3, TASK 3).

Aggregates every category module's `*_ENTRIES` tuple into one
lookup-by-key store. Pure in-memory composition over static data --
no I/O, no database, no live computation. `_build_index()` raises at
import time on a duplicate key across categories, the same
fail-loud-at-definition-time posture `ai/prompts/prompt_registry.py`
takes for its own version records, rather than letting a silent
duplicate shadow an earlier entry.
"""

from typing import Dict, Optional, Sequence

from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory, KnowledgeEntry
from ai_layer.knowledge_ai.knowledge_base.smc import SMC_ENTRIES
from ai_layer.knowledge_ai.knowledge_base.wyckoff import WYCKOFF_ENTRIES
from ai_layer.knowledge_ai.knowledge_base.risk import RISK_ENTRIES
from ai_layer.knowledge_ai.knowledge_base.psychology import PSYCHOLOGY_ENTRIES
from ai_layer.knowledge_ai.knowledge_base.examples import EXAMPLES_ENTRIES
from ai_layer.knowledge_ai.knowledge_base.faq import FAQ_ENTRIES

_ALL_ENTRIES: Sequence[KnowledgeEntry] = (
    *SMC_ENTRIES,
    *WYCKOFF_ENTRIES,
    *RISK_ENTRIES,
    *PSYCHOLOGY_ENTRIES,
    *EXAMPLES_ENTRIES,
    *FAQ_ENTRIES,
)


def _build_index(entries: Sequence[KnowledgeEntry]) -> Dict[str, KnowledgeEntry]:
    index: Dict[str, KnowledgeEntry] = {}
    for entry in entries:
        if entry.key in index:
            raise ValueError(f"Duplicate knowledge entry key: {entry.key!r}")
        index[entry.key] = entry
    return index


_BY_KEY: Dict[str, KnowledgeEntry] = _build_index(_ALL_ENTRIES)


def get_entry(key: str) -> Optional[KnowledgeEntry]:
    return _BY_KEY.get(key)


def entries_by_category(category: KnowledgeCategory) -> Sequence[KnowledgeEntry]:
    return tuple(entry for entry in _ALL_ENTRIES if entry.category == category)


def search(query: str) -> Sequence[KnowledgeEntry]:
    """Case-insensitive substring match over title, summary, and tags."""
    normalized = query.lower().strip()
    if not normalized:
        return ()
    return tuple(
        entry for entry in _ALL_ENTRIES
        if normalized in entry.title.lower()
        or normalized in entry.summary.lower()
        or any(normalized in tag.lower() for tag in entry.tags)
    )


def all_entries() -> Sequence[KnowledgeEntry]:
    return tuple(_ALL_ENTRIES)
