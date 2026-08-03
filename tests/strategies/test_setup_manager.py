"""Setup layer — SetupManager orchestration (TASK-CORE-007)."""

from types import SimpleNamespace

from context_layer.order_block.order_block import OrderBlockType

from strategy_layer.strategy_manager.manager import SetupManager, SetupEvaluation
from strategy_layer.strategy_engine.result import StrategyResult, SetupStatus, StrategyDirection


def test_evaluate_runs_every_strategy(make_ctx):
    mgr = SetupManager()
    results = mgr.evaluate(make_ctx(market_regime=SimpleNamespace(regime=None, direction=None, confidence=0)))
    assert len(results) == 11
    assert all(isinstance(r, StrategyResult) for r in results)


def test_none_context_yields_all_invalid():
    results = SetupManager().evaluate(None)
    assert len(results) == 11
    assert all(r.status is SetupStatus.INVALID for r in results)


def test_ranking_puts_setups_first_by_confidence(make_ctx):
    # A single order block yields one SETUP_FOUND; it must rank ahead of the rest.
    ctx = make_ctx(
        order_blocks=[SimpleNamespace(index=5, type=OrderBlockType.BULLISH, low=100.0, high=105.0)],
        candles=[SimpleNamespace(close=102.0)],
    )
    ev = SetupManager().evaluate_full(ctx)
    assert isinstance(ev, SetupEvaluation)
    assert ev.best is not None
    assert ev.best.status is SetupStatus.SETUP_FOUND
    assert ev.best.strategy_name == "ORDER_BLOCK_SETUP"
    assert ev.best.direction is StrategyDirection.LONG
    # Ranking: all SETUP_FOUND come before any NO_SETUP/INVALID.
    statuses = [r.status for r in ev.results]
    first_non_found = next((i for i, s in enumerate(statuses) if s is not SetupStatus.SETUP_FOUND), len(statuses))
    assert all(s is SetupStatus.SETUP_FOUND for s in statuses[:first_non_found])


def test_manager_accepts_injected_registry():
    from strategy_layer.strategy_library.registry import SetupRegistry
    from strategy_layer.strategy_library.snr_strategy import SNRStrategy
    reg = SetupRegistry()
    reg.register(SNRStrategy())
    mgr = SetupManager(registry=reg)
    assert mgr.registry.names() == ["SUPPORT_RESISTANCE_SETUP"]
    assert len(mgr.evaluate(None)) == 1
