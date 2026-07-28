"""
AI Layer — Content Type Vocabulary (shared pipeline vocabulary).

TASK-AI-000A (AI Architecture Cleanup, Stage 1): `ContentType` was
extracted here, to a neutral top-level `ai/content_types.py`, from
`ai/content/content_types.py`. It is a cross-cutting *vocabulary* used
across the whole intelligence pipeline -- upstream (`ai/explanation/`,
`ai/trading_analyst/`, `ai/chart_intelligence/`), the content service
itself (`ai/content/`), and downstream (`broadcast/`) -- so it is a
genuinely shared abstraction, not a content-service-internal type.

Having it inside `ai/content/` forced the upstream `ai/explanation/`
package (whose `ExplanationOutput.content_type` field is typed as
`ContentType`) to import *down* into `ai/content/`, while
`ai/content/content_adapters.py` legitimately imports *up* into
`ai/explanation/` -- a real `ai.explanation ↔ ai.content` circular
dependency that also violated the documented Intelligence Dependency
Principle (`docs/policies/DIRECTOR_POLICY.md`: Explanation sits
strictly upstream of Content). Extracting the shared vocabulary to a
neutral module both packages import *downward* removes the cycle and
restores that principle (approved strategy #1: shared-abstraction
extraction).

Only the `ContentType` enum moved. The content-service-specific
helpers that map a `Capability` to content metadata
(`CONTENT_CAPABILITIES`, `is_content_capability()`, `content_title()`)
stay in `ai/content/content_types.py`, since they are genuinely
content-internal and are not part of this shared vocabulary. The enum
members and their string values are unchanged -- only the import path
of `ContentType` moved.
"""

from enum import Enum


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
    `docs/PHASE63_6_AUDIT.md` for the full mapping. `LIVE_ANALYSIS`
    added Phase 63.8 TASK 1 -- the one genuine gap in that same
    phase's `BroadcastType` mapping exercise, see
    `docs/PHASE63_8_AUDIT.md`.
    """
    WEEKLY_OUTLOOK = "WEEKLY_OUTLOOK"
    DAILY_BRIEF = "DAILY_BRIEF"
    NEWS_ANALYSIS = "NEWS_ANALYSIS"
    MARKET_UPDATE = "MARKET_UPDATE"
    PERFORMANCE_REVIEW = "PERFORMANCE_REVIEW"
    EDUCATION = "EDUCATION"
    EXPLANATION = "EXPLANATION"
    TRADE_REPLAY = "TRADE_REPLAY"
    LIVE_ANALYSIS = "LIVE_ANALYSIS"
