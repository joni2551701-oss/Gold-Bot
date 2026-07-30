"""Setup layer — Session strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from strategies.session_strategy import SessionStrategy
from strategies.result import StrategyDirection, SetupStatus


def _session(name):
    return SimpleNamespace(session=SimpleNamespace(value=name))


def test_killzone_without_structure_is_neutral(make_ctx):
    ctx = make_ctx(session_events=[_session("LONDON")])
    r = SessionStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.NEUTRAL
    assert r.confidence == 0.5


def test_killzone_with_structural_confluence_gets_direction(make_ctx):
    ctx = make_ctx(
        session_events=[_session("NEW_YORK")],
        bos_events=[SimpleNamespace(index=5, direction=SimpleNamespace(value="BULLISH"))],
    )
    r = SessionStrategy().evaluate(ctx)
    assert r.direction is StrategyDirection.LONG
    assert r.confidence == 0.65


def test_off_session_is_no_setup(make_ctx):
    r = SessionStrategy().evaluate(make_ctx(session_events=[_session("ASIA")]))
    assert r.status is SetupStatus.NO_SETUP
