"""
Phase 60.8 (Safe Integration Layer, TASK 2/3/5) -- end-to-end
PipelineGuard wiring tests through the real TradingPipeline.run().
Builds a real TradingPipeline (same stubbing posture as
tests/conftest.py's mock_pipeline fixture: only the data-fetch layer
is stubbed) with an injected PipelineGuard backed by a stub
EmergencyManager, so every Emergency combination is deterministic and
never touches the real database's emergency_states table.

Phase 60.9 (Runtime Registry Separation, TASK 4): PipelineGuard no
longer reads RuntimeFeatureManager at all -- the former "ENABLE_SIGNALS
OFF"/"ENABLE_AI OFF" runtime-feature scenarios no longer apply (those
names were removed from the registry entirely, see
docs/FEATURE_REGISTRY_SEPARATION.md). The AI-stage neutral-substitution
mechanism (core/pipeline.py's _neutral_ai_result()) is still real,
tested code -- exercised below via a duck-typed stub guard, since no
real EmergencyState combination triggers before_ai() skipping alone
(see core_layer/pipeline/pipeline_guard.py's own "Design notes" for why).
"""

from dataclasses import dataclass

from core_layer.pipeline import TradingPipeline
from core_layer.emergency.emergency_state import EmergencyState, create_emergency_state_record
from core_layer.pipeline.pipeline_guard import GuardDecision, PipelineGuard
from data.market_data import MarketSnapshot
from decision.models import DecisionAction


class _StubEmergencyManager:
    def __init__(self, state=EmergencyState.NORMAL):
        self._record = create_emergency_state_record(state)

    def get_status(self):
        return self._record


@dataclass
class _AiOnlySkipGuard:
    """Duck-typed stub: before_ai() skips, the other three hooks always proceed -- a combination no real EmergencyState produces (see module docstring), used to directly test core/pipeline.py's neutral-substitution handling."""

    def before_signal(self):
        return GuardDecision(proceed=True)

    def before_ai(self):
        return GuardDecision(proceed=False, reason="test: ai stage forced off")

    def before_execution(self):
        return GuardDecision(proceed=True)

    def before_database(self):
        return GuardDecision(proceed=True)


def _pipeline(candidates, ai_results, emergency_state=EmergencyState.NORMAL, pipeline_guard=None):
    guard = pipeline_guard or PipelineGuard(emergency_manager=_StubEmergencyManager(emergency_state))
    pipeline = TradingPipeline(
        symbol="XAUUSD", interval="M15", outputsize=200,
        send_notifications=True, persist_signals=True, pipeline_guard=guard,
    )
    pipeline.signal_engine.generate_signals = lambda context: candidates
    pipeline.data_normalizer.get_candles = lambda *a, **k: []
    pipeline.data_normalizer.get_snapshot = lambda *a, **k: MarketSnapshot(symbol="XAUUSD")
    results_iter = iter(ai_results)
    pipeline.ai_analyzer.analyze = lambda candidate, context: next(results_iter)
    return pipeline


def test_ai_stage_skip_substitutes_a_neutral_result_and_decision_still_runs(mock_signal_candidate):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.95)
    pipeline = _pipeline([candidate], [], pipeline_guard=_AiOnlySkipGuard())
    calls = []
    pipeline.ai_analyzer.analyze = lambda c, ctx: (calls.append(1), None)[1]

    result = pipeline.run()

    assert calls == []  # AIAnalyzer.analyze() was never actually invoked
    assert len(result["ai_results"]) == 1
    assert result["ai_results"][0].approved is True
    assert result["ai_results"][0].confidence == 0.5
    assert len(result["decisions"]) == 1  # Decision Engine still evaluated the candidate


def test_emergency_warning_does_not_block_the_pipeline(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.9)
    pipeline = _pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)], EmergencyState.WARNING)

    result = pipeline.run()

    assert result["decisions"][0].action == DecisionAction.APPROVE
    assert len(result["telegram_messages"]) == 1
    assert len(result["notification_results"]) == 1  # delivery still happened


def test_emergency_paused_skips_execution_but_decision_and_risk_continue(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.9)
    pipeline = _pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)], EmergencyState.PAUSED)

    result = pipeline.run()

    assert result["decisions"][0].action == DecisionAction.APPROVE
    assert result["risk_results"][0].approved is True
    assert len(result["telegram_messages"]) == 1  # formatting still happens
    assert result["notification_results"] == []  # delivery itself was skipped
    assert len(result["signal_records"]) == 1  # database write is unaffected by PAUSED


def test_emergency_maintenance_skips_signal_through_database(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.9)
    pipeline = _pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)], EmergencyState.MAINTENANCE)

    result = pipeline.run()

    assert result["signals"] == []
    assert result["decisions"] == []
    assert result["telegram_messages"] == []
    assert result["notification_results"] == []
    assert result["signal_records"] == []


def test_emergency_killed_aborts_the_pipeline(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = _pipeline([candidate], [mock_ai_result()], EmergencyState.KILLED)

    result = pipeline.run()

    assert result["signals"] == []
    assert result["context_snapshot"] is None
    assert result["decisions"] == []
    assert result["telegram_messages"] == []
    assert result["signal_records"] == []
    # Still populated: everything computed before the first guard hook.
    assert result["context"] is not None
    assert result["market_phase"] is not None
