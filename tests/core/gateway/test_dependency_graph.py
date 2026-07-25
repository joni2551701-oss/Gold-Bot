"""Tests for the service dependency graph (module 10, amendment 3)."""

import pytest

from core.gateway.dependency_graph import (
    DependencyError, missing_dependencies, find_cycle, validate,
    resolution_order, build_graph,
)

from _gfakes import manifest


def test_no_missing_when_all_registered():
    graph = {"Replay": ["MarketMemory"], "MarketMemory": []}
    assert missing_dependencies(graph) == {}


def test_missing_dependency_detected():
    graph = {"Replay": ["MarketMemory"]}          # MarketMemory not registered
    assert missing_dependencies(graph) == {"Replay": ["MarketMemory"]}


def test_no_cycle_returns_empty():
    graph = {"Replay": ["MarketMemory"], "MarketMemory": []}
    assert find_cycle(graph) == []


def test_cycle_detected():
    graph = {"A": ["B"], "B": ["A"]}
    cycle = find_cycle(graph)
    assert cycle and cycle[0] == cycle[-1]


def test_validate_raises_on_missing():
    with pytest.raises(DependencyError):
        validate({"Replay": ["MarketMemory"]})


def test_validate_raises_on_cycle():
    with pytest.raises(DependencyError):
        validate({"A": ["B"], "B": ["A"]})


def test_resolution_order_dependencies_first():
    graph = {"Replay": ["MarketMemory"], "Snapshot": ["PersistentMemory"],
             "MarketMemory": [], "PersistentMemory": []}
    order = resolution_order(graph)
    assert order.index("MarketMemory") < order.index("Replay")
    assert order.index("PersistentMemory") < order.index("Snapshot")


def test_build_graph_from_manifests():
    manifests = [manifest("Replay", dependencies=("MarketMemory",)),
                 manifest("MarketMemory")]
    graph = build_graph(manifests)
    assert graph == {"Replay": ("MarketMemory",), "MarketMemory": ()}
