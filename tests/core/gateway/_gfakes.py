"""Shared helpers for Core Gateway Layer tests (module 10)."""

from datetime import datetime, timezone, timedelta

from core.gateway.service_manifest import (
    ServiceManifest, ServiceKind, HealthPolicy,
)
from core.gateway.gateway_request import GatewayRequest, Principal


def at(i, seconds=1):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(
        seconds=i * seconds)


class FakeClock:
    """Deterministic, manually-advanced clock callable."""

    def __init__(self, start=None):
        self._now = start or at(0)

    def __call__(self):
        return self._now

    def advance(self, seconds):
        self._now = self._now + timedelta(seconds=seconds)
        return self._now

    def set(self, now):
        self._now = now
        return self._now


def manifest(name, *, version="1.0.0", capabilities=(), dependencies=(),
             kind=ServiceKind.INTERNAL, owner="core", description="",
             max_failures=3, recovery_seconds=30):
    return ServiceManifest(
        name=name, version=version, capabilities=tuple(capabilities),
        dependencies=tuple(dependencies), kind=kind, owner=owner,
        description=description,
        health_policy=HealthPolicy(
            max_consecutive_failures=max_failures,
            recovery_timeout=timedelta(seconds=recovery_seconds)))


def echo_handler(ctx, payload):
    """A trivial service handler that returns its payload."""
    return payload


def boom_handler(ctx, payload):
    raise RuntimeError("handler failed")


def request(service="", *, capability=None, payload=None, token=None,
            correlation_id=None):
    return GatewayRequest(service=service, capability=capability,
                          payload=payload, token=token,
                          correlation_id=correlation_id)


def principal(pid="u1", roles=(), authenticated=True):
    return Principal(id=pid, roles=tuple(roles), authenticated=authenticated)
