"""STEP-08: validator, quality, enricher, formatter, serializer (TASK-CORE-008)."""

from datetime import datetime, timezone

from signal_layer.signal_builder.schema import SignalSchema
from signal_layer.signal_validator import validator as V
from signal_layer.signal_scoring import quality as Q
from signal_layer.signal_builder import enricher as E
from signal_layer.signal_formatter import formatter as F
from signal_layer.signal_formatter import serializer as S


def _sig(direction="BUY", entry=100.0, sl=98.0, tp=104.0, strategy="BOS"):
    return SignalSchema(
        signal_id="id-1", created_at=datetime.now(timezone.utc),
        symbol="XAUUSD", timeframe="M15", direction=direction,
        entry_price=entry, stop_loss=sl, take_profit=tp, strategy_name=strategy,
    )


# ---- validator ----------------------------------------------------------

def test_validator_reuses_schema_validation():
    assert V.validate(_sig()).valid
    assert not V.validate(_sig(sl=105.0)).valid


def test_deduplicator():
    d = V.SignalDeduplicator()
    s = _sig()
    assert not d.is_duplicate(s)
    d.register(s)
    assert d.is_duplicate(_sig())  # same identity key
    d.reset()
    assert not d.is_duplicate(s)


def test_precheck_source():
    ok = V.precheck_source(direction="BUY", entry=100.0, strategy="BOS", confidence=0.8, rr=2.0)
    assert ok.valid
    bad = V.precheck_source(direction=None, entry=None, strategy=None, confidence=5.0, rr=None)
    assert not bad.valid and len(bad.errors) == 5


# ---- quality ------------------------------------------------------------

def test_quality_bands():
    assert Q.assess(0.9, 2.0) is Q.SignalStrength.STRONG
    assert Q.assess(0.65, 2.0) is Q.SignalStrength.GOOD
    assert Q.assess(0.45, 2.0) is Q.SignalStrength.NORMAL
    assert Q.assess(0.1, 2.0) is Q.SignalStrength.WEAK
    assert Q.assess(0.0, 2.0) is Q.SignalStrength.INVALID
    assert Q.assess(0.9, None, has_setup=False) is Q.SignalStrength.INVALID


def test_quality_rr_cap_and_grade_map():
    # rr < 1 steps the label down one level
    assert Q.assess(0.9, 0.5) is Q.SignalStrength.GOOD
    assert Q.map_grade("A+") is Q.SignalStrength.STRONG
    assert Q.map_grade(None) is Q.SignalStrength.INVALID


# ---- enricher -----------------------------------------------------------

def test_enricher_fills_optional_fields_without_mutating():
    s = _sig()
    out, enr = E.enrich(s, session="LONDON", current_price=100.5, regime="TREND")
    assert s.session is None  # original untouched (frozen)
    assert out.session == "LONDON"
    assert enr.current_price == 100.5 and enr.regime == "TREND"
    assert enr.build_version == E.BUILD_VERSION
    assert isinstance(enr.to_dict()["enriched_at"], str)


def test_enricher_does_not_overwrite_existing():
    s = _sig()
    s2 = SignalSchema(**{**s.__dict__, "session": "NEW_YORK"})
    out, _ = E.enrich(s2, session="LONDON")
    assert out.session == "NEW_YORK"  # already set -> not overwritten


# ---- formatter ----------------------------------------------------------

def test_formatter_is_platform_neutral():
    p = F.format_signal(_sig(), strength=Q.SignalStrength.STRONG, reasons=["BOS up"])
    assert p.title == "XAUUSD BUY"
    assert "STRONG" in p.summary
    assert p.short_reason == "BOS up"
    assert "XAUUSD" in p.tags
    # no HTML anywhere
    assert "<" not in (p.title + p.summary + p.description)


# ---- serializer ---------------------------------------------------------

def test_serializer_reuses_schema_and_folds_views():
    s = _sig()
    assert S.to_dict(s) == s.to_dict()
    payload = S.serialize_payload(
        s, strength=Q.SignalStrength.GOOD,
        presentation=F.format_signal(s), routes=["DECISION"], lifecycle="READY",
    )
    assert payload["signal"]["symbol"] == "XAUUSD"
    assert payload["strength"] == "GOOD"
    assert payload["routes"] == ["DECISION"]
    assert payload["lifecycle"] == "READY"
    # JSON-serializable
    import json
    json.loads(S.payload_to_json(payload))
