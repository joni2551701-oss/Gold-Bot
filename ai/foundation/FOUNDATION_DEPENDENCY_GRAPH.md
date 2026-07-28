# FOUNDATION_DEPENDENCY_GRAPH.md — TASK-AI-001

Status: dependency map of `ai/foundation/`. Every edge is an internal
`ai.foundation.* → ai.foundation.*` import; there are **no** edges to
any other `ai/` subpackage, to Core/Telegram/Database/etc., or to any
third-party package. Verified acyclic (AST cycle detector: 0 cycles).

## Internal edges (module → module)

```
context.py        -> (stdlib only)
lifecycle.py      -> (stdlib only)
interfaces.py     -> (stdlib only)

session.py        -> context
registry.py       -> interfaces
factory.py        -> interfaces
runtime.py        -> lifecycle
dummy.py          -> interfaces, lifecycle

manager.py        -> interfaces, lifecycle, registry, factory, session, runtime
self_check.py     -> manager, dummy, interfaces, lifecycle
```

## Layered view (bottom = no dependencies)

```
Layer 0 (leaves, stdlib only):   interfaces   lifecycle   context
Layer 1 (single collaborator):   registry(->interfaces)  factory(->interfaces)
                                 runtime(->lifecycle)     session(->context)
                                 dummy(->interfaces,lifecycle)
Layer 2 (composition root):      manager(->interfaces,lifecycle,registry,
                                          factory,session,runtime)
Layer 3 (entry point / demo):    self_check(->manager,dummy,...)
```

Strictly one-directional, top depends on bottom, never the reverse.

## External dependency check

- **Other `ai/` subpackages:** none. The subpackage-level cycle
  detector reports `ai.foundation` with zero cross-subpackage edges.
- **Core / Platform / Media / Telegram / Database:** none — not even
  `core.logger`. Confirmed by:
  `grep -rE "^\s*(from|import)\s+" ai/foundation/*.py` shows only
  stdlib and `ai.foundation.*` imports.
- **Third-party:** none. Pure Python stdlib
  (`abc`, `dataclasses`, `enum`, `typing`, `datetime`, `uuid`).

## Whole-`ai/` impact

Adding `ai/foundation/` kept the entire `ai/` package acyclic (the
TASK-AI-000A result of **0 circular dependencies** is preserved).
`ai/foundation/` is a new leaf that nothing else in `ai/` imports yet —
by design, it is the base the rest of the AI layer will later depend
on (Dependency Inversion), not a participant in today's graph.
