"""
AI Layer — Explanation Templates (Phase 63.1: AI Explanation
Intelligence Layer, TASK 3).

Three pure, deterministic text-assembly functions -- no AI/LLM call,
no network, no randomness. Each takes an `ExplanationInput` and
returns plain strings `explanation_builder.py` composes into an
`ExplanationOutput`. A missing optional field renders as an honest
placeholder ("not specified"), never a fabricated value.
"""

from ai.explanation.explanation_input import ExplanationInput

_NOT_SPECIFIED = "not specified"


def _or_not_specified(value) -> str:
    return str(value) if value not in (None, "") else _NOT_SPECIFIED


def build_trade_explanation(data: ExplanationInput) -> str:
    """WHY / WHAT / WHERE / RISK / INVALIDATION -- the Trade Explanation template."""
    return (
        f"WHY\n{_or_not_specified(data.technical_reason)}\n\n"
        f"WHAT\n{_or_not_specified(data.market_bias)} bias on {data.symbol}. "
        f"Entry {_or_not_specified(data.entry)}.\n\n"
        f"WHERE\nStop Loss {_or_not_specified(data.stop_loss)}, "
        f"Take Profit {_or_not_specified(data.take_profit)}, "
        f"Risk/Reward {_or_not_specified(data.risk_reward)}.\n\n"
        f"RISK\n{_or_not_specified(data.risk_reason)}\n\n"
        f"INVALIDATION\n{_or_not_specified(data.invalidation)}"
    )


def build_no_trade_explanation(data: ExplanationInput) -> str:
    """Market Condition / Missing Confirmation / Risk Reason / Waiting Condition."""
    return (
        f"MARKET CONDITION\n{_or_not_specified(data.market_condition)}\n\n"
        f"MISSING CONFIRMATION\n{_or_not_specified(data.missing_confirmation)}\n\n"
        f"RISK REASON\n{_or_not_specified(data.risk_reason)}\n\n"
        f"WAITING CONDITION\n{_or_not_specified(data.waiting_condition)}"
    )


def build_education_explanation(data: ExplanationInput) -> str:
    """Concept / Example / Lesson -- Education Mode template."""
    return (
        f"CONCEPT\n{_or_not_specified(data.concept)}\n\n"
        f"EXAMPLE\n{_or_not_specified(data.example)}\n\n"
        f"LESSON\n{_or_not_specified(data.lesson)}"
    )
