"""Tests for the service registry + discovery (module 10, amendments 2, 3)."""

import pytest

from core.gateway.service_registry import (
    ServiceRegistry, DuplicateServiceError, ServiceNotFoundError,
)
from core.gateway.service_manifest import ServiceKind
from core.gateway.dependency_graph import DependencyError

from _gfakes import manifest, echo_handler


def _registry(*manifests):
    reg = ServiceRegistry()
    for m in manifests:
        reg.register(m, echo_handler)
    return reg


def test_register_and_discover():
    reg = _registry(manifest("MarketMemory"))
    svc = reg.discover("MarketMemory")
    assert svc.name == "MarketMemory"
    assert reg.get("MarketMemory") is svc


def test_duplicate_rejected():
    reg = _registry(manifest("A"))
    with pytest.raises(DuplicateServiceError):
        reg.register(manifest("A"), echo_handler)


def test_discover_missing_raises():
    reg = ServiceRegistry()
    with pytest.raises(ServiceNotFoundError):
        reg.discover("nope")


def test_find_by_capability():
    reg = _registry(
        manifest("Replay", capabilities=("Replay",)),
        manifest("Snapshot", capabilities=("Snapshot",)))
    found = reg.find(capability="Replay")
    assert [s.name for s in found] == ["Replay"]


def test_find_by_kind():
    reg = _registry(
        manifest("Internal1", kind=ServiceKind.INTERNAL),
        manifest("External1", kind=ServiceKind.EXTERNAL))
    found = reg.find(kind=ServiceKind.EXTERNAL)
    assert [s.name for s in found] == ["External1"]


def test_validate_dependencies_ok():
    reg = _registry(manifest("Replay", dependencies=("MarketMemory",)),
                    manifest("MarketMemory"))
    reg.validate_dependencies()          # no raise


def test_validate_dependencies_missing():
    reg = _registry(manifest("Replay", dependencies=("MarketMemory",)))
    with pytest.raises(DependencyError):
        reg.validate_dependencies()


def test_startup_order():
    reg = _registry(manifest("Replay", dependencies=("MarketMemory",)),
                    manifest("MarketMemory"))
    order = reg.startup_order()
    assert order.index("MarketMemory") < order.index("Replay")
