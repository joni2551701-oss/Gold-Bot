import dataclasses

from ai.chart_intelligence.models import (
    ChartAnalysis,
    ChartAnalysisInput,
    ChartAnalysisType,
    ChartContext,
    ChartImageType,
    has_minimum_context,
)


def test_chart_image_type_has_five_members():
    assert len(list(ChartImageType)) == 5


def test_chart_image_type_members():
    values = {m.value for m in ChartImageType}
    assert values == {
        "TRADINGVIEW_SCREENSHOT", "MT5_SCREENSHOT", "TELEGRAM_IMAGE", "PDF_CHART", "OTHER",
    }


def test_chart_analysis_type_has_seven_members():
    assert len(list(ChartAnalysisType)) == 7


def test_chart_analysis_type_members():
    values = {m.value for m in ChartAnalysisType}
    assert values == {
        "STRUCTURE", "TREND", "LIQUIDITY", "ORDER_BLOCK", "FVG", "SUPPORT_RESISTANCE", "GENERAL",
    }


def test_chart_analysis_input_defaults():
    data = ChartAnalysisInput(symbol="XAUUSD", timeframe="H4")
    assert data.image_type == ChartImageType.OTHER
    assert data.analysis_type == ChartAnalysisType.GENERAL
    assert data.market_structure is None
    assert data.trend is None
    assert data.liquidity is None
    assert data.order_blocks == ()
    assert data.fvg == ()
    assert data.support == ()
    assert data.resistance == ()
    assert data.confidence == 0.0
    assert data.notes is None
    assert data.language == "en"


def test_chart_analysis_input_is_frozen():
    data = ChartAnalysisInput(symbol="XAUUSD", timeframe="H4")
    try:
        data.symbol = "EURUSD"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_chart_analysis_input_accepts_all_fields():
    data = ChartAnalysisInput(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.MT5_SCREENSHOT,
        analysis_type=ChartAnalysisType.LIQUIDITY, market_structure="BOS", trend="Bullish",
        liquidity="Sweep", order_blocks=["3400 OB"], fvg=["3395-3398"], support=["3390"],
        resistance=["3420"], confidence=75.0, notes="clean setup", language="uz",
    )
    assert data.image_type == ChartImageType.MT5_SCREENSHOT
    assert data.analysis_type == ChartAnalysisType.LIQUIDITY
    assert data.order_blocks == ["3400 OB"]
    assert data.language == "uz"


def test_chart_analysis_is_frozen():
    analysis = ChartAnalysis(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0, notes=None,
    )
    try:
        analysis.symbol = "EURUSD"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_chart_analysis_generated_at_defaults_empty():
    analysis = ChartAnalysis(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0, notes=None,
    )
    assert analysis.generated_at == ""


def test_chart_analysis_field_names_match_task_2_contract():
    """Phase 66.2 TASK 1 added chart_id (LOCK-permitted extension) -- see docs/PHASE66_2_AUDIT.md."""
    field_names = {f.name for f in dataclasses.fields(ChartAnalysis)}
    assert field_names == {
        "symbol", "timeframe", "image_type", "analysis_type", "market_structure", "trend",
        "liquidity", "order_blocks", "fvg", "support", "resistance", "confidence", "notes",
        "generated_at", "chart_id",
    }


def test_chart_analysis_input_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(ChartAnalysisInput)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_chart_context_defaults():
    ctx = ChartContext(source="telegram")
    assert ctx.resolution is None
    assert ctx.platform is None
    assert ctx.created_at == ""
    assert ctx.image_hash is None


def test_chart_context_is_frozen():
    ctx = ChartContext(source="telegram")
    try:
        ctx.source = "mt5"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_chart_context_field_names_match_task_3_contract():
    field_names = {f.name for f in dataclasses.fields(ChartContext)}
    assert field_names == {"source", "resolution", "platform", "created_at", "image_hash"}


def test_chart_context_never_stores_image_bytes():
    """Director Note 4: no field on ChartContext carries a binary payload -- image_hash is a plain string reference only."""
    for f in dataclasses.fields(ChartContext):
        assert "bytes" not in str(f.type).lower()
        assert "binary" not in str(f.type).lower()


def test_chart_context_accepts_full_metadata():
    ctx = ChartContext(source="tradingview", resolution="1920x1080", platform="TradingView Desktop",
                        created_at="2026-01-01T00:00:00Z", image_hash="abc123")
    assert ctx.source == "tradingview"
    assert ctx.image_hash == "abc123"


def test_has_minimum_context_true_for_populated_source():
    assert has_minimum_context(ChartContext(source="telegram")) is True


def test_has_minimum_context_false_for_empty_source():
    assert has_minimum_context(ChartContext(source="")) is False


def test_has_minimum_context_never_raises():
    for source in ("telegram", "", "mt5", "pdf"):
        result = has_minimum_context(ChartContext(source=source))
        assert isinstance(result, bool)


def test_chart_analysis_order_blocks_is_sequence():
    analysis = ChartAnalysis(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=("3400 OB",), fvg=(), support=(), resistance=(),
        confidence=0.0, notes=None,
    )
    assert analysis.order_blocks == ("3400 OB",)


def test_chart_analysis_equality():
    kwargs = dict(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0,
        notes=None, generated_at="2026-01-01",
    )
    a = ChartAnalysis(**kwargs)
    b = ChartAnalysis(**kwargs)
    assert a == b


def test_chart_analysis_inequality_on_symbol():
    kwargs = dict(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0, notes=None,
    )
    a = ChartAnalysis(**kwargs)
    b = ChartAnalysis(**{**kwargs, "symbol": "EURUSD"})
    assert a != b
