"""
Phase 59.3, TASK 6 -- context/fundamental_context.py tests.
"""

from datetime import datetime, timezone

from context.fundamental_context import (
    FundamentalContextSnapshot,
    compute_fundamental_context,
    generate_fundamental_snapshot_id,
)
from data.providers.fundamental_base import FundamentalDataPoint


def _point(series_id, value):
    return FundamentalDataPoint(
        series_id=series_id, value=value, unit="percent",
        as_of=datetime(2026, 1, 1, tzinfo=timezone.utc), source="fred",
    )


def test_no_inputs_produces_all_none_snapshot_never_raises():
    snapshot = compute_fundamental_context()

    assert isinstance(snapshot, FundamentalContextSnapshot)
    assert snapshot.fed_rate is None
    assert snapshot.inflation is None
    assert snapshot.dollar_strength is None
    assert snapshot.risk_level is None


def test_interest_rate_value_is_relayed_directly():
    snapshot = compute_fundamental_context(interest_rate=_point("FEDFUNDS", 5.25))
    assert snapshot.fed_rate == 5.25


def test_inflation_value_is_relayed_directly():
    snapshot = compute_fundamental_context(inflation=_point("CPIAUCSL", 310.3))
    assert snapshot.inflation == 310.3


def test_both_inputs_supplied():
    snapshot = compute_fundamental_context(
        interest_rate=_point("FEDFUNDS", 5.0), inflation=_point("CPIAUCSL", 300.0)
    )
    assert snapshot.fed_rate == 5.0
    assert snapshot.inflation == 300.0


def test_dollar_strength_and_risk_level_are_always_none_honest_hooks():
    """No fabricated classification -- see the module's own docstring on why."""
    snapshot = compute_fundamental_context(interest_rate=_point("FEDFUNDS", 5.25))
    assert snapshot.dollar_strength is None
    assert snapshot.risk_level is None


def test_snapshot_id_is_unique_per_call():
    a = compute_fundamental_context()
    b = compute_fundamental_context()
    assert a.snapshot_id != b.snapshot_id


def test_to_dict_is_json_safe():
    import json

    snapshot = compute_fundamental_context(interest_rate=_point("FEDFUNDS", 5.25))
    data = snapshot.to_dict()
    json.dumps(data)  # must not raise
    assert data["fed_rate"] == 5.25


def test_generate_fundamental_snapshot_id_returns_uuid_shaped_string():
    value = generate_fundamental_snapshot_id()
    assert isinstance(value, str)
    assert len(value) == 36


def test_snapshot_is_frozen():
    snapshot = compute_fundamental_context()
    try:
        snapshot.fed_rate = 999.0
        assert False, "FundamentalContextSnapshot must be immutable"
    except AttributeError:
        pass


def test_never_generates_a_signal_or_decision():
    """Structural guard matching the task's own boundary: no signal/decision-shaped attribute anywhere on the module."""
    import context.fundamental_context as module

    forbidden_terms = ("signal", "decision", "approve", "reject")
    public_names = [name for name in dir(module) if not name.startswith("_")]
    for name in public_names:
        assert not any(term in name.lower() for term in forbidden_terms), name
