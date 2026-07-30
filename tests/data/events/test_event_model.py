"""Unit tests for data/events/event_model.py (module 7)."""

from datetime import datetime

import pytest

from data.events.event_model import (
    Event, EventType, EVENT_SCHEMA_VERSION,
    validate_event, EventValidationError,
)
from _efakes import make_event, ts


def test_namespaces_amendment6():
    assert EventType.MARKET_CANDLE_OPENED.namespace == "MARKET"
    assert EventType.BOOTSTRAP_STARTED.namespace == "BOOTSTRAP"
    assert EventType.SYSTEM_READINESS_CHANGED.namespace == "SYSTEM"
    assert EventType.STREAM_CONNECTED.namespace == "STREAM"


def test_event_has_version_and_correlation():
    e = make_event(correlation_id="run-1")
    assert e.event_version == EVENT_SCHEMA_VERSION      # amendment 1
    assert e.correlation_id == "run-1"                  # amendment 2


def test_validation_accepts_good_event():
    validate_event(make_event())                        # no raise


def test_validation_rejects_missing_fields():
    with pytest.raises(EventValidationError):
        validate_event(Event(type=EventType.MARKET_CANDLE_CLOSED,
                             event_id="", timestamp=ts(0)))   # empty id
    with pytest.raises(EventValidationError):
        validate_event(Event(type=EventType.MARKET_CANDLE_CLOSED,
                             event_id="e1", timestamp=None))  # no timestamp
    with pytest.raises(EventValidationError):
        validate_event(Event(type=EventType.MARKET_CANDLE_CLOSED,
                             event_id="e1",
                             timestamp=datetime(2026, 7, 24)))  # naive tz


def test_validation_require_payload():
    e = Event(type=EventType.MARKET_CANDLE_CLOSED, payload=None,
              event_id="e1", timestamp=ts(0))
    validate_event(e, require_payload=False)            # ok
    with pytest.raises(EventValidationError):
        validate_event(e, require_payload=True)
