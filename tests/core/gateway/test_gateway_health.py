"""Tests for Gateway health, metrics, version and context (module 10)."""

from core.gateway.health_service import HealthService, GatewayHealth
from core.gateway.metrics_service import GatewayMetrics
from core.gateway.version_service import (
    VersionService, CORE_VERSION, GATEWAY_API_VERSION,
)
from core.gateway.gateway_context import new_context
from core.gateway.gateway_request import GatewayResponse, GatewayStatus

from _gfakes import at, principal


# -- health -------------------------------------------------------------
def test_health_ok_when_no_checks():
    assert HealthService().status() is GatewayHealth.OK


def test_health_grades():
    hs = HealthService()
    hs.register_check("a", lambda: True)
    hs.register_check("b", lambda: True)
    assert hs.status() is GatewayHealth.OK
    hs.register_check("c", lambda: False)
    assert hs.status() is GatewayHealth.DEGRADED
    hs2 = HealthService()
    hs2.register_check("x", lambda: False)
    assert hs2.status() is GatewayHealth.DOWN


def test_health_check_exception_is_failure():
    hs = HealthService()
    hs.register_check("boom", lambda: (_ for _ in ()).throw(ValueError()))
    assert hs.status() is GatewayHealth.DOWN
    assert hs.report()["checks"]["boom"] is False


# -- metrics ------------------------------------------------------------
def test_metrics_record():
    m = GatewayMetrics()
    m.record(GatewayResponse(status=GatewayStatus.OK, service="A"))
    m.record(GatewayResponse(status=GatewayStatus.ERROR, service="A"))
    m.record(GatewayResponse(status=GatewayStatus.OK, service="B"))
    snap = m.snapshot()
    assert snap["total"] == 3
    assert snap["by_status"]["ok"] == 2
    assert snap["by_service"]["A"] == 2
    assert snap["failures"] == 1


# -- version ------------------------------------------------------------
def test_version_info():
    info = VersionService().info()
    assert info["core_version"] == CORE_VERSION
    assert info["api_version"] == GATEWAY_API_VERSION


# -- context (amendment 4) ---------------------------------------------
def test_context_fields():
    ctx = new_context("svc", principal("u1"), now=at(0),
                      core_version="1.1.0", api_version="1.0")
    assert ctx.service == "svc"
    assert ctx.principal.id == "u1"
    assert ctx.timestamp == at(0)
    assert ctx.core_version == "1.1.0"
    assert ctx.request_id                       # auto-generated, non-empty
    assert ctx.correlation_id == ctx.request_id  # defaults to request_id


def test_context_uses_given_correlation_id():
    ctx = new_context("svc", principal(), now=at(0), correlation_id="corr-9")
    assert ctx.correlation_id == "corr-9"
