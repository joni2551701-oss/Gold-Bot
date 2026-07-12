from typing import List
from context.context_orchestrator import ContextSnapshot
from context.bos import BosDirection
from signals.models import SignalCandidate, SignalType


class LiquidityStrategy:
    """
    Analyzes Liquidity Sweeps in relation to structural BOS and Order Blocks.
    Stateless and read-only.
    """

    def analyze(self, context: ContextSnapshot) -> List[SignalCandidate]:
        candidates: List[SignalCandidate] = []

        if not context.liquidity_sweeps or not context.bos_events:
            return candidates

        latest_sweep = context.liquidity_sweeps[-1]

        for bos in context.bos_events:
            if bos.index > latest_sweep.index:
                relevant_ob = None
                for ob in context.order_blocks:
                    if abs(ob.index - latest_sweep.index) <= 5:
                        relevant_ob = ob
                        break

                if relevant_ob:
                    s_type = (
                        SignalType.BUY
                        if bos.direction == BosDirection.BULLISH
                        else SignalType.SELL
                    )

                    entry = (relevant_ob.high + relevant_ob.low) / 2
                    stop_loss = latest_sweep.sweep_price
                    take_profit = bos.broken_structure.swing.price

                    candidates.append(SignalCandidate(
                        signal_type=s_type,
                        entry=entry,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        strategy_name="LIQUIDITY_SWEEP_STRATEGY",
                        confidence=0.75,
                        reasons=[f"Sweep at {latest_sweep.index} confirmed by BOS at {bos.index}"]
                    ))
                    break

        return candidates
