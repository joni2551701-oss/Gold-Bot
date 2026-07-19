"""
Voice Layer — Voice Intent Detector (Phase 65.2, TASK 3).

`detect_intent()` is a pure, deterministic keyword classifier -- no
LLM call, no network call, matching every other Phase 61.x-65.x
"metadata only" convention. This phase uses the detected intent for
logging/metadata only (attached to `voice/conversation_bridge.py`'s
own result) -- no branching logic anywhere reads it yet; a future
phase may route different intents to different prompts/tools without
changing this function's signature.
"""

from voice.intents.models import VoiceIntent

_KEYWORDS = {
    VoiceIntent.TRADE_EXPLANATION: ("why did you", "explain this trade", "why this signal", "why entry", "why stop loss", "why sl", "why tp"),
    VoiceIntent.MARKET_ANALYSIS: ("market", "gold", "xauusd", "price", "trend", "analysis", "chart"),
    VoiceIntent.EDUCATION: ("teach me", "how do i", "what is", "explain", "learn", "beginner"),
    VoiceIntent.ACCOUNT_HELP: ("my account", "subscription", "payment", "billing", "password", "login"),
}


def detect_intent(text: str) -> VoiceIntent:
    """Never raises: empty/unmatched text returns GENERAL_CHAT. Checked in dict-declared order (TRADE_EXPLANATION before MARKET_ANALYSIS) so a phrase like "why this signal" doesn't fall through to the broader MARKET_ANALYSIS keyword set first."""
    if not text:
        return VoiceIntent.GENERAL_CHAT

    lowered = text.lower()
    for intent, keywords in _KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return intent

    return VoiceIntent.GENERAL_CHAT
