"""
Pre-Phase 59 Architecture Readiness Review, AC-03 -- Signal <-> Context
Historical Link integration tests.

Uses the same mock_pipeline fixture as tests/integration/test_pipeline_flow.py
(only the data-fetch layer stubbed; Decision, Risk, and the new
market_phase/signal_history stages are real, unmodified production
code) to verify core/pipeline.py's wiring end to end, not just the
underlying signals.adapter/context.snapshot units in isolation.
"""

from signals.schema import SignalSchema
from context.snapshot import ContextSnapshotSchema
from context.market_phase import MarketPhaseResult


def test_pipeline_returns_a_context_snapshot_and_signal_history(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    assert isinstance(result["context_snapshot"], ContextSnapshotSchema)
    assert isinstance(result["market_phase"], MarketPhaseResult)
    assert len(result["signal_history"]) == 1
    assert isinstance(result["signal_history"][0], SignalSchema)


def test_signal_history_market_phase_matches_the_cycle_market_phase(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """Phase 59 Real Market Validation Foundation, TASK 2 -- market_phase must flow from the cycle's own MarketPhaseResult, never recomputed."""
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    record = result["signal_history"][0]
    assert record.market_phase == result["market_phase"].phase.value


def test_signal_history_context_id_matches_the_cycle_context_snapshot(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    record = result["signal_history"][0]
    snapshot = result["context_snapshot"]
    assert record.context_id == snapshot.snapshot_id
    assert record.context_id is not None


def test_signal_history_decision_id_is_populated_per_decision(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    record = result["signal_history"][0]
    assert record.decision_id is not None
    assert len(record.decision_id) == 36  # a real UUID4 string


def test_signal_history_strategy_name_matches_the_real_candidate(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(strategy_name="LIQUIDITY_SWEEP_STRATEGY")
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    assert result["signal_history"][0].strategy_name == "LIQUIDITY_SWEEP_STRATEGY"


def test_signal_history_reflects_the_real_decision_status(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    record = result["signal_history"][0]
    decision = result["decisions"][0]
    assert record.decision in ("APPROVED", "REJECTED", "PENDING")
    # AI approved + high confidence -> Decision Engine should APPROVE -> "APPROVED"
    if decision.action.value == "APPROVE":
        assert record.decision == "APPROVED"


def test_multiple_candidates_each_get_their_own_distinct_decision_id(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidates = [
        mock_signal_candidate(strategy_name="LIQUIDITY_SWEEP_STRATEGY"),
        mock_signal_candidate(strategy_name="FVG_STRATEGY"),
    ]
    ai_results = [mock_ai_result(approved=True, confidence=0.9) for _ in candidates]
    pipeline = mock_pipeline(candidates, ai_results)

    result = pipeline.run()

    assert len(result["signal_history"]) == 2
    decision_ids = {record.decision_id for record in result["signal_history"]}
    assert len(decision_ids) == 2  # each candidate's decision gets its own id
    # both share the same cycle's context_id -- one context per cycle, not per candidate
    context_ids = {record.context_id for record in result["signal_history"]}
    assert len(context_ids) == 1


def test_no_candidates_produces_empty_signal_history_but_still_a_context_snapshot(mock_pipeline):
    pipeline = mock_pipeline([], [])

    result = pipeline.run()

    assert result["signal_history"] == []
    assert isinstance(result["context_snapshot"], ContextSnapshotSchema)  # still built once per cycle


def test_signal_history_is_json_serializable(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    for record in result["signal_history"]:
        record.to_json()  # must not raise
    result["context_snapshot"].to_json()  # must not raise
