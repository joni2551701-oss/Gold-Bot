"""
AI Layer — AI Content Types (Phase 61.5: AI Production Integration
Foundation, TASK 5; extended Phase 63.0: Senior Trading AI Foundation,
TASK 2; extended Phase 63.6: AI Content Intelligence Foundation,
TASK 6; extended Phase 63.8: AI Broadcast Intelligence Foundation,
TASK 1).

`ai/capabilities/capability.py`'s four new `AI_*` members (Phase 61.5
TASK 5) are already the vocabulary for "what content can AI be asked
to generate" -- this module does not duplicate them as a second enum.
It is the one place that knows *which* `Capability` values are
content-generation-shaped (`CONTENT_CAPABILITIES`) and their
human-readable display title, so `ai/content/content_adapter.py`
doesn't hardcode either.

Phase 63.0 TASK 2 originally added a `ContentType` vocabulary here.
TASK-AI-000A (AI Architecture Cleanup, Stage 1) extracted that enum to
the neutral top-level `ai/content_types.py` -- it is a cross-cutting
vocabulary the upstream `ai/explanation/` package also needs, and
keeping it here forced a real `ai.explanation ↔ ai.content` circular
dependency (see that module's own docstring). What remains here is the
genuinely content-service-internal mapping from a `Capability` to
content metadata (`CONTENT_CAPABILITIES`, `is_content_capability()`,
`content_title()`) -- these stay because they are not shared
vocabulary. No generation logic here (Rule 6 -- "Content Generate
qilmaydi. Faqat contract.").
"""

from typing import Dict, FrozenSet

from ai.capabilities.capability import Capability

CONTENT_CAPABILITIES: FrozenSet[Capability] = frozenset({
    Capability.AI_MARKET_REPORT,
    Capability.AI_WEEKLY_OUTLOOK,
    Capability.AI_NEWS_ANALYSIS,
    Capability.AI_SCRIPT_GENERATION,
})

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
