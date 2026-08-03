from typing import Optional
from dataclasses import dataclass

from signal_layer.signal_builder.models import SignalCandidate
from ai.ai_analyzer import AIAnalysisResult
from decision_layer.decision_engine.models import TradeDecision
from risk_layer.risk_engine.risk_manager import RiskResult


@dataclass(frozen=True)
class FormatterConfig:
    enabled: bool = True


@dataclass(frozen=True)
class FormattedSignal:
    formatted: bool
    text: str


def _safe(obj, attr: str, default: str = "N/A"):
    """Reads an attribute defensively -- never raises AttributeError."""
    value = getattr(obj, attr, None)
    if value is None:
        return default
    return value


class SignalFormatter:
    """
    Telegram Layer — signal text formatting only.

    Converts a SignalCandidate + AIAnalysisResult + TradeDecision +
    RiskResult into a human-readable message for manual review and
    execution. Never calculates confidence, never makes a decision,
    never calculates risk, never modifies the signal -- it only reads
    values already produced by the Decision Engine and Risk Manager
    and renders them as text.
    """

    def __init__(
        self,
        config: Optional[FormatterConfig] = None,
    ):
        self.config = config or FormatterConfig()

    def format(self) -> FormattedSignal:
        """
        Legacy placeholder entry point, retained for backward
        compatibility with existing callers (main.py, platform_layer/telegram/notifier.py).
        Use format_signal() for the real signal -> text conversion.
        """
        return FormattedSignal(
            formatted=False,
            text=""
        )

    def format_signal(
        self,
        signal: SignalCandidate,
        ai_analysis: AIAnalysisResult,
        decision: TradeDecision,
        risk_result: RiskResult,
    ) -> str:
        """
        Renders a complete, human-readable trading signal message from
        the four pipeline output objects. Every field is read
        defensively (getattr with a safe default) so a missing or
        malformed attribute never raises -- it renders as "N/A" instead.
        """
        signal_type = _safe(signal, "signal_type")
        direction = getattr(signal_type, "value", "N/A") if signal_type != "N/A" else "N/A"

        symbol = _safe(signal, "symbol", "XAUUSD")

        entry = _safe(signal, "entry")
        stop_loss = _safe(signal, "stop_loss")
        take_profit = _safe(signal, "take_profit")

        entry_text = f"{entry:.2f}" if isinstance(entry, (int, float)) else "N/A"
        sl_text = f"{stop_loss:.2f}" if isinstance(stop_loss, (int, float)) else "N/A"
        tp_text = f"{take_profit:.2f}" if isinstance(take_profit, (int, float)) else "N/A"

        action = _safe(decision, "action")
        action_text = getattr(action, "value", "N/A") if action != "N/A" else "N/A"
        decision_reason = _safe(decision, "reason")
        confidence = _safe(decision, "confidence")
        confidence_text = f"{confidence * 100:.0f}%" if isinstance(confidence, (int, float)) else "N/A"

        risk_approved = _safe(risk_result, "approved", None)
        risk_status_text = "Approved" if risk_approved is True else "Blocked"

        risk_reward = _safe(risk_result, "risk_reward")
        if risk_approved is True and isinstance(risk_reward, (int, float)) and risk_reward > 0:
            rr_text = f"1:{risk_reward:.1f}"
        else:
            rr_text = "N/A"

        risk_amount = _safe(risk_result, "risk_amount")
        if risk_approved is True and isinstance(risk_amount, (int, float)) and risk_amount > 0:
            risk_amount_text = f"{risk_amount:.2f}$"
        else:
            risk_amount_text = "N/A"

        explanation = _safe(ai_analysis, "explanation")

        return (
            "====================\n"
            "🟡 GOLD SIGNAL\n\n"
            f"Symbol:\n{symbol}\n\n"
            f"Direction:\n{direction}\n\n"
            f"Entry:\n{entry_text}\n\n"
            f"Stop Loss:\n{sl_text}\n\n"
            f"Take Profit:\n{tp_text}\n\n"
            f"Risk Reward:\n{rr_text}\n\n"
            f"Confidence:\n{confidence_text}\n\n"
            f"AI Decision:\n{action_text}\n\n"
            f"Risk Status:\n{risk_status_text}\n\n"
            f"Risk Amount:\n{risk_amount_text}\n\n"
            f"Analysis:\n\n{explanation}\n\n"
            f"Reason:\n\n{decision_reason}\n"
            "===================="
        )

    def format_signal_row(self, row: dict) -> str:
        """
        Renders a single persisted 'signals' table row (as returned by
        SignalRepository.get_latest_signal() / get_signal() /
        get_recent_signals()) for /signal and /history. Unlike
        format_signal(), this reads a flat DB row dict, not live
        pipeline objects.

        strategy/timeframe/rr_ratio/ai_decision/risk_status/
        risk_amount/signal_status (Phase 39) are read straight off the
        row -- SignalRepository.save_signal_record() populates them at
        write time via database.signal_record.create_signal_record().
        A pre-Phase-39 row still renders correctly: the schema
        migration backfills these columns with their SQL defaults
        ('UNKNOWN'/'N/A'/'NEW'/0), and any value still missing or
        non-numeric falls back to "N/A" here, same as every other
        field in this method.
        """
        symbol = row.get("symbol") or "XAUUSD"
        direction = row.get("direction") or "N/A"
        strategy = row.get("strategy") or "UNKNOWN"
        timeframe = row.get("timeframe") or "M15"

        entry = row.get("entry_zone_min")
        stop_loss = row.get("stop_loss")
        take_profit = row.get("take_profit_1")

        entry_text = f"{entry:.2f}" if isinstance(entry, (int, float)) else "N/A"
        sl_text = f"{stop_loss:.2f}" if isinstance(stop_loss, (int, float)) else "N/A"
        tp_text = f"{take_profit:.2f}" if isinstance(take_profit, (int, float)) else "N/A"

        rr_ratio = row.get("rr_ratio")
        rr_text = f"1:{rr_ratio:.1f}" if isinstance(rr_ratio, (int, float)) and rr_ratio > 0 else "N/A"

        confidence = row.get("confidence_score")
        confidence_text = f"{confidence * 100:.0f}%" if isinstance(confidence, (int, float)) else "N/A"

        ai_decision = row.get("ai_decision") or "N/A"
        risk_status = row.get("risk_status") or "N/A"

        risk_amount = row.get("risk_amount")
        risk_amount_text = (
            f"${risk_amount:.2f}" if isinstance(risk_amount, (int, float)) and risk_amount > 0 else "N/A"
        )

        signal_status = row.get("signal_status") or "N/A"
        date = row.get("created_at") or "N/A"

        return (
            "🟡 GOLD SIGNAL\n\n"
            f"Symbol:\n{symbol}\n\n"
            f"Direction:\n{direction}\n\n"
            f"Strategy:\n{strategy}\n\n"
            f"Timeframe:\n{timeframe}\n\n"
            f"Entry:\n{entry_text}\n\n"
            f"Stop Loss:\n{sl_text}\n\n"
            f"Take Profit:\n{tp_text}\n\n"
            f"RR:\n{rr_text}\n\n"
            f"Confidence:\n{confidence_text}\n\n"
            f"AI Decision:\n{ai_decision}\n\n"
            f"Risk:\n{risk_status}\n\n"
            f"Risk Amount:\n{risk_amount_text}\n\n"
            f"Status:\n{signal_status}\n\n"
            f"Date:\n{date}"
        )

    def format_signal_history(self, rows) -> str:
        """
        Renders a numbered list of persisted signal rows (newest
        first, as returned by SignalRepository.get_recent_signals())
        for /history. Same Phase 39 field/fallback rules as
        format_signal_row().
        """
        lines = ["Signal History"]
        for i, row in enumerate(rows, start=1):
            symbol = row.get("symbol") or "XAUUSD"
            direction = row.get("direction") or "N/A"
            strategy = row.get("strategy") or "UNKNOWN"

            rr_ratio = row.get("rr_ratio")
            rr_text = f"1:{rr_ratio:.1f}" if isinstance(rr_ratio, (int, float)) and rr_ratio > 0 else "N/A"

            confidence = row.get("confidence_score")
            confidence_text = f"{confidence * 100:.0f}%" if isinstance(confidence, (int, float)) else "N/A"
            date = row.get("created_at") or "N/A"
            lines.append(
                f"\n{i}.\n\n{symbol} {direction}\n\n"
                f"Strategy:\n{strategy}\n\n"
                f"RR:\n{rr_text}\n\n"
                f"Confidence:\n{confidence_text}\n\n"
                f"Date:\n{date}"
            )
        return "\n".join(lines)
