"""
Knowledge Foundation — FAQ entries (Phase 61.3, TASK 3).

Restates facts `CLAUDE.md`, `ai/README.md`, and `risk/README.md`
already document about how GoldBot itself behaves -- not trading
theory, but the bot's own documented contract.
"""

from knowledge.models import KnowledgeCategory, KnowledgeEntry

FAQ_ENTRIES = (
    KnowledgeEntry(
        key="faq.does_ai_place_trades",
        category=KnowledgeCategory.FAQ,
        title="Does the AI layer place trades?",
        summary=(
            "No. The AI layer is advisory input to the Decision Engine "
            "only -- it never itself approves or rejects a trade, never "
            "calls the Risk Manager, and never triggers a Telegram send "
            "or an execution action."
        ),
        tags=("ai", "faq", "advisory", "decision engine"),
    ),
    KnowledgeEntry(
        key="faq.can_risk_manager_be_bypassed",
        category=KnowledgeCategory.FAQ,
        title="Can the Risk Manager be bypassed?",
        summary=(
            "No. Every signal that could reach a user must pass through "
            "RiskManager.evaluate() -- there is no shortcut path to "
            "Telegram delivery for any signal, regardless of source or "
            "confidence."
        ),
        tags=("risk manager", "faq", "safety"),
    ),
    KnowledgeEntry(
        key="faq.does_goldbot_execute_orders",
        category=KnowledgeCategory.FAQ,
        title="Does GoldBot place broker orders?",
        summary=(
            "No. GoldBot is a semi-automatic signal bot. The `execution/` "
            "layer is intentionally inert -- no MT5 order calls exist -- "
            "and Risk Manager's position sizing is a suggestion only."
        ),
        tags=("execution", "faq", "semi-automatic"),
    ),
    KnowledgeEntry(
        key="faq.does_goldbot_use_volume",
        category=KnowledgeCategory.FAQ,
        title="Does GoldBot use trading volume data?",
        summary=(
            "No. GoldBot's candle data is OHLC-only -- there is no volume "
            "data source anywhere in the codebase. Any detector that "
            "conventionally uses volume (e.g. Wyckoff Spring/Upthrust "
            "confirmation) reports 'not checked' rather than fabricating "
            "a value."
        ),
        tags=("volume", "faq", "data", "limitation"),
    ),
    KnowledgeEntry(
        key="faq.what_does_goldbot_trade",
        category=KnowledgeCategory.FAQ,
        title="What instrument does GoldBot trade?",
        summary="XAUUSD (Gold vs US Dollar) — a semi-automatic trading-signal bot delivered via Telegram.",
        tags=("xauusd", "gold", "faq"),
    ),
)
