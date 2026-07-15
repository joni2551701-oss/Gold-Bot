"""
Phase 60.2, TASK 3 -- backtesting/backtest_engine.py tests. Real
repositories (SQLite, tests/conftest.py's autouse fresh_database
fixture) and the real DecisionEngine/RiskManager -- only
SignalEngine.generate_signals()/AIAnalyzer.analyze() are stubbed
(same monkeypatch convention tests/conftest.py's own mock_pipeline
fixture already established for the live pipeline), so these tests
prove the real Decision/Risk/PaperTrade/Analytics chain runs
end-to-end without needing a real strategy pattern to trigger in the
seeded candle data.
"""

from datetime import datetime, timezone

from backtesting.backtest_engine import BacktestEngine
from backtesting.replay_models import ReplayConfig
from database.raw_candle_models import create_raw_candle
from database.raw_candle_repository import RawCandleRepository


def _seed_candles(n=250, symbol="XAUUSD", timeframe="M15"):
    """Distinct, monotonically increasing timestamps (15-minute spacing, matching M15)."""
    from datetime import timedelta
    repo = RawCandleRepository()
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for i in range(n):
        repo.save_candle(create_raw_candle(
            symbol=symbol, timeframe=timeframe,
            timestamp=base + timedelta(minutes=15 * i),
            open=2000.0, high=2005.0, low=1995.0, close=2001.0,
            provider="twelvedata",
        ))
    return repo, base + timedelta(minutes=15 * (n - 1))


def _config(end, **overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=end,
    )
    defaults.update(overrides)
    return ReplayConfig(**defaults)


def test_engine_processes_every_candle_with_no_signals():
    _, end = _seed_candles(250)
    engine = BacktestEngine(_config(end))

    result = engine.run()

    assert result.candles_processed == 250
    assert result.signals_generated == 0
    assert result.trades_opened == 0
    assert result.performances == []


def test_too_few_candles_produces_no_signals_but_does_not_crash():
    _, end = _seed_candles(5)
    engine = BacktestEngine(_config(end))

    result = engine.run()

    assert result.candles_processed == 5
    assert result.signals_generated == 0


def test_approved_candidate_opens_a_paper_trade(mock_signal_candidate, mock_ai_result):
    _, end = _seed_candles(250)
    engine = BacktestEngine(_config(end))

    candidate = mock_signal_candidate()
    call_count = {"n": 0}

    def _one_shot_signals(context):
        call_count["n"] += 1
        return [candidate] if call_count["n"] == 1 else []

    engine.signal_engine.generate_signals = _one_shot_signals
    engine.ai_analyzer.analyze = lambda c, ctx: mock_ai_result(approved=True, confidence=0.95, risk_score=0.05)

    result = engine.run()

    assert result.signals_generated == 1
    assert result.trades_opened == 1
    assert len(result.performances) == 1
    assert result.performances[0].strategy_id == candidate.strategy_name


def test_approved_candidates_paper_trade_actually_resolves(mock_signal_candidate, mock_ai_result):
    """
    Phase 60.7 TASK 1 regression: _process_candidate() previously
    discarded open_paper_trade()/check_paper_trade_against_candles()'s
    returned trade, so paper_trade stayed at TradeState.CREATED
    forever and every SignalPerformance.result was silently None. The
    fixture's default entry (4065.0) is far outside the seeded
    candles' 1995-2005 range, so entry is never touched -- the trade
    must resolve to EXPIRED, proving the transition is now captured.
    """
    _, end = _seed_candles(250)
    engine = BacktestEngine(_config(end))

    candidate = mock_signal_candidate()
    call_count = {"n": 0}

    def _one_shot_signals(context):
        call_count["n"] += 1
        return [candidate] if call_count["n"] == 1 else []

    engine.signal_engine.generate_signals = _one_shot_signals
    engine.ai_analyzer.analyze = lambda c, ctx: mock_ai_result(approved=True, confidence=0.95, risk_score=0.05)

    result = engine.run()

    assert result.trades_opened == 1
    assert result.performances[0].result == "EXPIRED"


def test_rejected_candidate_does_not_open_a_trade_but_is_still_tracked(mock_signal_candidate, mock_ai_result):
    _, end = _seed_candles(250)
    engine = BacktestEngine(_config(end))

    candidate = mock_signal_candidate()
    call_count = {"n": 0}

    def _one_shot_signals(context):
        call_count["n"] += 1
        return [candidate] if call_count["n"] == 1 else []

    engine.signal_engine.generate_signals = _one_shot_signals
    engine.ai_analyzer.analyze = lambda c, ctx: mock_ai_result(approved=False)

    result = engine.run()

    assert result.signals_generated == 1
    assert result.trades_opened == 0
    assert len(result.performances) == 1
    assert result.performances[0].result is None


def test_default_dependencies_are_the_real_classes():
    _, end = _seed_candles(30)
    engine = BacktestEngine(_config(end))

    from ai.ai_analyzer import AIAnalyzer
    from decision.decision_engine import DecisionEngine
    from risk.risk_manager import RiskManager

    assert isinstance(engine.ai_analyzer, AIAnalyzer)
    assert isinstance(engine.decision_engine, DecisionEngine)
    assert isinstance(engine.risk_manager, RiskManager)


def test_htf_bias_defaults_to_neutral_fallback():
    _, end = _seed_candles(30)
    engine = BacktestEngine(_config(end))

    from context.htf_bias import HTFBias
    result = engine.htf_bias_provider("XAUUSD")
    assert result.bias == HTFBias.UNKNOWN
