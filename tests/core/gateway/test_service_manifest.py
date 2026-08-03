"""Tests for the service manifest (module 10, amendments 2, 3, 6)."""

from core_layer.gateway.service_manifest import (
    ServiceManifest, ServiceKind, HealthPolicy,
)

from _gfakes import manifest


def test_defaults():
    m = ServiceManifest(name="MarketMemory")
    assert m.version == "1.0.0"
    assert m.capabilities == ()
    assert m.dependencies == ()
    assert m.kind is ServiceKind.INTERNAL
    assert isinstance(m.health_policy, HealthPolicy)


def test_has_capability():
    m = manifest("Replay", capabilities=("Replay", "Timeline"))
    assert m.has_capability("Replay")
    assert not m.has_capability("Snapshot")


def test_as_dict_roundtrip_fields():
    m = manifest("Snapshot", capabilities=("Snapshot",),
                 dependencies=("PersistentMemory",), owner="core",
                 description="snapshot mgmt", max_failures=5,
                 recovery_seconds=60)
    d = m.as_dict()
    assert d["name"] == "Snapshot"
    assert d["capabilities"] == ["Snapshot"]
    assert d["dependencies"] == ["PersistentMemory"]
    assert d["kind"] == "internal"
    assert d["health_policy"]["max_consecutive_failures"] == 5
    assert d["health_policy"]["recovery_timeout_seconds"] == 60.0
    assert d["owner"] == "core"
    assert d["description"] == "snapshot mgmt"
