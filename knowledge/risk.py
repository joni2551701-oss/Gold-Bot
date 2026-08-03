"""
Knowledge Foundation — Risk entries (Phase 61.3, TASK 3).

Restates `risk/README.md` and `CLAUDE.md`'s own Trading Safety rules --
what `risk_layer.risk_engine.risk_manager.RiskManager.evaluate()` actually validates, not
generic risk-management theory. No entry here describes a number this
codebase does not already enforce.
"""

from knowledge.models import KnowledgeCategory, KnowledgeEntry

RISK_ENTRIES = (
    KnowledgeEntry(
        key="risk.geometry_validation",
        category=KnowledgeCategory.RISK,
        title="Stop-loss / take-profit geometry validation",
        summary=(
            "Every trade decision's geometry must be internally consistent "
            "before Risk Manager will approve it: for a BUY, "
            "stop_loss < entry < take_profit; for a SELL, the mirror image. "
            "A decision that fails this check is rejected regardless of "
            "confidence."
        ),
        tags=("risk manager", "geometry", "stop loss", "take profit"),
    ),
    KnowledgeEntry(
        key="risk.stop_loss_distance",
        category=KnowledgeCategory.RISK,
        title="Stop-loss distance validation",
        summary=(
            "Risk Manager checks that the stop-loss distance from entry is "
            "within an acceptable range -- a stop placed unrealistically "
            "close or unrealistically far is rejected, independent of the "
            "trade's directional geometry being otherwise valid."
        ),
        tags=("risk manager", "stop loss", "distance"),
    ),
    KnowledgeEntry(
        key="risk.reward_and_sizing",
        category=KnowledgeCategory.RISK,
        title="Risk/reward and position sizing",
        summary=(
            "Risk Manager computes a risk/reward ratio and a lot-size "
            "sizing suggestion from the trade decision and an optional "
            "account balance. This is a sizing suggestion only -- GoldBot "
            "has no broker/MT5 connection and never issues an order "
            "instruction."
        ),
        tags=("risk manager", "position size", "risk reward", "lot size"),
    ),
    KnowledgeEntry(
        key="risk.final_gate",
        category=KnowledgeCategory.RISK,
        title="Risk Manager is the final gate before Telegram",
        summary=(
            "Every signal that could reach a user must pass through "
            "RiskManager.evaluate() -- there is no shortcut path from a "
            "Decision Engine approval straight to a Telegram notification. "
            "This is a hard rule (`CLAUDE.md` Trading Safety), never a "
            "convention that can be routed around."
        ),
        tags=("risk manager", "pipeline", "telegram", "safety"),
    ),
)
