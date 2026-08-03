"""Phase 61.0 TASK 5 — AI Context Builder: pure composition, AI never receives raw market data."""

from datetime import datetime, timezone

from ai_layer.ai_engine.context.context_adapter import sanitize_market_context
from ai_layer.ai_engine.context.context_builder import build_ai_context
from ai_layer.ai_service.interfaces import MarketContext
from ai_layer.knowledge_ai.knowledge_base.journal.trade_journal import DecisionType, SignalType, TradeOutcome, create_journal_entry
from ai_layer.knowledge_ai.learning_context import build_learning_context
from ai_layer.personal_ai.user_profile.user_profile import AIUserProfile
from signal_layer.signal_builder.schema import SignalSchema, generate_signal_id


def test_build_ai_context_with_no_inputs_returns_all_empty():
    ctx = build_ai_context()
    assert ctx.market_context is None
    assert ctx.signal is None
    assert ctx.user_profile is None
    assert ctx.trade_history == []
    assert ctx.learning_context is None
    assert ctx.built_at is not None


def test_build_ai_context_composes_every_named_input():
    market_context = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend")
    signal = SignalSchema(
        signal_id=generate_signal_id(), created_at=datetime.now(timezone.utc),
        symbol="XAUUSD", timeframe="M15", direction="BUY",
    )
    profile = AIUserProfile(telegram_id="123", experience_level="beginner")
    trade = create_journal_entry(
        signal_id="s1", strategy_name="LIQUIDITY_SWEEP", signal_type=SignalType.BUY,
        technical_score=80.0, ai_confidence=0.7, decision=DecisionType.APPROVED,
        entry=2000.0, stop_loss=1990.0, take_profit=2020.0, exit_price=2020.0,
        pnl=20.0, rr=2.0, outcome=TradeOutcome.WIN, timestamp=datetime.now(timezone.utc),
    )
    learning_context = build_learning_context(records=[])

    ctx = build_ai_context(
        market_context=market_context, signal=signal, user_profile=profile,
        trade_history=[trade], learning_context=learning_context,
    )

    assert ctx.market_context is market_context
    assert ctx.signal is signal
    assert ctx.user_profile is profile
    assert ctx.trade_history == [trade]
    assert ctx.learning_context is learning_context


def test_to_dict_is_json_safe():
    market_context = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend")
    ctx = build_ai_context(market_context=market_context)
    data = ctx.to_dict()
    assert data["market_context"]["symbol"] == "XAUUSD"
    assert data["trade_history_count"] == 0
    assert isinstance(data["built_at"], str)


def test_sanitize_market_context_strips_forbidden_raw_keys():
    dirty = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend", metadata={"candles": [1, 2, 3], "note": "kept"})
    clean = sanitize_market_context(dirty)
    assert "candles" not in clean.metadata
    assert clean.metadata["note"] == "kept"


def test_sanitize_market_context_passes_through_clean_context_unchanged():
    clean_input = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend", metadata={"note": "kept"})
    result = sanitize_market_context(clean_input)
    assert result is clean_input


def test_sanitize_market_context_handles_none():
    assert sanitize_market_context(None) is None


def test_build_ai_context_sanitizes_market_context_automatically():
    dirty = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend", metadata={"raw_candles": []})
    ctx = build_ai_context(market_context=dirty)
    assert "raw_candles" not in ctx.market_context.metadata
