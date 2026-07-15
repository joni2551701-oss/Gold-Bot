"""
Phase 60.5: Fundamental Intelligence Foundation, TASK 4 --
context/economic_events.py tests.
"""

from datetime import datetime, timezone

from context.economic_events import EconomicEvent, EventImpact


def _event(expected=None, actual=None):
    return EconomicEvent(
        name="NFP", date=datetime(2026, 1, 2, tzinfo=timezone.utc),
        impact=EventImpact.HIGH, currency="USD", expected=expected, actual=actual,
    )


def test_construction_matches_the_briefs_own_fields():
    event = _event(expected=180.0, actual=210.0)

    assert event.name == "NFP"
    assert event.impact == EventImpact.HIGH
    assert event.currency == "USD"
    assert event.expected == 180.0
    assert event.actual == 210.0


def test_surprise_is_actual_minus_expected():
    event = _event(expected=180.0, actual=210.0)

    assert event.surprise == 30.0


def test_surprise_is_none_when_actual_not_reported_yet():
    event = _event(expected=180.0, actual=None)

    assert event.surprise is None


def test_surprise_is_none_when_expected_unknown():
    event = _event(expected=None, actual=210.0)

    assert event.surprise is None


def test_defaults_have_no_expected_or_actual():
    event = EconomicEvent(
        name="FOMC Statement", date=datetime(2026, 1, 2, tzinfo=timezone.utc),
        impact=EventImpact.HIGH, currency="USD",
    )

    assert event.expected is None
    assert event.actual is None
    assert event.surprise is None


def test_event_is_frozen():
    event = _event()
    try:
        event.actual = 999.0
        assert False, "EconomicEvent must be immutable"
    except AttributeError:
        pass


def test_to_dict_is_json_safe():
    import json

    event = _event(expected=180.0, actual=210.0)
    data = event.to_dict()

    json.dumps(data)  # must not raise
    assert data["impact"] == "HIGH"
    assert data["surprise"] == 30.0


def test_event_impact_has_three_standard_tiers():
    assert {i.value for i in EventImpact} == {"HIGH", "MEDIUM", "LOW"}
