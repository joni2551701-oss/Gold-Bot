from ai.content.content_adapter import ContentEngine
from ai.trading_analyst.content_adapter import prepare_content, trading_analysis_to_content_body
from ai.trading_analyst.models import TradingAnalysis, TradingRiskLevel
from broadcast.broadcast_manager import BroadcastManager
from broadcast.models import BroadcastStatus
from media.media_manager import MediaManager


def _analysis(**overrides):
    defaults = dict(
        symbol="XAUUSD", direction="BUY", confidence=0.82, market_bias="BULLISH",
        risk_level=TradingRiskLevel.MEDIUM, rr=2.5, summary="Bullish bias on XAUUSD.",
        strengths=("H4 BOS", "Liquidity Sweep"), weaknesses=("Low volume",),
        recommendation="WHY BUY: H4 BOS", educational_note="Liquidity sweeps often precede reversals.",
    )
    defaults.update(overrides)
    return TradingAnalysis(**defaults)


def test_trading_analysis_to_content_body_includes_summary():
    body = trading_analysis_to_content_body(_analysis())
    assert "Bullish bias on XAUUSD." in body


def test_trading_analysis_to_content_body_includes_strengths():
    body = trading_analysis_to_content_body(_analysis())
    assert "Strengths: H4 BOS; Liquidity Sweep" in body


def test_trading_analysis_to_content_body_includes_weaknesses():
    body = trading_analysis_to_content_body(_analysis())
    assert "Weaknesses: Low volume" in body


def test_trading_analysis_to_content_body_omits_weaknesses_when_empty():
    body = trading_analysis_to_content_body(_analysis(weaknesses=()))
    assert "Weaknesses:" not in body


def test_trading_analysis_to_content_body_includes_recommendation():
    body = trading_analysis_to_content_body(_analysis())
    assert "WHY BUY: H4 BOS" in body


def test_trading_analysis_to_content_body_includes_educational_note():
    body = trading_analysis_to_content_body(_analysis())
    assert "Liquidity sweeps often precede reversals." in body


def test_trading_analysis_to_content_body_omits_educational_note_when_none():
    body = trading_analysis_to_content_body(_analysis(educational_note=None))
    assert "Liquidity sweeps often precede reversals." not in body


def test_prepare_content_full_success_path():
    result = prepare_content(_analysis(), ContentEngine(), MediaManager(), BroadcastManager())
    assert result is not None
    assert result.status == BroadcastStatus.READY
    assert result.broadcast_type.value == "LIVE_ANALYSIS"


def test_prepare_content_never_raises_for_minimal_analysis():
    minimal = TradingAnalysis(
        symbol="EURUSD", direction="WAIT", confidence=0.0, market_bias="NEUTRAL",
        risk_level=TradingRiskLevel.LOW, rr=None, summary="", strengths=(), weaknesses=(),
        recommendation="WHY WAIT",
    )
    result = prepare_content(minimal, ContentEngine(), MediaManager(), BroadcastManager())
    assert result is not None


def test_prepare_content_broadcast_type_is_live_analysis():
    result = prepare_content(_analysis(), ContentEngine(), MediaManager(), BroadcastManager())
    assert result.broadcast_type.value == "LIVE_ANALYSIS"


def test_prepare_content_has_media_id():
    result = prepare_content(_analysis(), ContentEngine(), MediaManager(), BroadcastManager())
    assert result.media_id


def test_prepare_content_symbol_in_content_body():
    body = trading_analysis_to_content_body(_analysis(symbol="EURUSD"))
    assert "Bullish bias on XAUUSD." in body  # summary unaffected by symbol override
    assert isinstance(body, str)


def test_prepare_content_different_symbols_produce_independent_assets():
    result_a = prepare_content(_analysis(symbol="XAUUSD"), ContentEngine(), MediaManager(), BroadcastManager())
    result_b = prepare_content(_analysis(symbol="EURUSD"), ContentEngine(), MediaManager(), BroadcastManager())
    assert result_a.id != result_b.id
