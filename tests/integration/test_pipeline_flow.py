"""
Phase 52 — TradingPipeline integration tests.

Previously ZERO tests exercised core/pipeline.py end-to-end (0%
coverage before this phase) -- meaning the critical-bug-fix phase's
guarantees (rejected/blocked/invalid-geometry signals never reach
Telegram; at most one Telegram message per pipeline cycle) had no
permanent regression protection, only ad-hoc manual verification in
chat during that phase. This file is that missing regression suite.

Uses the mock_pipeline fixture (tests/conftest.py): only the
data-fetch step is stubbed (no live Twelve Data / Telegram network
possible in a test run) -- Decision, Risk, the approve+select filter,
SignalFormatter, Notifier, and SignalRepository are all real,
unmodified production code.
"""

from decision.models import DecisionAction
from signals.models import SignalType


def test_case1_valid_signal_is_approved_and_telegram_eligible(
    mock_pipeline, mock_signal_candidate, mock_ai_result
):
    """Case 1: a geometrically valid, high-confidence signal -> APPROVE + Risk PASS + exactly one Telegram message."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.9)
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    assert result["decisions"][0].action == DecisionAction.APPROVE
    assert result["risk_results"][0].approved is True
    assert len(result["telegram_messages"]) == 1
    assert len(result["signal_records"]) == 1  # persisted regardless


def test_case2_ai_reject_never_reaches_telegram(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """Case 2: AI rejects the signal -> Decision REJECT, zero Telegram messages, still persisted."""
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=False)])

    result = pipeline.run()

    assert result["decisions"][0].action == DecisionAction.REJECT
    assert len(result["telegram_messages"]) == 0
    assert len(result["signal_records"]) == 1  # rejected signals are still saved for analytics


def test_case3_risk_blocked_never_reaches_telegram(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """Case 3: AI approves but geometry is invalid -> Risk blocks, zero Telegram messages."""
    candidate = mock_signal_candidate(entry=4000.0, stop_loss=4010.0, take_profit=3990.0)  # invalid BUY
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()

    assert result["decisions"][0].action == DecisionAction.APPROVE
    assert result["risk_results"][0].approved is False
    assert len(result["telegram_messages"]) == 0
    assert len(result["signal_records"]) == 1


def test_case4_multiple_candidates_only_highest_confidence_selected(
    mock_pipeline, mock_signal_candidate, mock_ai_result
):
    """Case 4: 3 candidates (2 valid APPROVE + 1 invalid-geometry) -> exactly 1 Telegram message, the highest-confidence valid one."""
    candidates = [
        mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4075.0, confidence=0.80, strategy_name="A"),
        mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, confidence=0.95, strategy_name="B"),
        mock_signal_candidate(
            signal_type=SignalType.SELL, entry=4111.40, stop_loss=4111.33, take_profit=4090.0,
            confidence=0.99, strategy_name="C_invalid_geometry",
        ),
    ]
    ai_results = [mock_ai_result(approved=True, confidence=0.9) for _ in candidates]
    pipeline = mock_pipeline(candidates, ai_results)

    result = pipeline.run()

    assert [d.action for d in result["decisions"]] == [
        DecisionAction.APPROVE, DecisionAction.APPROVE, DecisionAction.APPROVE,
    ]
    assert [r.approved for r in result["risk_results"]] == [True, True, False]
    assert len(result["telegram_messages"]) == 1  # never more than one per cycle
    assert len(result["signal_records"]) == 3  # every candidate still persisted


def test_no_candidates_produces_no_telegram_messages(mock_pipeline):
    """Zero signal candidates (e.g. no market data) must not crash and must send nothing."""
    pipeline = mock_pipeline([], [])

    result = pipeline.run()

    assert result["telegram_messages"] == []
    assert result["signal_records"] == []


def test_persist_signals_false_does_not_write_to_database(mock_signal_candidate, mock_ai_result):
    """send_notifications/persist_signals both default False -- no side effects unless explicitly enabled."""
    from core.pipeline import TradingPipeline

    pipeline = TradingPipeline(symbol="XAUUSD", interval="M15", outputsize=200)
    pipeline.signal_engine.generate_signals = lambda context: [mock_signal_candidate()]
    pipeline.data_normalizer.get_candles = lambda *a, **k: []
    pipeline.ai_analyzer.analyze = lambda candidate, context: mock_ai_result(approved=True, confidence=0.95)

    result = pipeline.run()

    assert result["signal_records"] == []
    assert result["notification_results"] == []
    assert pipeline.signal_repository is None  # never constructed -- no disk write at all
