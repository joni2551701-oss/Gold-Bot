"""
Phase 59 Preparation, TASK 6 -- end-to-end foundation tests covering
this phase's own acceptance criteria: PaperTrade creation, Signal
lifecycle transition, Performance schema, Missing data handling,
Context link preservation, Signal -> Result chain.

Uses the same mock_pipeline/mock_signal_candidate/mock_ai_result
fixtures as tests/integration/test_signal_context_link.py (AC-03) --
only the data-fetch layer is stubbed; core/pipeline.py itself,
Decision, and Risk are real, unmodified production code. This file
does not touch core/pipeline.py -- it only feeds the pipeline's own
real SignalSchema/ContextSnapshotSchema output into the new Phase 59
foundation modules (data_layer/live_data/market_data_snapshot.py, lifecycle/,
analytics/), none of which the pipeline calls itself.
"""

from datetime import datetime, timezone

from analytics.signal_performance import compute_signal_performance
from analytics.strategy_report import build_strategy_report
from data_layer.live_data.market_data_snapshot import capture_market_data_snapshot
from lifecycle.paper_trade import (
    cancel_paper_trade,
    close_paper_trade,
    create_paper_trade,
    open_paper_trade,
)
from lifecycle.signal_state import (
    SignalLifecycleState,
    derive_signal_lifecycle_state,
    transition_signal_state,
)
from lifecycle.trade_state import TradeState
from signals.schema import SignalSchema


def _approved_signal(**overrides) -> SignalSchema:
    base = dict(
        signal_id="sig-e2e",
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction="BUY",
        entry_price=2000.0,
        stop_loss=1990.0,
        take_profit=2020.0,
        decision="APPROVED",
        strategy_name="LIQUIDITY_SWEEP_STRATEGY",
        quality_grade="A+",
        context_id="ctx-e2e",
    )
    base.update(overrides)
    return SignalSchema(**base)


# --- Acceptance criterion: PaperTrade creation ---

def test_paper_trade_creation_from_an_approved_signal():
    signal = _approved_signal()

    trade = create_paper_trade(signal)

    assert trade.status == TradeState.CREATED
    assert trade.signal_id == signal.signal_id
    assert trade.entry == signal.entry_price


