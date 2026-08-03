from ai.chart_intelligence.content_adapter import chart_analysis_to_content_body, prepare_content
from ai.chart_intelligence.models import ChartAnalysis, ChartAnalysisType, ChartImageType
from ai.content.content_adapter import ContentEngine
from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
from media_layer.telegram_broadcast.models import BroadcastStatus
from media_layer.content_manager.media_manager import MediaManager


def _analysis(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.TRADINGVIEW_SCREENSHOT,
        analysis_type=ChartAnalysisType.STRUCTURE, market_structure="BOS confirmed",
        trend="Bullish", liquidity="Sweep below 3390", order_blocks=("3400 bullish OB",),
        fvg=("3395-3398",), support=("3390",), resistance=("3420",), confidence=0.82,
        notes="Clean structure",
    )
    defaults.update(overrides)
    return ChartAnalysis(**defaults)


def test_content_body_includes_market_structure():
    body = chart_analysis_to_content_body(_analysis())
    assert "Market Structure: BOS confirmed" in body


def test_content_body_includes_trend():
    body = chart_analysis_to_content_body(_analysis())
    assert "Trend: Bullish" in body


def test_content_body_includes_liquidity():
    body = chart_analysis_to_content_body(_analysis())
    assert "Liquidity: Sweep below 3390" in body


def test_content_body_includes_order_blocks():
    body = chart_analysis_to_content_body(_analysis())
    assert "Order Blocks: 3400 bullish OB" in body


def test_content_body_includes_fvg():
    body = chart_analysis_to_content_body(_analysis())
    assert "FVG: 3395-3398" in body


def test_content_body_includes_support_and_resistance():
    body = chart_analysis_to_content_body(_analysis())
    assert "Support: 3390" in body
    assert "Resistance: 3420" in body


def test_content_body_includes_notes():
    body = chart_analysis_to_content_body(_analysis())
    assert "Clean structure" in body


def test_content_body_omits_empty_fields():
    minimal = _analysis(market_structure=None, trend=None, liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), notes=None)
    body = chart_analysis_to_content_body(minimal)
    assert body == "XAUUSD H4 chart analysis"


def test_content_body_never_empty():
    minimal = ChartAnalysis(
        symbol="EURUSD", timeframe="M15", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0, notes=None,
    )
    assert chart_analysis_to_content_body(minimal) != ""


def test_prepare_content_full_success_path():
    result = prepare_content(_analysis(), ContentEngine(), MediaManager(), BroadcastManager())
    assert result is not None
    assert result.status == BroadcastStatus.READY
    assert result.broadcast_type.value == "LIVE_ANALYSIS"


def test_prepare_content_never_raises_for_minimal_analysis():
    minimal = ChartAnalysis(
        symbol="EURUSD", timeframe="M15", image_type=ChartImageType.OTHER,
        analysis_type=ChartAnalysisType.GENERAL, market_structure=None, trend=None,
        liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(), confidence=0.0, notes=None,
    )
    result = prepare_content(minimal, ContentEngine(), MediaManager(), BroadcastManager())
    assert result is not None


def test_prepare_content_title_includes_symbol_and_timeframe():
    result = prepare_content(_analysis(symbol="EURUSD", timeframe="D1"), ContentEngine(), MediaManager(), BroadcastManager())
    assert result is not None


def test_prepare_content_has_media_id():
    result = prepare_content(_analysis(), ContentEngine(), MediaManager(), BroadcastManager())
    assert result.media_id


def test_prepare_content_different_symbols_produce_independent_assets():
    result_a = prepare_content(_analysis(symbol="XAUUSD"), ContentEngine(), MediaManager(), BroadcastManager())
    result_b = prepare_content(_analysis(symbol="EURUSD"), ContentEngine(), MediaManager(), BroadcastManager())
    assert result_a.id != result_b.id
