"""
AI Layer — AI Content Types (Phase 61.5: AI Production Integration
Foundation, TASK 5; extended Phase 63.0: Senior Trading AI Foundation,
TASK 2; extended Phase 63.6: AI Content Intelligence Foundation,
TASK 6).

`ai/capabilities/capability.py`'s four new `AI_*` members (Phase 61.5
TASK 5) are already the vocabulary for "what content can AI be asked
to generate" -- this module does not duplicate them as a second enum.
It is the one place that knows *which* `Capability` values are
content-generation-shaped (`CONTENT_CAPABILITIES`) and their
human-readable display title, so `ai/content/content_adapter.py`
doesn't hardcode either.

Phase 63.0 TASK 2: per the Director's own brief this phase, GoldBot
needs a `ContentType` vocabulary of the *kinds* of content the future
Senior Trading AI platform produces (`WEEKLY_OUTLOOK`, `DAILY_BRIEF`,
`NEWS_ANALYSIS`, `MARKET_UPDATE`, `PERFORMANCE_REVIEW`, `EDUCATION`,
`EXPLANATION`) -- a foundation-only content package, per Module Reuse
Principle (`docs/PHASE63_0_FOUNDATION_AUDIT.md`), extends this
existing file in place rather than a new top-level `content/` package
duplicating `ContentRequest`/`ContentResult`. This is deliberately a
*type* taxonomy, narrower than `Capability`: some values already
overlap conceptually with an existing `Capability`
(`WEEKLY_OUTLOOK`≈`AI_WEEKLY_OUTLOOK`, `NEWS_ANALYSIS`≈`AI_NEWS_ANALYSIS`)
while others (`DAILY_BRIEF`, `MARKET_UPDATE`, `PERFORMANCE_REVIEW`) have
no `Capability` of their own yet -- a future phase may generate any of
them through the single new `Capability.AI_CONTENT` (TASK 8) plus this
`ContentType` as a parameter, rather than growing the `Capability` enum
one-for-one with every content type. No generation logic here (Rule 6
-- "Content Generate qilmaydi. Faqat contract.").
"""

from enum import Enum
from typing import Dict, FrozenSet

from ai.capabilities.capability import Capability

CONTENT_CAPABILITIES: FrozenSet[Capability] = frozenset({
    Capability.AI_MARKET_REPORT,
    Capability.AI_WEEKLY_OUTLOOK,
    Capability.AI_NEWS_ANALYSIS,
    Capability.AI_SCRIPT_GENERATION,
})


class ContentType(Enum):
    """
    The kinds of content the future Senior Trading AI platform can
    produce -- pure vocabulary, no generation logic (Phase 63.0 TASK 2).
    `TRADE_REPLAY` added Phase 63.6 TASK 6 -- traced to
    `docs/roadmap/AI_EVOLUTION.md`'s own "AI Media Intelligence
    Platform" vision section, which already named "Trade Replay" as a
    future content flow with no `ContentType` value of its own until
    now. The brief's other five named types (`TRADE_EXPLANATION`,
    `MARKET_REPORT`, `EDUCATION`, `WEEKLY_OUTLOOK`, `NEWS_SUMMARY`) all
    map onto an existing member (`EXPLANATION`, `MARKET_UPDATE`,
    `EDUCATION`, `WEEKLY_OUTLOOK`, `NEWS_ANALYSIS` respectively) -- see
    `docs/PHASE63_6_AUDIT.md` for the full mapping.
    """
    WEEKLY_OUTLOOK = "WEEKLY_OUTLOOK"
    DAILY_BRIEF = "DAILY_BRIEF"
    NEWS_ANALYSIS = "NEWS_ANALYSIS"
    MARKET_UPDATE = "MARKET_UPDATE"
    PERFORMANCE_REVIEW = "PERFORMANCE_REVIEW"
    EDUCATION = "EDUCATION"
    EXPLANATION = "EXPLANATION"
    TRADE_REPLAY = "TRADE_REPLAY"

_CONTENT_TITLES: Dict[Capability, str] = {
    Capability.AI_MARKET_REPORT: "Market Report",
    Capability.AI_WEEKLY_OUTLOOK: "Weekly Outlook",
    Capability.AI_NEWS_ANALYSIS: "News Analysis",
    Capability.AI_SCRIPT_GENERATION: "Script",
}


def is_content_capability(capability: Capability) -> bool:
    """Never raises: any `Capability` not in `CONTENT_CAPABILITIES` (e.g. CHAT, ANALYSIS) reports False, not an error."""
    return capability in CONTENT_CAPABILITIES


def content_title(capability: Capability) -> str:
    """Never raises: a non-content capability falls back to its own `.value` rather than raising KeyError."""
    return _CONTENT_TITLES.get(capability, capability.value)
