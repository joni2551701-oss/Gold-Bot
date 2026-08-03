"""Phase 61.3 TASK 2 — ContextSnapshotSchema -> MarketContext adapter. ai/ never imports context/ at runtime."""

import sys

from ai.context.context_adapter import market_context_from_snapshot


def _schema(**overrides):
    from context_layer.context_engine.snapshot import ContextSnapshotSchema, LiquidityInfo, SessionInfo, StructureInfo, ZonesInfo, generate_snapshot_id
    from datetime import datetime, timezone

    defaults = dict(
        snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc),
        symbol="XAUUSD", timeframe="M15",
        structure=StructureInfo(trend="BULLISH", bos=True, choch=False, swing_state="HH"),
        liquidity=LiquidityInfo(sweep_detected=True, liquidity_type="BUY_SIDE_LIQUIDITY"),
        zones=ZonesInfo(order_block=True, fvg=False),
        session=SessionInfo(current_session="LONDON"),
        regime="TRENDING",
    )
    defaults.update(overrides)
    return ContextSnapshotSchema(**defaults)


def test_ai_context_adapter_module_never_imports_context_at_runtime():
    """
    Fresh-import check: ai/context/context_adapter.py's context.snapshot
    reference is TYPE_CHECKING-only. Saves and restores every removed
    sys.modules entry in a finally block -- permanently dropping
    context.* here would force every later test to re-import it fresh,
    producing a *new* class object for anything like context_layer.trend.htf_bias.HTFBias
    with a different identity than the one other already-imported code
    holds a reference to (enums compare by identity), breaking unrelated
    tests elsewhere in the suite. Discovered via a real full-suite
    regression this exact bug caused before this fix.
    """
    saved_context_modules = {
        mod: sys.modules[mod] for mod in list(sys.modules)
        if mod == "context_layer" or mod.startswith("context_layer.")
    }
    saved_adapter = sys.modules.pop("ai.context.context_adapter", None)
    for mod in saved_context_modules:
        del sys.modules[mod]

    try:
        import ai.context.context_adapter

        assert hasattr(ai.context.context_adapter, "market_context_from_snapshot")
        assert "context_layer.context_engine.snapshot" not in sys.modules
        assert "context_layer" not in sys.modules
    finally:
        sys.modules.update(saved_context_modules)
        if saved_adapter is not None:
            sys.modules["ai.context.context_adapter"] = saved_adapter


def test_symbol_and_timeframe_carry_through():
    mc = market_context_from_snapshot(_schema())
    assert mc.symbol == "XAUUSD"
    assert mc.timeframe == "M15"


def test_summary_includes_regime_and_trend():
    mc = market_context_from_snapshot(_schema())
    assert "Regime: TRENDING" in mc.summary
    assert "Trend: BULLISH" in mc.summary


def test_summary_includes_bos_choch_when_detected():
    mc = market_context_from_snapshot(_schema())
    assert "BOS detected" in mc.summary
    assert "CHoCH detected" not in mc.summary


def test_summary_includes_liquidity_and_zones():
    mc = market_context_from_snapshot(_schema())
    assert "Liquidity sweep: BUY_SIDE_LIQUIDITY" in mc.summary
    assert "Order block present" in mc.summary
    assert "Fair value gap present" not in mc.summary


def test_summary_includes_session():
    mc = market_context_from_snapshot(_schema())
    assert "Session: LONDON" in mc.summary


def test_metadata_carries_snapshot_id():
    schema = _schema()
    mc = market_context_from_snapshot(schema)
    assert mc.metadata["snapshot_id"] == schema.snapshot_id


def test_degenerate_schema_falls_back_to_unknown_symbol_timeframe():
    from context_layer.context_engine.snapshot import ContextSnapshotSchema, generate_snapshot_id
    from datetime import datetime, timezone

    empty_schema = ContextSnapshotSchema(snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc))
    mc = market_context_from_snapshot(empty_schema)
    assert mc.symbol == "UNKNOWN"
    assert mc.timeframe == "UNKNOWN"


def test_no_raw_candle_data_can_appear_in_metadata():
    mc = market_context_from_snapshot(_schema())
    assert "candles" not in mc.metadata
    assert "raw_candles" not in mc.metadata
