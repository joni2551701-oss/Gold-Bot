"""Tests for the Gateway router dispatch pipeline (module 10)."""

from core.gateway.service_registry import ServiceRegistry
from core.gateway.router import GatewayRouter
from core.gateway.rate_limiter import RateLimiter
from core.gateway.authentication import TokenAuthenticator
from core.gateway.authorization import RoleAuthorizer
from core.gateway.service_state import ServiceState
from core.gateway.gateway_request import GatewayStatus
from core.gateway.gateway_events import GatewayEventName

from _gfakes import (
    FakeClock, manifest, echo_handler, boom_handler, request, principal,
)


def _ready(reg, m, handler=echo_handler):
    svc = reg.register(m, handler)
    svc.transition(ServiceState.STARTING)
    svc.transition(ServiceState.READY)
    return svc


def test_happy_path_ok():
    reg = ServiceRegistry()
    _ready(reg, manifest("Echo", capabilities=("Echo",)))
    router = GatewayRouter(reg, clock=FakeClock())
    resp = router.dispatch(request("Echo", payload={"x": 1}))
    assert resp.ok
    assert resp.status is GatewayStatus.OK
    assert resp.payload == {"x": 1}
    assert resp.service == "Echo"
    assert resp.request_id


def test_unauthenticated():
    reg = ServiceRegistry()
    _ready(reg, manifest("Echo"))
    router = GatewayRouter(reg, authenticator=TokenAuthenticator({}),
                           clock=FakeClock())
    resp = router.dispatch(request("Echo"))              # no token
    assert resp.status is GatewayStatus.UNAUTHENTICATED


def test_not_found():
    router = GatewayRouter(ServiceRegistry(), clock=FakeClock())
    resp = router.dispatch(request("Missing"))
    assert resp.status is GatewayStatus.NOT_FOUND


def test_forbidden():
    reg = ServiceRegistry()
    _ready(reg, manifest("AdminSvc"))
    authz = RoleAuthorizer({"AdminSvc": {"admin"}})
    auth = TokenAuthenticator({"t": principal("u", roles=("user",))})
    router = GatewayRouter(reg, authenticator=auth, authorizer=authz,
                           clock=FakeClock())
    resp = router.dispatch(request("AdminSvc", token="t"))
    assert resp.status is GatewayStatus.FORBIDDEN


def test_unavailable_when_not_ready():
    reg = ServiceRegistry()
    reg.register(manifest("Echo"), echo_handler)         # stays REGISTERED
    router = GatewayRouter(reg, clock=FakeClock())
    resp = router.dispatch(request("Echo"))
    assert resp.status is GatewayStatus.UNAVAILABLE


def test_discovery_by_capability():
    reg = ServiceRegistry()
    _ready(reg, manifest("Replay", capabilities=("Replay",)))
    router = GatewayRouter(reg, clock=FakeClock())
    resp = router.dispatch(request(capability="Replay", payload=7))
    assert resp.ok and resp.payload == 7 and resp.service == "Replay"


def test_rate_limited():
    reg = ServiceRegistry()
    _ready(reg, manifest("Echo"))
    rl = RateLimiter(capacity=1, refill_per_second=0.0)
    router = GatewayRouter(reg, rate_limiter=rl, clock=FakeClock())
    assert router.dispatch(request("Echo")).ok
    assert router.dispatch(request("Echo")).status is GatewayStatus.RATE_LIMITED


def test_handler_error_contained_and_counted():
    reg = ServiceRegistry()
    _ready(reg, manifest("Bad"), handler=boom_handler)
    router = GatewayRouter(reg, clock=FakeClock())
    resp = router.dispatch(request("Bad"))
    assert resp.status is GatewayStatus.ERROR
    assert "handler failed" in resp.error


def test_circuit_opens_after_repeated_failures():
    reg = ServiceRegistry()
    _ready(reg, manifest("Bad", max_failures=2), handler=boom_handler)
    router = GatewayRouter(reg, clock=FakeClock())
    router.dispatch(request("Bad"))                      # fail 1
    router.dispatch(request("Bad"))                      # fail 2 -> OPEN
    resp = router.dispatch(request("Bad"))               # rejected by breaker
    assert resp.status is GatewayStatus.UNAVAILABLE
    assert resp.error == "circuit open"


def test_events_emitted_to_sink():
    reg = ServiceRegistry()
    _ready(reg, manifest("Echo"))
    events = []
    router = GatewayRouter(reg, clock=FakeClock(), event_sink=events.append)
    router.dispatch(request("Echo"))
    names = [e.name for e in events]
    assert GatewayEventName.REQUEST_RECEIVED in names
    assert GatewayEventName.AUTHENTICATED in names
    assert GatewayEventName.DISPATCHED in names
    assert GatewayEventName.COMPLETED in names


def test_metrics_accumulate():
    reg = ServiceRegistry()
    _ready(reg, manifest("Echo"))
    router = GatewayRouter(reg, clock=FakeClock())
    router.dispatch(request("Echo"))
    router.dispatch(request("Missing"))
    snap = router.metrics.snapshot()
    assert snap["total"] == 2
    assert snap["by_status"]["ok"] == 1
    assert snap["by_status"]["not_found"] == 1
