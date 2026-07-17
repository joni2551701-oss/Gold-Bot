"""
AI Layer — Capability model (Phase 61.0: AI Infrastructure Foundation,
TASK 2; extended Phase 61.5: AI Production Integration Foundation,
TASK 5).

Capability names *what* the AI layer can be asked to do, never *how*
or *which vendor* answers it. Per the Phase 61.0 brief: "Capability
model nomini bilmaydi" -- a caller asks for Capability.EXPLANATION and
never learns from this module whether Gemini, OpenAI, or a local model
served it. That mapping is TASK 4's `ai/router/` job, not this one's.

Foundation only: this enum has no behavior, no provider awareness, and
is not imported by `core/pipeline.py`, `decision/`, `risk/`,
`strategies/`, `signals/`, or `execution/` (Phase 61.0's own
restriction list).

The four `AI_*` content members (Phase 61.5 TASK 5) follow the Module
Reuse Principle's step 2 (extend, don't duplicate): `ai/content/`
needed a vocabulary for "what content can AI be asked to generate,"
and `Capability` already *is* that vocabulary for every other `ai/`
consumer (`ai/access/access_control.py`'s Role x Capability matrix,
`ai/router/routing_rules.py`, `ai/runtime/ai_service.py`'s dispatch
table) -- a second, parallel "ContentType" enum would duplicate it. No
`ai/runtime/ai_service.py` dispatch entry exists for these four yet
(same as `SUMMARY`/`EDUCATION`/`MEMORY`/`TOOL_CALLING`/`VIDEO`/
`DOCUMENT` before them) -- `ai/content/content_adapter.py` asks
honestly and is cleanly rejected until a future phase adds the
provider-side mapping. Adding these is additive and safe:
`AccessControl`'s `OWNER`/`ADMIN` entries are `frozenset(Capability)`
(every current member, evaluated at import time) so console operators
gain access automatically; `VIP`/`PREMIUM`/`FREE` list members
explicitly, so they do not gain these four until a future phase
opts them in.
"""

from enum import Enum


class Capability(Enum):
    """
    The fixed vocabulary of AI capabilities this Worker Brief names.
    Each value is advisory-only, matching every other `ai/` module's
    boundary (`ai/interfaces.py`'s `AIAnalyzerInterface` docstring):
    none of these ever approve/reject a trade, call
    `risk.risk_manager.RiskManager`, or trigger execution/Telegram
    delivery on their own.
    """
    CHAT = "CHAT"
    ANALYSIS = "ANALYSIS"
    EXPLANATION = "EXPLANATION"
    SUMMARY = "SUMMARY"
    MEMORY = "MEMORY"
    EDUCATION = "EDUCATION"
    TOOL_CALLING = "TOOL_CALLING"
    VISION = "VISION"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    VOICE = "VOICE"
    DOCUMENT = "DOCUMENT"
    AI_MARKET_REPORT = "AI_MARKET_REPORT"
    AI_WEEKLY_OUTLOOK = "AI_WEEKLY_OUTLOOK"
    AI_NEWS_ANALYSIS = "AI_NEWS_ANALYSIS"
    AI_SCRIPT_GENERATION = "AI_SCRIPT_GENERATION"
