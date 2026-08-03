"""
market/ facade — MarketStructureView projection (TASK-CORE-005).

Proves market_structure.py is a PROJECTION of context's already-computed
structure/zones, never a second detector: it copies context's own
trend/bos/choch/swing_state/order_block/fvg through unchanged and
invents nothing when they are absent.
"""

from types import SimpleNamespace

from data_layer.live_data.market.market_structure import MarketStructureView


def test_projects_context_structure_and_zones_verbatim():
    schema = SimpleNamespace(
        structure=SimpleNamespace(trend="BEARISH", bos=True, choch=True, swing_state="LL"),
        zones=SimpleNamespace(order_block=True, fvg=True),
    )
    view = MarketStructureView.from_context(schema)
    assert view.trend == "BEARISH"
    assert view.bos is True
    assert view.choch is True
    assert view.swing_state == "LL"
    assert view.order_block is True
    assert view.fvg is True


def test_empty_context_yields_empty_view():
    view = MarketStructureView.from_context(SimpleNamespace())
    assert view.trend is None
    assert view.bos is False
    assert view.choch is False
    assert view.swing_state is None
    assert view.order_block is False
    assert view.fvg is False


def test_none_groups_do_not_raise():
    schema = SimpleNamespace(structure=None, zones=None)
    view = MarketStructureView.from_context(schema)
    assert view == MarketStructureView()


def test_view_is_frozen():
    view = MarketStructureView.from_context(SimpleNamespace())
    try:
        view.trend = "BULLISH"  # type: ignore[misc]
    except Exception as exc:  # FrozenInstanceError
        assert "frozen" in type(exc).__name__.lower() or "cannot assign" in str(exc).lower()
    else:
        raise AssertionError("MarketStructureView must be immutable")
