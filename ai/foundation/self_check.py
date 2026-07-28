"""
AI Foundation — Self Check (TASK-AI-001: AI Foundation Activation).

A runnable, dependency-free demonstration that the Foundation works
end-to-end: Factory builds a component, Registry holds it, the Manager
drives the shared lifecycle, the Session Manager creates/closes/restores
a session carrying a `FoundationContext`, and the aggregate health
check reports HEALTHY.

Because TASK-AI-001 forbids adding files under `tests/`, this module is
how the Foundation's "it works" success criteria are demonstrated:
run `python -m ai.foundation.self_check` (exits 0 on success, 1 on
failure). Every check is a pure, deterministic assertion over the
Foundation's own public API -- no LLM, no provider, no I/O.

Depends only on stdlib and `ai.foundation.*`.
"""

from typing import List, Tuple

from ai.foundation.dummy import DummyAIComponent
from ai.foundation.interfaces import HealthState
from ai.foundation.lifecycle import LifecycleState
from ai.foundation.manager import AIManager

CheckResult = Tuple[str, bool, str]


def run_self_check() -> List[CheckResult]:
    """Exercise the whole Foundation and return (name, ok, detail) per check."""
    results: List[CheckResult] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, bool(ok), detail))

    manager = AIManager()

    # Factory + Registry: build a Dummy via a registered builder, then register it.
    manager.factory.register_builder("dummy", lambda: DummyAIComponent("dummy"))
    component = manager.factory.create("dummy")
    check("Factory.create", component.name == "dummy", f"built {component.name}")
    manager.registry.register(component)
    check("Registry.register/list", manager.registry.list() == ["dummy"], str(manager.registry.list()))
    check("Registry.get", manager.registry.get("dummy") is component, "retrieved same instance")

    # Lifecycle: CREATED -> INITIALIZED -> STARTED, fanned out to the component.
    check("Runtime initial state", manager.runtime.state is LifecycleState.CREATED, manager.runtime.state.value)
    manager.initialize()
    check("Manager.initialize", manager.runtime.state is LifecycleState.INITIALIZED, manager.runtime.state.value)
    manager.start()
    check("Manager.start", manager.runtime.state is LifecycleState.STARTED, manager.runtime.state.value)
    check("Runtime.status running", manager.runtime.status().running is True, str(manager.runtime.status()))

    # Dummy behavior: status() -> READY, echo() -> identity.
    check("Component.status READY", component.status() == "READY", component.status())
    check("Component.echo", component.echo("ping") == "ping", "echo returned input")

    # Session + Context: create, inspect the 5-field context, close, restore.
    session = manager.sessions.create_session(user_id="u1", language="uz", persona_id="p1")
    ctx = session.context
    check(
        "Session/Context fields",
        ctx.user_id == "u1" and ctx.language == "uz" and ctx.persona_id == "p1" and ctx.session_id == session.session_id,
        f"session_id={ctx.session_id}",
    )
    check("Session.close", manager.sessions.close_session(session.session_id) is True, "closed")
    check("Session inactive", session.session_id not in manager.sessions.active_sessions(), "not active")
    restored = manager.sessions.restore_session(session.session_id)
    check("Session.restore", restored is not None and restored.active, "restored + active")

    # Health: aggregate over registered components -> HEALTHY.
    report = manager.health()
    check("Health.aggregate HEALTHY", report.state is HealthState.HEALTHY, f"{report.state.value}; children={len(report.children)}")

    # Shutdown: terminal state, sessions cleared.
    manager.stop()
    manager.shutdown()
    check("Manager.shutdown", manager.runtime.state is LifecycleState.SHUTDOWN, manager.runtime.state.value)
    check("Sessions cleared", manager.sessions.list_sessions() == [], "no sessions after shutdown")

    return results


def main() -> int:
    results = run_self_check()
    ok_all = all(ok for _, ok, _ in results)
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}" + (f" -- {detail}" if detail else ""))
    print(f"\nAI Foundation self-check: {'SUCCESS' if ok_all else 'FAILURE'} "
          f"({sum(1 for _, ok, _ in results if ok)}/{len(results)} checks passed)")
    return 0 if ok_all else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
