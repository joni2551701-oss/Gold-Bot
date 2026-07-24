"""
Phase 17.2.1 — Signal Layer Import & Instantiation tests.

Phase 52 audit finding: this file predates pytest-style test functions
(it originally defined a standalone run_test() function, invoked only
via `if __name__ == "__main__":`) -- pytest's default collection only
picks up functions named test_*, so it silently contributed ZERO
tests to the suite despite matching the test_*.py filename pattern.
Rewritten here as real pytest tests with the same scope and coverage.

Scope (per Director specification):
- Verify import chain (no ModuleNotFoundError / ImportError)
- Verify class instantiation (constructors execute without error)
- Verify dependency wiring (SignalEngine -> StrategyManager -> strategies)

Explicitly OUT of scope for this phase:
- generate_signals() execution (see test_generate_signals.py)
- Strategy logic / signal quality
- TwelveData, Gemini, Telegram, MT5 -- none of these are touched.
"""


def test_signal_layer_imports_cleanly():
    from signals.signal_engine import SignalEngine
    from strategies.strategy_manager import StrategyManager
    from strategies.liquidity_strategy import LiquidityStrategy
    from strategies.fvg_strategy import FVGStrategy
    from strategies.amd_strategy import AMDStrategy

    # Referencing every imported name is the actual assertion here --
    # a successful, non-empty import chain with no ModuleNotFoundError.
    for cls in (SignalEngine, StrategyManager, LiquidityStrategy, FVGStrategy, AMDStrategy):
        assert isinstance(cls, type)


def test_individual_strategies_instantiate():
    from strategies.liquidity_strategy import LiquidityStrategy
    from strategies.fvg_strategy import FVGStrategy
    from strategies.amd_strategy import AMDStrategy

    assert LiquidityStrategy() is not None
    assert FVGStrategy() is not None
    assert AMDStrategy() is not None


def test_signal_engine_wires_strategy_manager_with_all_three_strategies():
    from signals.signal_engine import SignalEngine
    from strategies.strategy_manager import StrategyManager
    from strategies.liquidity_strategy import LiquidityStrategy
    from strategies.fvg_strategy import FVGStrategy
    from strategies.amd_strategy import AMDStrategy

    engine = SignalEngine()

    assert isinstance(engine.strategy_manager, StrategyManager)

    expected_types = {LiquidityStrategy, FVGStrategy, AMDStrategy}
    actual_types = {type(s) for s in engine.strategy_manager.strategies}
    assert actual_types == expected_types
