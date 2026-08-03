from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.trading_analyst.analyst_runtime import TradingAnalystRuntime
from ai_layer.ai_engine.trading_analyst.models import TradingAnalysisInput, TradingRiskLevel
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_trading_analyst=True)
DISABLED = FeatureFlags(enable_trading_analyst=False)


def _input(**overrides):
    defaults = dict(
        symbol="XAUUSD", direction="BUY", market_bias="BULLISH", confidence=82.0,
        signal_score=0.8, htf_score=0.9, risk_score=0.6, ai_score=0.75,
        risk_level=TradingRiskLevel.MEDIUM, risk_reward=2.5,
        entry=3400.0, stop_loss=3362.0, take_profit=3480.0,
        technical_reason="H4 BOS + Liquidity Sweep + Bullish OB + Discount Zone",
        risk_reason="Invalidation below 3362", invalidation="Close below 3362",
        strengths=["H4 BOS", "Liquidity Sweep", "Bullish Order Block", "Discount Zone"],
        weaknesses=["Low volume on H1"],
    )
    defaults.update(overrides)
    return TradingAnalysisInput(**defaults)


def _runtime(flags=ENABLED):
    return TradingAnalystRuntime(flags=flags)


def test_analyze_owner_succeeds():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result is not None
    assert result.symbol == "XAUUSD"
    assert result.direction == "BUY"


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


def test_analyze_relays_market_bias():
    result = _runtime().analyze(_input(market_bias="BEARISH"), AIRole.OWNER)
    assert result.market_bias == "BEARISH"


def test_analyze_relays_risk_level_never_computes_it():
    result = _runtime().analyze(_input(risk_level=TradingRiskLevel.HIGH), AIRole.OWNER)
    assert result.risk_level == TradingRiskLevel.HIGH


def test_analyze_relays_rr():
    result = _runtime().analyze(_input(risk_reward=3.1), AIRole.OWNER)
    assert result.rr == 3.1


def test_analyze_relays_strengths_and_weaknesses():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.strengths == ("H4 BOS", "Liquidity Sweep", "Bullish Order Block", "Discount Zone")
    assert result.weaknesses == ("Low volume on H1",)


def test_analyze_recommendation_uses_direction_and_first_strength():
    result = _runtime().analyze(_input(direction="SELL", strengths=["Bearish OB"]), AIRole.OWNER)
    assert result.recommendation == "WHY SELL: Bearish OB"


def test_analyze_recommendation_falls_back_to_technical_reason_without_strengths():
    result = _runtime().analyze(_input(direction="WAIT", strengths=[], technical_reason="No confirmation yet"), AIRole.OWNER)
    assert result.recommendation == "WHY WAIT: No confirmation yet"


def test_analyze_recommendation_never_fabricates_a_new_verdict():
    """Director Note 1: recommendation must echo direction, never invent BUY/SELL on its own."""
    for direction in ("BUY", "SELL", "WAIT", "SKIP"):
        result = _runtime().analyze(_input(direction=direction), AIRole.OWNER)
        assert result.direction == direction
        assert result.recommendation.startswith(f"WHY {direction}")


def test_analyze_sets_generated_at():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.generated_at != ""


def test_analyze_summary_comes_from_explanation_builder():
    result = _runtime().analyze(_input(market_bias="BULLISH"), AIRole.OWNER)
    assert "BULLISH" in result.summary
    assert result.symbol in result.summary


def test_analyze_never_raises_for_minimal_input():
    minimal = TradingAnalysisInput(symbol="EURUSD", direction="WAIT", market_bias="NEUTRAL")
    result = _runtime().analyze(minimal, AIRole.OWNER)
    assert result is not None


def test_analyze_never_raises_across_all_roles():
    for role in AIRole:
        result = _runtime().analyze(_input(), role)
        assert result is None or result.symbol == "XAUUSD"


def test_runtime_default_construction_never_raises():
    runtime = TradingAnalystRuntime()
    assert runtime is not None


def test_runtime_accepts_injected_intelligence_runtime():
    from ai_layer.ai_engine.intelligence_runtime import IntelligenceRuntime
    injected = IntelligenceRuntime()
    runtime = TradingAnalystRuntime(intelligence_runtime=injected, flags=ENABLED)
    result = runtime.analyze(_input(), AIRole.OWNER)
    assert result is not None


def test_runtime_accepts_injected_explanation_builder():
    from ai_layer.explanation_ai.explanation_builder import ExplanationBuilder
    injected = ExplanationBuilder()
    runtime = TradingAnalystRuntime(explanation_builder=injected, flags=ENABLED)
    result = runtime.analyze(_input(), AIRole.OWNER)
    assert result is not None


def test_analyze_relays_language_into_explanation():
    result = _runtime().analyze(_input(language="uz"), AIRole.OWNER)
    assert result is not None


def test_analyze_skip_direction_recommendation():
    result = _runtime().analyze(_input(direction="SKIP", strengths=["No clear setup"]), AIRole.OWNER)
    assert result.recommendation == "WHY SKIP: No clear setup"


def test_analyze_educational_note_is_none_for_trade_mode_without_lesson():
    result = _runtime().analyze(_input(), AIRole.OWNER)
    assert result.educational_note is None


def test_analyze_low_risk_level_relayed():
    result = _runtime().analyze(_input(risk_level=TradingRiskLevel.LOW), AIRole.OWNER)
    assert result.risk_level == TradingRiskLevel.LOW
