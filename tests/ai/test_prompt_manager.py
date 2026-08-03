"""
Phase 55 — PromptManager foundation tests.

Static template rendering only -- no LLM call anywhere in
ai/prompts/prompt_manager.py, matching this phase's explicit scope.
"""

from ai.interfaces import MarketContext, UserContext
from ai.prompts.prompt_manager import PromptManager
from context_layer.fundamental.fundamental_context import compute_fundamental_context, merge_fundamental_score
from context_layer.fundamental.fundamental_scoring import compute_fundamental_score


def test_market_analysis_prompt_includes_context_fields():
    manager = PromptManager()
    context = MarketContext(symbol="XAUUSD", timeframe="M15", summary="range-bound")

    prompt = manager.get_market_analysis_prompt(context)

    assert isinstance(prompt, str)
    assert "XAUUSD" in prompt
    assert "M15" in prompt
    assert "range-bound" in prompt


def test_market_analysis_prompt_forbids_signal_generation_in_its_own_text():
    """The template itself must state the AI-advisory-only boundary."""
    manager = PromptManager()
    context = MarketContext(symbol="XAUUSD", timeframe="M15", summary="x")

    prompt = manager.get_market_analysis_prompt(context)

    assert "Do NOT generate" in prompt or "do not approve" in prompt.lower() or "MISSION" in prompt


def test_user_assistant_prompt_without_user_context_returns_base_template():
    manager = PromptManager()
    prompt = manager.get_user_assistant_prompt()

    assert isinstance(prompt, str)
    assert "GoldBot Personal Assistant" in prompt


def test_user_assistant_prompt_with_user_context_includes_personalization():
    manager = PromptManager()
    user_context = UserContext(experience_level="advanced", preferred_strategy="AMD", language="UZ")

    prompt = manager.get_user_assistant_prompt(user_context)

    assert "advanced" in prompt
    assert "AMD" in prompt
    assert "UZ" in prompt


def test_prompt_manager_never_calls_a_network_or_llm_client():
    """No aiogram/requests/google-genai import anywhere in prompt_manager.py."""
    import inspect
    from ai.prompts import prompt_manager

    source = inspect.getsource(prompt_manager)
    for forbidden in ("import requests", "import aiogram", "genai", "openai"):
        assert forbidden not in source


# --- Phase 60.5 TASK 7: get_fundamental_analysis_prompt() ---

def test_fundamental_analysis_prompt_includes_technical_and_fundamental_fields():
    manager = PromptManager()
    context = MarketContext(symbol="XAUUSD", timeframe="H4", summary="bearish structure")
    snapshot = compute_fundamental_context()
    score = compute_fundamental_score(dxy_bias="BULLISH", fed_expectation="HAWKISH")
    fundamental = merge_fundamental_score(snapshot, score)

    prompt = manager.get_fundamental_analysis_prompt(context, fundamental)

    assert "XAUUSD" in prompt
    assert "H4" in prompt
    assert "bearish structure" in prompt
    assert "BULLISH" in prompt
    assert "HAWKISH" in prompt
    assert fundamental.gold_bias in prompt


def test_fundamental_analysis_prompt_states_the_no_trade_signal_boundary():
    """The template itself must state the advisory-only boundary, matching every other prompt in this module."""
    manager = PromptManager()
    context = MarketContext(symbol="XAUUSD", timeframe="H4", summary="x")
    fundamental = compute_fundamental_context()

    prompt = manager.get_fundamental_analysis_prompt(context, fundamental)

    assert "do not say" in prompt.lower() or "do not generate" in prompt.lower() or "MISSION" in prompt


def test_fundamental_analysis_prompt_handles_all_none_fundamental_gracefully():
    manager = PromptManager()
    context = MarketContext(symbol="XAUUSD", timeframe="H4", summary="x")
    fundamental = compute_fundamental_context()  # every scoring field None

    prompt = manager.get_fundamental_analysis_prompt(context, fundamental)  # must not raise

    assert "unknown" in prompt
