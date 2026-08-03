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

get_fundamental_analysis_prompt() (Phase 60.5: Fundamental
Intelligence Foundation, TASK 7) is an extension of this same class,
not a new ai/fundamental_prompt.py file -- TASK 1's reuse audit found
this class is already the general-purpose, MarketContext-shaped
template registry a fundamental-analysis prompt belongs in, and the
Module Reuse Principle (CLAUDE.md) makes extending an existing module
the default over creating a new one. Same static-template-only
posture as every other method here: no LLM call, no network access.
"""

from typing import Optional, TYPE_CHECKING

from ai.interfaces import MarketContext, UserContext

if TYPE_CHECKING:
    from context_layer.fundamental.fundamental_context import FundamentalContextSnapshot

FUNDAMENTAL_ANALYSIS_SYSTEM_PROMPT = """
ROLE: Macro/Fundamental Analyst.
MISSION: Explain what the supplied technical and fundamental context
together suggest about gold. Do NOT generate a trade signal, do NOT
say "BUY" or "SELL", do NOT approve or reject anything, do NOT invent
data not present in the supplied context. Output a macro bias
(BULLISH GOLD / BEARISH GOLD / NEUTRAL) with a confidence and reasons
only -- the Decision Engine, not this prompt, turns any of this into a
trade.
""".strip()

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

    def get_fundamental_analysis_prompt(
        self, market_context: MarketContext, fundamental: 'FundamentalContextSnapshot'
    ) -> str:
        """
        Builds a combined technical + fundamental analysis prompt from
        an already-built MarketContext and an already-built
        context.fundamental_context.FundamentalContextSnapshot (Phase
        60.5). Template only -- matches the Director's own worked
        example shape ("Technical: H4 bearish / Fundamental: Fed
        hawkish, DXY strong"). Never calls FundamentalContextSnapshot's
        producer itself; this method only formats an already-computed
        snapshot.
        """
        return (
            f"{FUNDAMENTAL_ANALYSIS_SYSTEM_PROMPT}\n\n"
            f"Symbol: {market_context.symbol}\n"
            f"Timeframe: {market_context.timeframe}\n"
            f"Technical: {market_context.summary}\n\n"
            f"Fundamental:\n"
            f"Gold Bias: {fundamental.gold_bias or 'unknown'}\n"
            f"Confidence: {fundamental.confidence if fundamental.confidence is not None else 'unknown'}\n"
            f"DXY Bias: {fundamental.dxy_bias or 'unknown'}\n"
            f"Rates Bias: {fundamental.rates_bias or 'unknown'}\n"
            f"Inflation Bias: {fundamental.inflation_bias or 'unknown'}\n"
            f"Fed Expectation: {fundamental.fed_expectation or 'unknown'}\n"
            f"Risk Sentiment: {fundamental.risk_sentiment or 'unknown'}"
        )
