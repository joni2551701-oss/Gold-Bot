from ai.access.permissions import AIRole
from ai.chart_intelligence.chart_runtime import ChartRuntime
from ai.chart_intelligence.models import ChartAnalysisInput, ChartAnalysisType, ChartImageType
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_chart_intelligence=True)
DISABLED = FeatureFlags(enable_chart_intelligence=False)


def _input(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="H4", image_type=ChartImageType.TRADINGVIEW_SCREENSHOT,
        analysis_type=ChartAnalysisType.STRUCTURE, market_structure="BOS confirmed",
        trend="Bullish", liquidity="Sweep below 3390", order_blocks=["3400 bullish OB"],
        fvg=["3395-3398"], support=["3390"], resistance=["3420"], confidence=82.0,
        notes="Clean structure",
    )
    defaults.update(overrides)
    return ChartAnalysisInput(**defaults)


def _runtime(flags=ENABLED):
    return ChartRuntime(flags=flags)


def test_analyze_owner_succeeds():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result is not None
    assert result.symbol == "XAUUSD"
    assert result.timeframe == "H4"


def test_analyze_admin_blocked():
    assert _runtime().analyze(_input(), AIRole.ADMIN) is None


def test_analyze_vip_blocked():
    assert _runtime().analyze(_input(), AIRole.VIP) is None


def test_analyze_premium_blocked():
    assert _runtime().analyze(_input(), AIRole.PREMIUM) is None


def test_analyze_free_blocked():
    assert _runtime().analyze(_input(), AIRole.FREE) is None


def test_analyze_blocked_when_flag_disabled_even_for_owner():
    assert _runtime(flags=DISABLED).analyze(_input(), AIRole.OWNER) is None


def test_analyze_confidence_scaled_to_unit_range():
    result = _runtime().analyze(_input(confidence=82.0), AIRole.OWNER)
    assert result.confidence == 0.82


def test_analyze_confidence_clamps_out_of_range_values():
    result_high = _runtime().analyze(_input(confidence=150.0), AIRole.OWNER)
    assert result_high.confidence == 1.0
    result_low = _runtime().analyze(_input(confidence=-10.0), AIRole.OWNER)
    assert result_low.confidence == 0.0


def test_analyze_relays_image_type_never_computes_it():
    result = _runtime().analyze(_input(image_type=ChartImageType.MT5_SCREENSHOT), AIRole.OWNER)
    assert result.image_type == ChartImageType.MT5_SCREENSHOT


def test_analyze_relays_analysis_type():
    result = _runtime().analyze(_input(analysis_type=ChartAnalysisType.FVG), AIRole.OWNER)
    assert result.analysis_type == ChartAnalysisType.FVG


def test_analyze_relays_market_structure_trend_liquidity():
    result = _runtime().analyze(_input(market_structure="CHoCH", trend="Bearish", liquidity="Grab above 3420"), AIRole.OWNER)
    assert result.market_structure == "CHoCH"
    assert result.trend == "Bearish"
    assert result.liquidity == "Grab above 3420"


def test_analyze_relays_order_blocks_fvg_support_resistance():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.order_blocks == ("3400 bullish OB",)
    assert result.fvg == ("3395-3398",)
    assert result.support == ("3390",)
    assert result.resistance == ("3420",)


def test_analyze_relays_notes():
    result = _runtime().analyze(_input(notes="watch for retest"), AIRole.OWNER)
    assert result.notes == "watch for retest"


def test_analyze_sets_generated_at():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.generated_at != ""


def test_analyze_sets_chart_id():
    """Phase 66.2 TASK 1 extension -- every analyze() call stamps a non-empty chart_id."""
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.chart_id != ""
    assert result.chart_id.startswith("chart_")


def test_analyze_chart_id_unique_across_calls():
    runtime = _runtime()
    result_a = runtime.analyze(_input(), AIRole.OWNER)
    result_b = runtime.analyze(_input(), AIRole.OWNER)
    assert result_a.chart_id != result_b.chart_id


def test_analyze_never_raises_for_minimal_input():
    minimal = ChartAnalysisInput(symbol="EURUSD", timeframe="M15")
    result = _runtime().analyze(minimal, AIRole.OWNER)
    assert result is not None


def test_analyze_never_raises_across_all_roles():
    for role in AIRole:
        result = _runtime().analyze(_input(), role)
        assert result is None or result.symbol == "XAUUSD"


def test_analyze_never_produces_buy_sell_verdict():
    """Rule 2: ChartAnalysis has no direction/verdict field at all."""
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert not hasattr(result, "direction")
    assert not hasattr(result, "recommendation")


def test_runtime_default_construction_never_raises():
    runtime = ChartRuntime()
    assert runtime is not None


def test_runtime_accepts_injected_explanation_builder():
    from ai.explanation.explanation_builder import ExplanationBuilder
    injected = ExplanationBuilder()
    runtime = ChartRuntime(explanation_builder=injected, flags=ENABLED)
    result = runtime.analyze(_input(), AIRole.OWNER)
    assert result is not None


def test_explain_owner_succeeds():
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    explanation = _runtime().explain(chart, AIRole.OWNER)
    assert explanation is not None
    assert "STRUCTURE" in explanation.summary or chart.symbol in explanation.summary


def test_explain_admin_blocked():
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    assert _runtime().explain(chart, AIRole.ADMIN) is None


def test_explain_blocked_when_flag_disabled():
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    assert _runtime(flags=DISABLED).explain(chart, AIRole.OWNER) is None


def test_explain_uses_education_mode_never_trade_mode_verdict():
    """Rule 2: Chart Intelligence never produces a TRADE-mode BUY/SELL/NO_TRADE verdict on its own."""
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    explanation = _runtime().explain(chart, AIRole.OWNER)
    assert explanation.educational_note is None or isinstance(explanation.educational_note, str)


def test_explain_relays_language():
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    explanation = _runtime().explain(chart, AIRole.OWNER, language="uz")
    assert explanation.language == "uz"


def test_explain_falls_back_when_no_market_structure():
    chart = _runtime().analyze(_input(market_structure=None, trend=None, liquidity=None), AIRole.OWNER)
    explanation = _runtime().explain(chart, AIRole.OWNER)
    assert explanation is not None


def test_explain_never_raises_across_all_roles():
    chart = _runtime().analyze(_input(), AIRole.OWNER)
    for role in AIRole:
        result = _runtime().explain(chart, role)
        assert result is None or result.summary != ""
