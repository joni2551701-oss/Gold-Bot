from dataclasses import dataclass
from context.context_orchestrator import ContextSnapshot
from signals.models import SignalCandidate
from ai.confidence_model import ConfidenceResult

SYSTEM_PROMPT = """
ROLE: Trading Validator.
MISSION: Validate the provided signal using only the supplied context.
FORBIDDEN:
- Do NOT generate signals.
- Do NOT modify Entry, StopLoss, TakeProfit, or Direction.
- Do NOT invent Market Structure, Liquidity, FVG, or OrderBlocks.
- Evaluate ONLY supplied data.
- If data is missing or ambiguous, output a risk score of 1.0 and do not approve.
OUTPUT: Strict JSON matching the provided schema.
"""

@dataclass(frozen=True)
class PromptPayload:
    system_prompt: str
    user_prompt: str
    json_schema: dict

def _summarize_context(context: ContextSnapshot) -> str:
    """Deterministic, comprehensive context summary."""
    latest_structure = context.structure[-1] if context.structure else None
    return (
        f"Trend/Bias: {latest_structure.structure.value if latest_structure else 'Neutral'}, "
        f"BOS: {context.bos_events[-1].broken_structure.swing.price if context.bos_events else 'N/A'}, "
        f"CHoCH: {context.choch_events[-1].broken_structure.swing.price if context.choch_events else 'N/A'}, "
        f"Liquidity Sweep: {context.liquidity_sweeps[-1].sweep_price if context.liquidity_sweeps else 'N/A'}, "
        f"Liquidity Zone: {context.liquidity_zones[-1].price if context.liquidity_zones else 'N/A'}, "
        f"OB: {context.order_blocks[-1].high if context.order_blocks else 'N/A'}, "
        f"FVG: {context.fair_value_gaps[-1].top if context.fair_value_gaps else 'N/A'}, "
        f"AMD: {context.amd_events[-1].type if context.amd_events else 'N/A'}, "
        f"Session: unknown, "
        f"Premium/Discount: unknown"
    )

def build_prompt(signal: SignalCandidate, context: ContextSnapshot, conf: ConfidenceResult) -> PromptPayload:
    schema = {
        "type": "object",
        "properties": {
            "approved": {"type": "boolean"},
            "confidence": {"type": "number", "description": "Value between 0.0 and 1.0"},
            "risk_score": {"type": "number", "description": "Value between 0.0 and 1.0"},
            "summary": {"type": "string"},
            "risks": {"type": "array", "items": {"type": "string"}},
            "recommendation": {"type": "string"}
        },
        "required": ["approved", "confidence", "risk_score", "summary", "risks", "recommendation"],
        "additionalProperties": False
    }
    
    user = f"""
    SIGNAL METADATA:
    Strategy: {signal.strategy_name}, Type: {signal.signal_type.value}
    Entry: {signal.entry}, SL: {signal.stop_loss}, TP: {signal.take_profit}
    
    CONFIDENCE METRICS:
    Score: {conf.technical_score}/100
    Reasons: {', '.join(conf.reasons)}
    Warnings: {', '.join(conf.warnings)}
    
    MARKET CONTEXT:
    {_summarize_context(context)}
    """
    
    return PromptPayload(SYSTEM_PROMPT, user, schema)
