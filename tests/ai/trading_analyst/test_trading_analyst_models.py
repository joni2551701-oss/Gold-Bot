from ai_layer.ai_engine.trading_analyst.models import TradingAnalysis, TradingAnalysisInput, TradingRiskLevel


def test_trading_analysis_input_required_fields():
    data = TradingAnalysisInput(symbol="XAUUSD", direction="BUY", market_bias="BULLISH")
    assert data.symbol == "XAUUSD"
    assert data.direction == "BUY"
    assert data.market_bias == "BULLISH"


def test_trading_analysis_input_defaults():
    data = TradingAnalysisInput(symbol="XAUUSD", direction="BUY", market_bias="BULLISH")
    assert data.confidence == 0.0
    assert data.signal_score == 0.0
    assert data.htf_score == 0.0
    assert data.risk_score == 0.0
    assert data.ai_score == 0.0
    assert data.risk_level == TradingRiskLevel.MEDIUM
    assert data.risk_reward is None
    assert data.entry is None
    assert data.strengths == ()
    assert data.weaknesses == ()
    assert data.language == "en"


def test_trading_analysis_input_is_frozen():
    data = TradingAnalysisInput(symbol="XAUUSD", direction="BUY", market_bias="BULLISH")
    try:
        data.symbol = "EURUSD"
        assert False, "TradingAnalysisInput should be frozen"
    except AttributeError:
        pass


def test_trading_analysis_input_market_analysis_fields():
    data = TradingAnalysisInput(
        symbol="XAUUSD", direction="BUY", market_bias="BULLISH",
        session="London", htf_trend="Uptrend", liquidity_note="Sweep below 3360",
        structure_note="BOS confirmed", volume_note="Above average",
        volatility_note="Normal",
    )
    assert data.session == "London"
    assert data.htf_trend == "Uptrend"
    assert data.liquidity_note == "Sweep below 3360"
    assert data.structure_note == "BOS confirmed"
    assert data.volume_note == "Above average"
    assert data.volatility_note == "Normal"


def test_trading_analysis_input_strengths_and_weaknesses():
    data = TradingAnalysisInput(
        symbol="XAUUSD", direction="BUY", market_bias="BULLISH",
        strengths=["H4 BOS", "Liquidity Sweep"], weaknesses=["Low volume"],
    )
    assert data.strengths == ["H4 BOS", "Liquidity Sweep"]
    assert data.weaknesses == ["Low volume"]


def test_trading_analysis_input_has_no_trading_core_object_fields():
    """Regression guard: TradingAnalysisInput must never carry a decision/risk object field -- Article 3 resolution."""
    field_names = set(TradingAnalysisInput.__dataclass_fields__.keys())
    forbidden = {"trade_decision", "risk_result", "signal", "signal_candidate", "decision", "risk"}
    assert field_names.isdisjoint(forbidden)


def test_trading_risk_level_members():
    assert TradingRiskLevel.LOW.value == "LOW"
    assert TradingRiskLevel.MEDIUM.value == "MEDIUM"
    assert TradingRiskLevel.HIGH.value == "HIGH"


def test_trading_analysis_required_fields():
    analysis = TradingAnalysis(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias.",
        strengths=("H4 BOS",), weaknesses=(), recommendation="WHY BUY: H4 BOS",
    )
    assert analysis.symbol == "XAUUSD"
    assert analysis.direction == "BUY"
    assert analysis.confidence == 0.82
    assert analysis.risk_level == TradingRiskLevel.MEDIUM


def test_trading_analysis_defaults():
    analysis = TradingAnalysis(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias.",
        strengths=(), weaknesses=(), recommendation="WHY BUY",
    )
    assert analysis.educational_note is None
    assert analysis.generated_at == ""


def test_trading_analysis_is_frozen():
    analysis = TradingAnalysis(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias.",
        strengths=(), weaknesses=(), recommendation="WHY BUY",
    )
    try:
        analysis.symbol = "EURUSD"
        assert False, "TradingAnalysis should be frozen"
    except AttributeError:
        pass


def test_trading_analysis_has_no_provider_field():
    field_names = set(TradingAnalysis.__dataclass_fields__.keys())
    assert "provider" not in field_names


def test_trading_analysis_field_names_match_task_2_contract():
    """TASK 2's own named field list, verified exhaustively."""
    field_names = set(TradingAnalysis.__dataclass_fields__.keys())
    assert field_names == {
        "symbol", "direction", "confidence", "market_bias", "risk_level", "rr",
        "summary", "strengths", "weaknesses", "recommendation", "educational_note",
        "generated_at",
    }


def test_trading_risk_level_has_exactly_three_members():
    assert len(TradingRiskLevel) == 3


def test_trading_analysis_equality_by_value():
    a = TradingAnalysis(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias.",
        strengths=("H4 BOS",), weaknesses=(), recommendation="WHY BUY",
    )
    b = TradingAnalysis(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias.",
        strengths=("H4 BOS",), weaknesses=(), recommendation="WHY BUY",
    )
    assert a == b


def test_trading_analysis_input_equality_by_value():
    a = TradingAnalysisInput(symbol="XAUUSD", direction="BUY", market_bias="BULLISH")
    b = TradingAnalysisInput(symbol="XAUUSD", direction="BUY", market_bias="BULLISH")
    assert a == b


def test_trading_analysis_input_risk_reasoning_fields():
    data = TradingAnalysisInput(
        symbol="XAUUSD", direction="BUY", market_bias="BULLISH",
        technical_reason="H4 BOS", risk_reason="Below 3362", invalidation="Close below 3362",
    )
    assert data.technical_reason == "H4 BOS"
    assert data.risk_reason == "Below 3362"
    assert data.invalidation == "Close below 3362"


def test_trading_analysis_input_price_fields():
    data = TradingAnalysisInput(
        symbol="XAUUSD", direction="BUY", market_bias="BULLISH",
        entry=3400.0, stop_loss=3362.0, take_profit=3480.0,
    )
    assert data.entry == 3400.0
    assert data.stop_loss == 3362.0
    assert data.take_profit == 3480.0
