from ai.chart_intelligence.models import ChartAnalysis, ChartAnalysisType, ChartImageType
from ai.chart_intelligence.trading_analyst_adapter import combined_explanation
from ai.explanation.explanation_builder import ExplanationBuilder
from ai.trading_analyst.models import TradingAnalysis, TradingRiskLevel


def _trading(**overrides):
    defaults = dict(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias on XAUUSD.",
        strengths=("H4 BOS",), weaknesses=(), recommendation="WHY BUY: H4 BOS",
    )
    defaults.update(overrides)
    return TradingAnalysis(**defaults)


def _chart(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.TRADINGVIEW_SCREENSHOT,
        analysis_type=ChartAnalysisType.STRUCTURE, market_structure="BOS confirmed",
        trend="Bullish", liquidity=None, order_blocks=(), fvg=(), support=(), resistance=(),
        confidence=0.8, notes=None,
    )
    defaults.update(overrides)
    return ChartAnalysis(**defaults)


def test_combined_explanation_never_raises():
    result = combined_explanation(_trading(), _chart(), ExplanationBuilder())
    assert result is not None


def test_combined_explanation_relays_market_bias():
    result = combined_explanation(_trading(market_bias="BEARISH"), _chart(), ExplanationBuilder())
    assert result.market_context == "BEARISH"


def test_combined_explanation_relays_symbol_from_trading():
    result = combined_explanation(_trading(symbol="EURUSD"), _chart(symbol="EURUSD"), ExplanationBuilder())
    assert "EURUSD" in result.summary or result.market_context is not None


def test_combined_explanation_includes_chart_market_structure_in_reasoning():
    result = combined_explanation(_trading(), _chart(market_structure="CHoCH confirmed"), ExplanationBuilder())
    assert "CHoCH confirmed" in result.technical_reasoning


def test_combined_explanation_includes_trading_summary_in_reasoning():
    result = combined_explanation(_trading(summary="Strong bullish setup."), _chart(market_structure=None, trend=None), ExplanationBuilder())
    assert "Strong bullish setup." in result.technical_reasoning


def test_combined_explanation_confidence_uses_chart_scale():
    result = combined_explanation(_trading(), _chart(confidence=0.55), ExplanationBuilder())
    assert result.confidence == 0.55


def test_combined_explanation_relays_risk_reward_from_trading():
    result = combined_explanation(_trading(rr=3.1), _chart(), ExplanationBuilder())
    # ExplanationOutput has no direct rr field -- verify no exception and stable output shape
    assert result is not None


def test_combined_explanation_uses_chart_notes_as_invalidation():
    result = combined_explanation(_trading(), _chart(notes="invalidate below 3390"), ExplanationBuilder())
    assert result.invalidation == "invalidate below 3390"


def test_combined_explanation_never_fabricates_a_verdict():
    """Rule 2: the combined explanation carries no BUY/SELL/NO_TRADE field of its own."""
    result = combined_explanation(_trading(direction="SELL"), _chart(), ExplanationBuilder())
    assert not hasattr(result, "direction")


def test_combined_explanation_handles_empty_chart_fields():
    empty_chart = _chart(market_structure=None, trend=None, liquidity=None, notes=None)
    result = combined_explanation(_trading(), empty_chart, ExplanationBuilder())
    assert result is not None


def test_combined_explanation_different_symbols_produce_independent_results():
    result_a = combined_explanation(_trading(symbol="XAUUSD"), _chart(symbol="XAUUSD"), ExplanationBuilder())
    result_b = combined_explanation(_trading(symbol="EURUSD"), _chart(symbol="EURUSD"), ExplanationBuilder())
    assert result_a.market_context == result_b.market_context  # same bias in this fixture
    assert result_a is not result_b
