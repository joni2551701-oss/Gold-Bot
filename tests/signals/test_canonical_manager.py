"""STEP-08: SignalManager orchestration + empty/invalid/duplicate/serialization (TASK-CORE-008)."""

import json

from signals.manager import SignalManager, CanonicalSignalResult
from signals.quality import SignalStrength
from signals.lifecycle.state import CanonicalSignalStatus
from signals.router import SignalConsumer


def test_full_long_setup_builds_ready_signal(make_strategy_result):
    m = SignalManager()
    r = m.build(make_strategy_result(), symbol="XAUUSD", timeframe="M15", session="LONDON")
    assert isinstance(r, CanonicalSignalResult)
    assert r.is_valid
    assert r.signal.direction == "BUY"
    assert r.signal.entry_price == 100.5      # midpoint of (100,101)
    assert r.signal.stop_loss == 98.0
    assert r.signal.take_profit == 105.5      # entry + rr*risk = 100.5 + 2*2.5
    assert r.strength is SignalStrength.STRONG
    assert r.status is CanonicalSignalStatus.READY
    assert SignalConsumer.TELEGRAM.value in r.routes
    assert r.presentation is not None and r.enrichment is not None


def test_short_setup_direction_and_target(make_strategy_result):
    m = SignalManager()
    r = m.build(make_strategy_result(direction="SHORT", entry_zone=(100.0, 101.0), invalidation=103.0, rr=1.5))
    assert r.signal.direction == "SELL"
    # entry 100.5, risk 2.5, tp = 100.5 - 1.5*2.5 = 96.75
    assert r.signal.take_profit == 96.75
    assert r.is_valid


def test_empty_strategy_result_is_invalid(make_strategy_result):
    from types import SimpleNamespace
    m = SignalManager()
    r = m.build(SimpleNamespace())
    assert not r.is_valid
    assert r.strength is SignalStrength.INVALID
    assert r.status is CanonicalSignalStatus.CREATED
    assert r.routes == []


def test_no_setup_status_is_invalid(make_strategy_result):
    m = SignalManager()
    r = m.build(make_strategy_result(status="NO_SETUP"))
    assert not r.is_valid
    assert any("no setup" in e for e in r.validation.errors)


def test_missing_rr_is_invalid(make_strategy_result):
    m = SignalManager()
    r = m.build(make_strategy_result(rr=None))
    assert not r.is_valid
    assert any("rr" in e for e in r.validation.errors)


def test_duplicate_signal_detected(make_strategy_result):
    m = SignalManager()
    first = m.build(make_strategy_result())
    second = m.build(make_strategy_result())
    assert first.is_valid
    assert second.is_duplicate
    assert not second.is_valid


def test_serialization_payload_is_json(make_strategy_result):
    m = SignalManager()
    r = m.build(make_strategy_result())
    payload = m.serialize(r)
    assert payload["signal"]["direction"] == "BUY"
    assert payload["strength"] == "STRONG"
    assert payload["lifecycle"] == "READY"
    json.loads(json.dumps(payload))  # round-trips


def test_manager_never_raises_on_garbage():
    m = SignalManager()
    for bad in (object(), None):
        r = m.build(bad)
        assert not r.is_valid
