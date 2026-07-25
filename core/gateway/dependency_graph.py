"""
Service dependency graph (v1.1 Phase 1, module 10; ORDER-064 amendment 3).

Each service declares its dependencies by name (e.g. Replay -> MarketMemory,
Snapshot -> PersistentMemory). Before the Gateway starts services it checks
the graph: every dependency must be a registered service, and there must be
no cycle. `resolution_order` returns a startup order in which every service
comes up after the ones it depends on.

Pure functions over `{name: dependencies}` mappings; dependency-free.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple


class DependencyError(RuntimeError):
    """Raised on a missing dependency or a dependency cycle."""


def missing_dependencies(graph: Dict[str, Iterable[str]]) -> Dict[str, List[str]]:
    """Map each service to its declared deps that are not registered."""
    known = set(graph)
    out: Dict[str, List[str]] = {}
    for name, deps in graph.items():
        gaps = [d for d in deps if d not in known]
        if gaps:
            out[name] = gaps
    return out


def find_cycle(graph: Dict[str, Iterable[str]]) -> List[str]:
    """Return one dependency cycle as a name list, or [] if acyclic."""
    WHITE, GREY, BLACK = 0, 1, 2
    color: Dict[str, int] = {n: WHITE for n in graph}
    stack: List[str] = []

    def visit(node: str) -> List[str]:
        color[node] = GREY
        stack.append(node)
        for dep in graph.get(node, ()):
            if dep not in color:            # unregistered -> handled elsewhere
                continue
            if color[dep] == GREY:
                idx = stack.index(dep)
                return stack[idx:] + [dep]
            if color[dep] == WHITE:
                found = visit(dep)
                if found:
                    return found
        color[node] = BLACK
        stack.pop()
        return []

    for n in graph:
        if color[n] == WHITE:
            cycle = visit(n)
            if cycle:
                return cycle
    return []


def validate(graph: Dict[str, Iterable[str]]) -> None:
    """Raise DependencyError on any missing dependency or cycle."""
    missing = missing_dependencies(graph)
    if missing:
        raise DependencyError(f"missing dependencies: {missing}")
    cycle = find_cycle(graph)
    if cycle:
        raise DependencyError("dependency cycle: " + " -> ".join(cycle))


def resolution_order(graph: Dict[str, Iterable[str]]) -> List[str]:
    """Topological startup order (dependencies first). Validates first."""
    validate(graph)
    order: List[str] = []
    seen: set = set()

    def visit(node: str) -> None:
        if node in seen:
            return
        for dep in graph.get(node, ()):
            visit(dep)
        seen.add(node)
        order.append(node)

    for n in graph:
        visit(n)
    return order


def build_graph(manifests: Iterable) -> Dict[str, Tuple[str, ...]]:
    """Build a {name: dependencies} graph from an iterable of manifests."""
    return {m.name: tuple(m.dependencies) for m in manifests}
