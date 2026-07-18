"""
Knowledge Foundation — Model (Phase 61.3, TASK 3; extended Phase 63.2,
TASK 2).

A queryable knowledge base, not a live data source. `KnowledgeEntry`
restates facts this codebase already committed to elsewhere (`docs/*.md`
prose, `context/*.py` docstrings and detection rules, `risk/README.md`)
in a structured, lookup-by-key shape a future AI consumer (Explanation
Engine, TASK 7; Conversation Engine, TASK 5) can retrieve without
re-deriving them from free text on every call. No entry here computes
anything or reads live market data -- every field is a static string
decided at commit time, the same "compute now, connect later" posture
every other Phase 61.x foundation module has used.

Phase 63.2 added `source` (Article 9 -- LOCKed since Phase 61.3,
optional-field-with-safe-default extension only): a free-text
provenance string for where an entry's content is traced from, e.g.
"context/bos.py" or "docs/WYCKOFF.md". Optional and unset (`None`) on
every pre-existing entry -- this phase does not backfill the 26
existing entries, only adds the capability for new/future ones to
record it.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence


class KnowledgeCategory(Enum):
    SMC = "SMC"
    WYCKOFF = "WYCKOFF"
    RISK = "RISK"
    PSYCHOLOGY = "PSYCHOLOGY"
    EXAMPLES = "EXAMPLES"
    FAQ = "FAQ"


@dataclass(frozen=True)
class KnowledgeEntry:
    key: str
    category: KnowledgeCategory
    title: str
    summary: str
    tags: Sequence[str] = field(default_factory=tuple)
    source: Optional[str] = None
