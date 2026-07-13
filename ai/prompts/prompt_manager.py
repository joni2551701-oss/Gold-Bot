"""
AI Layer — prompt management foundation (Phase 55).

Goal: keep prompt text in one place instead of scattered through the
codebase as inline strings. PromptManager returns static template
strings only -- no LLM call happens here, and none of these templates
are wired into ai/ai_analyzer.py or any other caller yet.

Distinct from the existing ai/ai_prompt.py: that module is a
production-shaped, Gemini-specific prompt+JSON-schema builder tightly
coupled to internal types (SignalCandidate, ContextSnapshot,
ConfidenceResult) for the one job of validating a trading signal.
PromptManager is the general-purpose successor shape for a future
v0.4+ AI Assistant Core, built against ai.interfaces.MarketContext/
UserContext instead, and covering more than just signal validation
(e.g. get_user_assistant_prompt() for a conversational assistant use
case ai_prompt.py was never meant to cover). ai/ai_prompt.py is left
exactly where it is -- nothing about it changes this phase.
"""

from typing import Optional

from ai.interfaces import MarketContext, UserContext

MARKET_ANALYSIS_SYSTEM_PROMPT = """
ROLE: Trading Market Analyst.
MISSION: Analyze the provided market context and describe what it
shows. Do NOT generate a trade signal, do NOT approve or reject
anything, do NOT invent data not present in the supplied context.
""".strip()

USER_ASSISTANT_SYSTEM_PROMPT = """
ROLE: GoldBot Personal Assistant.
MISSION: Help the user understand their own trading activity, settings,
and history. Never place a trade, never modify a signal, never bypass
Risk Manager or Decision Engine -- you only explain and inform.
""".strip()


class PromptManager:
    """Static template registry. No LLM call, no network access, no state."""

    def get_market_analysis_prompt(self, market_context: MarketContext) -> str:
        """Builds a market-analysis prompt from a MarketContext. Template only."""
        return (
            f"{MARKET_ANALYSIS_SYSTEM_PROMPT}\n\n"
            f"Symbol: {market_context.symbol}\n"
            f"Timeframe: {market_context.timeframe}\n"
            f"Summary: {market_context.summary}"
        )

    def get_user_assistant_prompt(self, user_context: Optional[UserContext] = None) -> str:
        """Builds a personal-assistant prompt from an optional UserContext. Template only."""
        if user_context is None:
            return USER_ASSISTANT_SYSTEM_PROMPT

        return (
            f"{USER_ASSISTANT_SYSTEM_PROMPT}\n\n"
            f"User experience level: {user_context.experience_level or 'unknown'}\n"
            f"Preferred strategy: {user_context.preferred_strategy or 'unknown'}\n"
            f"Risk style: {user_context.risk_style or 'unknown'}\n"
            f"Language: {user_context.language or 'unknown'}"
        )
