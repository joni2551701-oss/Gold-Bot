"""
Monitoring Layer — Decision Pipeline Logger (GoldBot Core Owner
Monitoring Alpha, TASK 5).

Records a primitive, per-criterion trace of an already-made signal
evaluation ("Market Structure: PASS, Liquidity: PASS, FVG: FAIL,
Decision: NO TRADE") -- this brief's own named future `66.5`/`66.6`
Performance/Strategy Intelligence datasource. Never generates a
signal, never decides a trade -- every field here is relayed from a
caller who already computed it (e.g. via
`signals.signal_quality.SignalQualityResult`, read type-only by the
caller, never imported by this module -- see
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s own "signals/ and context/"
section for why).

Persisted via `database.monitoring_repository.MonitoringRepository`
(TASK 9) -- this datasource must survive process restarts to
accumulate a real dataset for a future phase.
"""

from typing import Optional, Sequence, Tuple

from core_layer.logger.logger import setup_logger
from database.monitoring_repository import MonitoringRepository
from monitoring.models import DecisionPipelineEntry

logger = setup_logger("DecisionLogger")


class DecisionLogger:
    def __init__(self, repository: Optional[MonitoringRepository] = None):
        self._repository = repository

    def _get_repository(self) -> MonitoringRepository:
        if self._repository is None:
            self._repository = MonitoringRepository()
        return self._repository

    def log_entry(
        self,
        symbol: str,
        timeframe: str,
        criteria_met: Sequence[str],
        criteria_total: int,
        decision: str,
        reason: str = "",
        stage_durations_ms: Optional[Sequence[Tuple[str, float]]] = None,
    ) -> Optional[DecisionPipelineEntry]:
        """
        Never raises: a database failure logs a warning and returns
        None rather than propagating. `stage_durations_ms` (Phase B.0
        TASK 5) is caller-supplied only -- this method never measures a
        stage's duration itself, only relays what it is given.
        """
        try:
            row = self._get_repository().record_decision_entry(
                symbol=symbol, timeframe=timeframe, criteria_met=criteria_met,
                criteria_total=criteria_total, decision=decision, reason=reason,
                stage_durations_ms=stage_durations_ms or (),
            )
        except Exception as e:
            logger.warning(f"log_entry failed: {e}")
            return None

        return DecisionPipelineEntry(
            timestamp=row.created_at.isoformat() if row.created_at else "",
            symbol=row.symbol,
            timeframe=row.timeframe,
            criteria_met=row.criteria_met,
            criteria_total=row.criteria_total,
            decision=row.decision,
            reason=row.reason,
            stage_durations_ms=row.stage_durations_ms,
        )

    def get_recent_entries(self, limit: int = 20) -> Sequence[DecisionPipelineEntry]:
        """Never raises: a database failure returns an empty tuple."""
        try:
            rows = self._get_repository().get_recent_decision_entries(limit=limit)
        except Exception as e:
            logger.warning(f"get_recent_entries failed: {e}")
            return ()

        return tuple(
            DecisionPipelineEntry(
                timestamp=row.created_at.isoformat() if row.created_at else "",
                symbol=row.symbol,
                timeframe=row.timeframe,
                criteria_met=row.criteria_met,
                criteria_total=row.criteria_total,
                decision=row.decision,
                reason=row.reason,
                stage_durations_ms=row.stage_durations_ms,
            )
            for row in rows
        )
