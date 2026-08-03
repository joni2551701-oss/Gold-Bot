"""STEP-09 decision layer: status/model/rules/router/manager (TASK-CORE-009)."""

from datetime import datetime, timezone, timedelta
from types import SimpleNamespace

from signal_layer.signal_builder.schema import SignalSchema, generate_signal_id
from decision_layer.decision_engine.decision_status import (
    DecisionStatus, from_decision_action, from_signal_decision,
)
from decision_layer.decision_engine.models import DecisionAction
from decision_layer.decision_engine.decision_model import DecisionOutcome
from decision_layer.decision_service.decision_router import DecisionConsumer, route
from decision_layer.decision_service.decision_manager import DecisionManager


def _sig(direction="BUY", entry=100.0, sl=98.0, tp=104.0, conf=0.8,
         decision="APPROVED", age_s=0):
    return SignalSchema(
        signal_id=generate_signal_id(),
        created_at=datetime.now(timezone.utc) - timedelta(seconds=age_s),
        symbol="XAUUSD", timeframe="M15", direction=direction,
        entry_price=entry, stop_loss=sl, take_profit=tp,
        confidence_score=conf, decision=decision,
    )


# ---- status vocabulary + reuse mapping ----------------------------------

def test_status_values():
    assert {s.value for s in DecisionStatus} == {"APPROVE", "REJECT", "HOLD", "EXPIRE"}


def test_reuse_frozen_action_mapping():
    # The reuse point: NO_TRADE -> HOLD, APPROVE/REJECT pass through.
    assert from_decision_action(DecisionAction.APPROVE) is DecisionStatus.APPROVE
    assert from_decision_action(DecisionAction.REJECT) is DecisionStatus.REJECT
    assert from_decision_action(DecisionAction.NO_TRADE) is DecisionStatus.HOLD
    assert from_decision_action(SimpleNamespace(value="NO_TRADE")) is DecisionStatus.HOLD
    assert from_decision_action(None) is DecisionStatus.HOLD


def test_signal_decision_mapping():
    assert from_signal_decision("APPROVED") is DecisionStatus.APPROVE
    assert from_signal_decision("REJECTED") is DecisionStatus.REJECT
    assert from_signal_decision("PENDING") is DecisionStatus.HOLD
    assert from_signal_decision(None) is DecisionStatus.HOLD


# ---- manager pipeline ---------------------------------------------------

def test_approve_passthrough():
    r = DecisionManager().decide(_sig())
    assert isinstance(r, DecisionOutcome)
    assert r.status is DecisionStatus.APPROVE and r.is_approved


def test_reject_and_pending():
    assert DecisionManager().decide(_sig(decision="REJECTED")).status is DecisionStatus.REJECT
    assert DecisionManager().decide(_sig(decision="PENDING")).status is DecisionStatus.HOLD


def test_low_confidence_holds_an_approve():
    r = DecisionManager().decide(_sig(conf=0.3))
    assert r.status is DecisionStatus.HOLD
    assert "hold_low_confidence" in r.rules_applied


def test_stale_signal_expires():
    r = DecisionManager().decide(_sig(age_s=1200))
    assert r.status is DecisionStatus.EXPIRE
    assert "expire_stale" in r.rules_applied


def test_invalid_signal_rejected():
    r = DecisionManager().decide(_sig(direction="NONE", entry=None, sl=None, tp=None))
    assert r.status is DecisionStatus.REJECT
    assert "reject_invalid" in r.rules_applied


def test_reuse_trade_decision_no_trade_becomes_hold():
    td = SimpleNamespace(action=DecisionAction.NO_TRADE)
    r = DecisionManager().decide(_sig(decision="PENDING"), trade_decision=td)
    assert r.status is DecisionStatus.HOLD
    assert r.metadata["base_status"] == "HOLD"
    assert r.metadata["source"] == "trade_decision"


def test_none_signal_never_raises():
    r = DecisionManager().decide(None)
    assert r.status is DecisionStatus.REJECT


def test_serialization_roundtrip():
    import json
    d = DecisionManager().decide(_sig()).to_dict()
    assert d["status"] == "APPROVE"
    json.loads(DecisionManager().decide(_sig()).to_json())


# ---- router -------------------------------------------------------------

def test_router_only_approve_reaches_risk():
    approve = DecisionManager().decide(_sig())
    hold = DecisionManager().decide(_sig(decision="PENDING"))
    assert DecisionConsumer.RISK in route(approve)
    assert DecisionConsumer.RISK not in route(hold)
    # observers always present
    for outcome in (approve, hold):
        for c in (DecisionConsumer.DATABASE, DecisionConsumer.AI, DecisionConsumer.MONITORING):
            assert c in route(outcome)
