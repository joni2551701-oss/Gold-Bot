"""
market/ facade — invalid / malformed input tolerance (TASK-CORE-005).

Proves the read-only façade degrades gracefully on odd inputs
(unexpected types, partial groups, malformed order-book rows) rather
than raising -- the same structured-absence posture as stream/ and
context/. A projection never trusts its input to be well-formed.
"""

from types import SimpleNamespace

from market.market_manager import MarketManager
from market.orderbook import OrderBook
from market.trend_state import TrendState
from market.volatility_state import VolatilityLevel


def test_schema_with_wrong_typed_groups_does_not_raise():
    # structure/liquidity are ints, regime is a number -- all nonsense.
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15",
                             structure=123, liquidity=456, zones=None,
                             session="oops", regime=999)
    data = MarketManager().build_market_data(schema)
    assert data.symbol == "XAUUSD"
    # Non-string regime -> normalised to a token, volatility falls to UNKNOWN.
    assert data.volatility is VolatilityLevel.UNKNOWN
    assert data.trend is TrendState.UNKNOWN


def test_orderbook_from_malformed_rows_skips_bad_and_keeps_good():
    ob = OrderBook.from_levels(
        "XAUUSD",
        bids=[(2000.0, 1.0), ("bad", "row"), (1999.0,), None, (1998.0, 2.5)],
        asks=[],
    )
    # Only the two well-formed bid rows survive; asks empty.
    assert len(ob.bids) == 2
    assert ob.best_bid.price == 2000.0
    assert ob.asks == []
    assert ob.best_ask is None


def test_empty_orderbook_is_empty_not_error():
    ob = OrderBook.from_levels("XAUUSD", bids=None, asks=None)
    assert ob.is_empty is True


def test_build_snapshot_on_odd_schema_still_serialises():
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15", regime=None,
                             structure=None, liquidity=None, zones=None, session=None)
    snap = MarketManager().build_snapshot(schema)
    d = snap.to_dict()
    assert d["symbol"] == "XAUUSD"
    assert d["regime"] == "UNKNOWN"
