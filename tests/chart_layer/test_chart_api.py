"""FLOW-016 Chart Service Foundation -- Chart_API integration tests
(events + service + api).
"""

from chart_layer.chart_api import (
    ChartAPI,
    ChartEvent,
    ChartEventRecorder,
    ChartService,
    chart_created,
    chart_failed,
    chart_requested,
    chart_updated,
)
from chart_layer.chart_data import ChartStatus, ChartRequest


def _req():
    return ChartRequest(asset="XAUUSD", timeframe="M15")


# --- events ---------------------------------------------------------------
def test_event_factories_and_recorder():
    assert chart_requested("h").name == "ChartRequested"
    assert chart_created("h").name == "ChartCreated"
    assert chart_updated("h").name == "ChartUpdated"
    assert chart_failed("h", reason="x").name == "ChartFailed"
    rec = ChartEventRecorder()
    rec.emit(chart_requested("h"))
    rec.emit(chart_created("h"))
    assert [e.name for e in rec.events] == ["ChartRequested", "ChartCreated"]
    assert len(rec) == 2
    assert isinstance(rec.last(), ChartEvent)
    rec.clear()
    assert len(rec) == 0 and rec.last() is None


def test_recorder_events_is_a_copy():
    rec = ChartEventRecorder()
    rec.emit(chart_requested("h"))
    rec.events.clear()
    assert len(rec) == 1


# --- service --------------------------------------------------------------
def test_service_create_emits_and_caches():
    svc = ChartService()
    resp = svc.create_chart(_req())
    assert resp.status is ChartStatus.PLACEHOLDER
    assert [e.name for e in svc.events.events] == ["ChartRequested", "ChartCreated"]
    assert len(svc.cache) == 1


def test_service_cache_hit_does_not_recreate():
    svc = ChartService()
    svc.create_chart(_req())
    svc.create_chart(_req())
    assert [e.name for e in svc.events.events].count("ChartCreated") == 1


def test_service_get_uses_cache_when_present():
    svc = ChartService()
    svc.create_chart(_req())
    before = len(svc.events.events)
    svc.get_chart(_req())
    assert len(svc.events.events) == before


def test_service_update_invalidates_and_recreates():
    svc = ChartService()
    svc.create_chart(_req())
    svc.update_chart(_req())
    names = [e.name for e in svc.events.events]
    assert "ChartUpdated" in names
    assert names.count("ChartCreated") == 2


def test_service_invalid_request_failed():
    svc = ChartService()
    resp = svc.create_chart(ChartRequest(asset="", timeframe="M15"))
    assert resp.status is ChartStatus.FAILED
    assert svc.events.last().name == "ChartFailed"


def test_service_no_cache_mode():
    svc = ChartService()
    svc.create_chart(_req(), use_cache=False)
    assert len(svc.cache) == 0


# --- api E2E --------------------------------------------------------------
def test_api_e2e_create_get_update_clear():
    api = ChartAPI()
    created = api.create_chart(_req())
    assert created.ok is True
    ref = created.chart_reference
    assert ref == _req().request_hash()
    assert api.get_chart(_req()).chart_reference == ref
    assert api.update_chart(_req()).ok is True
    api.clear_cache()
    assert api.get_chart(_req()).ok is True


def test_api_invalid_is_failed_not_exception():
    resp = ChartAPI().create_chart(ChartRequest(asset="", timeframe="M15"))
    assert resp.status is ChartStatus.FAILED


def test_all_five_canonical_subpackages_importable():
    import importlib

    for mod in [
        "chart_layer.chart_data",
        "chart_layer.chart_renderer",
        "chart_layer.chart_core",
        "chart_layer.chart_api",
    ]:
        assert importlib.import_module(mod) is not None
