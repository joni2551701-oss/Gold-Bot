"""
Setup layer — base contract + empty/invalid context (TASK-CORE-007).

Every SetupStrategy must implement name()/evaluate()/validate()/score(),
always return a StrategyResult (never raise), and give a defined result
for empty and invalid contexts.
"""

from strategies.registry import DEFAULT_SETUP_STRATEGIES
from strategies.base import SetupStrategy
from strategies.result import StrategyResult, SetupStatus


def _all():
    return [cls() for cls in DEFAULT_SETUP_STRATEGIES]


def test_every_strategy_implements_the_contract():
    for s in _all():
        assert isinstance(s, SetupStrategy)
        assert isinstance(s.name(), str) and s.name()
        for method in ("evaluate", "validate", "score"):
            assert callable(getattr(s, method))


def test_none_context_is_invalid_not_a_raise():
    for s in _all():
        res = s.evaluate(None)
        assert isinstance(res, StrategyResult)
        assert res.status is SetupStatus.INVALID
        assert res.strategy_name == s.name()
        assert s.validate(None) is False
        assert s.score(None) == 0.0


def test_empty_context_is_no_setup(make_ctx):
    ctx = make_ctx()  # all fields empty, regime None
    for s in _all():
        res = s.evaluate(ctx)
        assert isinstance(res, StrategyResult)
        # Empty context carries no usable data -> INVALID by the base guard.
        assert res.status in (SetupStatus.NO_SETUP, SetupStatus.INVALID)
        assert not res.has_setup


def test_invalid_context_shapes_do_not_raise(make_ctx):
    # Malformed contexts: an attribute-less object, and one with all-None
    # fields plus a bogus regime. Strategies must still return a result.
    for ctx in (object(), make_ctx(structure=None, bos_events=None, order_blocks=None,
                                   liquidity_zones=None, market_regime="not-a-regime")):
        for s in _all():
            res = s.evaluate(ctx)
            assert isinstance(res, StrategyResult)


def test_names_are_unique():
    names = [cls().name() for cls in DEFAULT_SETUP_STRATEGIES]
    assert len(names) == len(set(names)) == 11