def test_paper_trade_creation_from_a_real_pipeline_signal(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """The pipeline's own real SignalSchema output (AC-03) is directly usable by create_paper_trade() when approved."""
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()
    record = result["signal_history"][0]

    if record.decision == "APPROVED":
        trade = create_paper_trade(record)
        assert trade.signal_id == record.signal_id
        assert trade.status == TradeState.CREATED


# --- Acceptance criterion: Signal lifecycle transition ---

def test_signal_lifecycle_transition_full_path():
    state = SignalLifecycleState.CREATED
    for next_state in (
        SignalLifecycleState.QUALITY_CHECKED,
        SignalLifecycleState.EXPLAINED,
        SignalLifecycleState.APPROVED,
        SignalLifecycleState.PAPER_OPEN,
        SignalLifecycleState.CLOSED,
    ):
        result = transition_signal_state(state, next_state)
        assert result.success is True
        state = next_state
    assert state == SignalLifecycleState.CLOSED


def test_signal_lifecycle_transition_derived_from_real_paper_trade():
    signal = _approved_signal()
    trade = create_paper_trade(signal)
    assert derive_signal_lifecycle_state(signal, paper_trade=trade) == SignalLifecycleState.APPROVED

    opened = open_paper_trade(trade).trade
    assert derive_signal_lifecycle_state(signal, paper_trade=opened) == SignalLifecycleState.PAPER_OPEN

    closed = close_paper_trade(opened, "TP").trade
    assert derive_signal_lifecycle_state(signal, paper_trade=closed) == SignalLifecycleState.CLOSED


# --- Acceptance criterion: Performance schema ---

def test_performance_schema_built_from_a_closed_paper_trade():
    signal = _approved_signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade

    performance = compute_signal_performance(signal, paper_trade=closed, session="LONDON", market_phase="MARKUP")

    assert performance.signal_id == signal.signal_id
    assert performance.strategy_id == "LIQUIDITY_SWEEP_STRATEGY"
    assert performance.result == "TP"
    assert performance.r_multiple == 2.0
    assert performance.session == "LONDON"
    assert performance.market_phase == "MARKUP"


def test_performance_schema_feeds_strategy_report():
    signal = _approved_signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade
    performance = compute_signal_performance(signal, paper_trade=closed)

    report = build_strategy_report([performance])

    assert report["LIQUIDITY_SWEEP_STRATEGY"].total_signals == 1
    assert report["LIQUIDITY_SWEEP_STRATEGY"].win_count == 1


# --- Acceptance criterion: Missing data handling ---

def test_missing_data_handling_empty_candles_never_raises():
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    assert snapshot.candle_count == 0


def test_missing_data_handling_no_candidates_still_produces_context(mock_pipeline):
    """No signal candidates this cycle -- MarketDataSnapshot/lifecycle/analytics must all still tolerate zero input."""
    pipeline = mock_pipeline([], [])

    result = pipeline.run()

    assert result["signal_history"] == []
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    assert snapshot.candle_count == 0
    # compute_signal_performance() with no paper trade at all -- must not raise on missing data
    unlinked_signal = _approved_signal(entry_price=None, stop_loss=None, take_profit=None, decision="PENDING")
    performance = compute_signal_performance(unlinked_signal)
    assert performance.result is None


def test_missing_data_handling_paper_trade_transitions_never_raise_on_bad_state():
    signal = _approved_signal()
    trade = create_paper_trade(signal)

    # Attempting to close a trade that was never opened -- a "missing data" style edge case.
    result = close_paper_trade(trade, "TP")

    assert result.success is False
    assert result.trade is trade  # unchanged, no exception


# --- Acceptance criterion: Context link preservation ---

def test_context_link_preservation_through_pipeline_and_paper_trade(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    result = pipeline.run()
    record = result["signal_history"][0]
    snapshot = result["context_snapshot"]

    # context_id survives from ContextSnapshotSchema -> SignalSchema (AC-03) ...
    assert record.context_id == snapshot.snapshot_id

    # ... and onward into SignalPerformance, without being recomputed.
    performance = compute_signal_performance(record)
    assert performance.context_id == record.context_id == snapshot.snapshot_id


def test_context_link_preservation_survives_a_cancelled_trade():
    signal = _approved_signal(context_id="ctx-preserved")
    trade = create_paper_trade(signal)
    cancelled = cancel_paper_trade(trade).trade

    performance = compute_signal_performance(signal, paper_trade=cancelled)

    assert performance.context_id == "ctx-preserved"  # unaffected by the trade's own outcome


# --- Acceptance criterion: Signal -> Result chain ---

def test_signal_to_result_chain_end_to_end():
    """Full chain: SignalSchema -> PaperTrade (CREATED -> OPEN -> CLOSED) -> SignalPerformance -> StrategyPerformanceReport."""
    signal = _approved_signal()

    trade = create_paper_trade(signal)
    assert trade.status == TradeState.CREATED

    trade = open_paper_trade(trade).trade
    assert trade.status == TradeState.OPEN

    trade = close_paper_trade(trade, "SL").trade
    assert trade.status == TradeState.CLOSED
    assert trade.result == "SL"

    performance = compute_signal_performance(signal, paper_trade=trade)
    assert performance.result == "SL"
    assert performance.r_multiple == -1.0

    report = build_strategy_report([performance])
    assert report["LIQUIDITY_SWEEP_STRATEGY"].loss_count == 1
    assert report["LIQUIDITY_SWEEP_STRATEGY"].win_rate == 0.0


def test_signal_to_result_chain_expired_never_opened():
    """A signal whose paper trade is cancelled before ever opening -- result reflects CANCELLED (Phase 59.4 TASK 1), no r_multiple, chain completes without error."""
    signal = _approved_signal()
    trade = create_paper_trade(signal)
    cancelled = cancel_paper_trade(trade).trade

    performance = compute_signal_performance(signal, paper_trade=cancelled)
    report = build_strategy_report([performance])

    assert performance.result == "CANCELLED"
    assert performance.r_multiple is None
    assert report["LIQUIDITY_SWEEP_STRATEGY"].total_signals == 1
    assert report["LIQUIDITY_SWEEP_STRATEGY"].win_count == 0
