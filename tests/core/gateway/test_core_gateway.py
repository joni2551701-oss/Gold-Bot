"""Tests for the CoreGateway facade (module 10) -- end-to-end."""

import pytest

from core.gateway.gateway import CoreGateway
from core.gateway.service_manifest import ServiceKind
from core.gateway.service_state import ServiceState
from core.gateway.service_registry import ServiceNotFoundError
from core.gateway.dependency_graph import DependencyError
from core.gateway.gateway_request import GatewayStatus
from core.gateway.gateway_events import GatewayEventName

from _gfakes import FakeClock, manifest, echo_handler, request


def _gateway(sink=None):
    return CoreGateway(clock=FakeClock(), event_sink=sink)


def test_register_start_dispatch():
    gw = _gateway()
    gw.register_service(manifest("MarketMemory", capabilities=("MarketMemory",)),
                        echo_handler)
    gw.register_service(manifest("Replay", capabilities=("Replay",),
                                 dependencies=("MarketMemory",)), echo_handler)
    order = gw.start()
    assert order.index("MarketMemory") < order.index("Replay")
    for name in ("MarketMemory", "Replay"):
        assert gw.discover(name).state is ServiceState.READY
    resp = gw.dispatch(request("Replay", payload="hello"))
    assert resp.ok and resp.payload == "hello"


def test_dispatch_before_start_is_unavailable():
    gw = _gateway()
    gw.register_service(manifest("Echo"), echo_handler)
    resp = gw.dispatch(request("Echo"))                  # not started -> not READY
    assert resp.status is GatewayStatus.UNAVAILABLE


def test_start_fails_on_missing_dependency():
    gw = _gateway()
    gw.register_service(manifest("Replay", dependencies=("MarketMemory",)),
                        echo_handler)
    with pytest.raises(DependencyError):
        gw.start()


def test_find_by_capability():
    gw = _gateway()
    gw.register_service(manifest("Snapshot", capabilities=("Snapshot",)),
                        echo_handler)
    gw.start()
    found = gw.find(capability="Snapshot")
    assert [s.name for s in found] == ["Snapshot"]


def test_find_by_kind():
    gw = _gateway()
    gw.register_service(manifest("Ext", kind=ServiceKind.EXTERNAL), echo_handler)
    gw.register_service(manifest("Int", kind=ServiceKind.INTERNAL), echo_handler)
    assert [s.name for s in gw.find(kind=ServiceKind.EXTERNAL)] == ["Ext"]


def test_degraded_service_not_routable():
    gw = _gateway()
    gw.register_service(manifest("Echo"), echo_handler)
    gw.start()
    gw.mark_degraded("Echo")
    assert gw.dispatch(request("Echo")).status is GatewayStatus.UNAVAILABLE
    gw.mark_ready("Echo")
    assert gw.dispatch(request("Echo")).ok


def test_stop_service():
    gw = _gateway()
    gw.register_service(manifest("Echo"), echo_handler)
    gw.start()
    gw.stop("Echo")
    assert gw.discover("Echo").state is ServiceState.STOPPED


def test_registration_emits_event():
    events = []
    gw = _gateway(sink=events.append)
    gw.register_service(manifest("Echo"), echo_handler)
    assert GatewayEventName.SERVICE_REGISTERED in [e.name for e in events]


def test_health_metrics_version_endpoints():
    gw = _gateway()
    gw.register_service(manifest("Echo"), echo_handler)
    gw.start()
    gw.dispatch(request("Echo"))
    assert gw.metrics_snapshot()["total"] == 1
    assert gw.version_info()["core_version"]
    assert "status" in gw.health_report()
    gw.health.register_check("core", lambda: True)
    assert gw.health_status().value == "OK"


def test_discover_missing_raises():
    gw = _gateway()
    with pytest.raises(ServiceNotFoundError):
        gw.discover("nope")
