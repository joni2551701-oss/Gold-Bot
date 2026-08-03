from ai.access.permissions import AIRole
from ai.chart_intelligence.models import ChartAnalysis, ChartAnalysisType, ChartImageType
from ai.trade_journal.journal_runtime import TradeJournalRuntime
from ai.trade_journal.trading_analyst_adapter import journal_entry_from_trading_and_chart
from ai.trading_analyst.models import TradingAnalysis, TradingRiskLevel
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_trade_journal=True)
DISABLED = FeatureFlags(enable_trade_journal=False)


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
        confidence=0.8, notes="clean setup", chart_id="chart_xyz",
    )
    defaults.update(overrides)
    return ChartAnalysis(**defaults)


def test_journal_entry_from_trading_and_chart_owner_succeeds():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(), _chart(), "trade_1", runtime, AIRole.OWNER)
    assert result is not None
    assert result.chart_id == "chart_xyz"
    assert result.trade_id == "trade_1"


def test_journal_entry_from_trading_and_chart_relays_symbol_and_timeframe():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(
        _trading(symbol="EURUSD"), _chart(symbol="EURUSD", timeframe="D1"), "trade_1", runtime, AIRole.OWNER,
    )
    assert result.symbol == "EURUSD"
    assert result.timeframe == "D1"


def test_journal_entry_from_trading_and_chart_relays_direction():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(direction="SELL"), _chart(), "trade_1", runtime, AIRole.OWNER)
    assert result.direction == "SELL"


def test_journal_entry_from_trading_and_chart_relays_confidence():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(confidence=0.55), _chart(), "trade_1", runtime, AIRole.OWNER)
    assert result.confidence == 0.55


def test_journal_entry_from_trading_and_chart_uses_recommendation_as_reason():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(
        _trading(recommendation="WHY BUY: strong setup"), _chart(), "trade_1", runtime, AIRole.OWNER,
    )
    assert result.reason == "WHY BUY: strong setup"


def test_journal_entry_from_trading_and_chart_falls_back_to_summary_without_recommendation():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(
        _trading(recommendation="", summary="fallback summary"), _chart(), "trade_1", runtime, AIRole.OWNER,
    )
    assert result.reason == "fallback summary"


def test_journal_entry_from_trading_and_chart_uses_chart_notes_as_lesson():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(), _chart(notes="watch for retest"), "trade_1", runtime, AIRole.OWNER)
    assert result.lesson == "watch for retest"


def test_journal_entry_from_trading_and_chart_accepts_optional_price_levels():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(
        _trading(), _chart(), "trade_1", runtime, AIRole.OWNER,
        entry=3400.0, sl=3390.0, tp=3420.0, result="WIN",
    )
    assert result.entry == 3400.0
    assert result.sl == 3390.0
    assert result.tp == 3420.0
    assert result.result == "WIN"


def test_journal_entry_from_trading_and_chart_never_fabricates_price_levels():
    """Neither TradingAnalysis nor ChartAnalysis carries entry/sl/tp -- unset unless explicitly passed."""
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(), _chart(), "trade_1", runtime, AIRole.OWNER)
    assert result.entry is None
    assert result.sl is None
    assert result.tp is None


def test_journal_entry_from_trading_and_chart_admin_blocked():
    runtime = TradeJournalRuntime(flags=ENABLED)
    result = journal_entry_from_trading_and_chart(_trading(), _chart(), "trade_1", runtime, AIRole.ADMIN)
    assert result is None


def test_journal_entry_from_trading_and_chart_blocked_when_flag_disabled():
    runtime = TradeJournalRuntime(flags=DISABLED)
    result = journal_entry_from_trading_and_chart(_trading(), _chart(), "trade_1", runtime, AIRole.OWNER)
    assert result is None


def test_journal_entry_from_trading_and_chart_never_produces_new_verdict():
    """Rule 2: the composed journal entry never invents a different direction than trading.direction."""
    runtime = TradeJournalRuntime(flags=ENABLED)
    for direction in ("BUY", "SELL", "WAIT", "SKIP"):
        result = journal_entry_from_trading_and_chart(_trading(direction=direction), _chart(), "trade_1", runtime, AIRole.OWNER)
        assert result.direction == direction
