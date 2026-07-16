"""
AI Layer — Capability model (Phase 61.0: AI Infrastructure Foundation,
TASK 2).

Capability names *what* the AI layer can be asked to do, never *how*
or *which vendor* answers it. Per the Phase 61.0 brief: "Capability
model nomini bilmaydi" -- a caller asks for Capability.EXPLANATION and
never learns from this module whether Gemini, OpenAI, or a local model
served it. That mapping is TASK 4's `ai/router/` job, not this one's.

Foundation only: this enum has no behavior, no provider awareness, and
is not imported by `core/pipeline.py`, `decision/`, `risk/`,
`strategies/`, `signals/`, or `execution/` (Phase 61.0's own
restriction list).
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
