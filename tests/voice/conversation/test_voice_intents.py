"""Phase 65.2 TASK 3 — voice/intents/: VoiceIntent + detect_intent()."""

from ai_layer.voice_ai.intents.detector import detect_intent
from ai_layer.voice_ai.intents.models import VoiceIntent


def test_voice_intent_has_five_values():
    assert {i.value for i in VoiceIntent} == {
        "MARKET_ANALYSIS", "TRADE_EXPLANATION", "EDUCATION", "ACCOUNT_HELP", "GENERAL_CHAT",
    }


def test_detect_intent_empty_text_returns_general_chat():
    assert detect_intent("") == VoiceIntent.GENERAL_CHAT


def test_detect_intent_trade_explanation():
    assert detect_intent("why did you take this trade") == VoiceIntent.TRADE_EXPLANATION
    assert detect_intent("Why This Signal Was Taken") == VoiceIntent.TRADE_EXPLANATION


def test_detect_intent_market_analysis():
    assert detect_intent("whats the gold price doing today") == VoiceIntent.MARKET_ANALYSIS
    assert detect_intent("show me the XAUUSD trend") == VoiceIntent.MARKET_ANALYSIS


def test_detect_intent_education():
    assert detect_intent("teach me how to place an order") == VoiceIntent.EDUCATION
    assert detect_intent("what is a stop loss") == VoiceIntent.EDUCATION


def test_detect_intent_account_help():
    assert detect_intent("help with my subscription payment") == VoiceIntent.ACCOUNT_HELP
    assert detect_intent("I forgot my password") == VoiceIntent.ACCOUNT_HELP


def test_detect_intent_general_chat_fallback():
    assert detect_intent("hello how are you") == VoiceIntent.GENERAL_CHAT


def test_detect_intent_is_case_insensitive():
    assert detect_intent("WHY DID YOU TAKE THIS TRADE") == VoiceIntent.TRADE_EXPLANATION


def test_detect_intent_never_raises_on_none_like_falsy_input():
    assert detect_intent(None) == VoiceIntent.GENERAL_CHAT
