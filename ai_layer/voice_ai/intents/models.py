"""
Voice Layer — Voice Intent Vocabulary (Phase 65.2, TASK 3).

Pure vocabulary, no detection logic (that lives in `detector.py`).
Named exactly as the brief's own five examples, ordered
most-specific-first since `detector.py`'s keyword matching checks in
this same order.
"""

from enum import Enum


class VoiceIntent(Enum):
    MARKET_ANALYSIS = "MARKET_ANALYSIS"
    TRADE_EXPLANATION = "TRADE_EXPLANATION"
    EDUCATION = "EDUCATION"
    ACCOUNT_HELP = "ACCOUNT_HELP"
    GENERAL_CHAT = "GENERAL_CHAT"
