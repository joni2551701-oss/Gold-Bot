"""Phase 61.6 TASK 2 — AI Runtime Lifecycle: runtime_state.py, runtime_manager.py, runtime_events.py."""

from ai.event_bus import EventBus, EventType
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_state import RuntimeState, VALID_TRANSITIONS, is_valid_transition


def test_fresh_runtime_manager_defaults_to_ready():
    manager = RuntimeManager()
    assert manager.current_state() == RuntimeState.READY
    assert manager.is_healthy() is True


def test_shutdown_is_terminal_no_outgoing_transitions():
    assert VALID_TRANSITIONS[RuntimeState.SHUTDOWN] == frozenset()


def test_is_valid_transition_true_for_ready_to_busy():
    assert is_valid_transition(RuntimeState.READY, RuntimeState.BUSY) is True


def test_is_valid_transition_false_for_shutdown_to_anything():
    assert is_valid_transition(RuntimeState.SHUTDOWN, RuntimeState.READY) is False


def test_transition_applies_a_valid_transition():
    manager = RuntimeManager()
    event = manager.transition(RuntimeState.DEGRADED, reason="circuit open")

    assert event is not None
    assert event.from_state == RuntimeState.READY
    assert event.to_state == RuntimeState.DEGRADED
    assert manager.current_state() == RuntimeState.DEGRADED
    assert manager.is_healthy() is True


def test_transition_rejects_an_invalid_transition_and_state_is_unchanged():
    manager = RuntimeManager(initial_state=RuntimeState.SHUTDOWN)
    event = manager.transition(RuntimeState.READY)

    assert event is None
    assert manager.current_state() == RuntimeState.SHUTDOWN


def test_failed_state_is_not_healthy():
    manager = RuntimeManager()
    manager.transition(RuntimeState.FAILED, reason="every provider unavailable")
    assert manager.is_healthy() is False


def test_history_records_construction_and_every_transition():
    manager = RuntimeManager(initial_state=RuntimeState.INITIALIZING)
    manager.transition(RuntimeState.READY, reason="startup complete")
    manager.transition(RuntimeState.BUSY)

    history = manager.history()

    assert len(history) == 3
    assert history[0].to_state == RuntimeState.INITIALIZING
    assert history[1].to_state == RuntimeState.READY
    assert history[2].to_state == RuntimeState.BUSY


def test_transitioning_into_ready_publishes_runtime_started_on_the_event_bus():
    bus = EventBus()
    manager = RuntimeManager(initial_state=RuntimeState.INITIALIZING, event_bus=bus)

    manager.transition(RuntimeState.READY, reason="startup complete")

    started = bus.history(EventType.RUNTIME_STARTED)
    assert len(started) == 1


def test_transitioning_into_shutdown_publishes_runtime_stopped_on_the_event_bus():
    bus = EventBus()
    manager = RuntimeManager(event_bus=bus)

    manager.transition(RuntimeState.SHUTDOWN, reason="owner requested")

    stopped = bus.history(EventType.RUNTIME_STOPPED)
    assert len(stopped) == 1


def test_transitioning_into_failed_publishes_runtime_failed_on_the_event_bus():
    bus = EventBus()
    manager = RuntimeManager(event_bus=bus)

    manager.transition(RuntimeState.FAILED, reason="every provider unavailable")

    failed = bus.history(EventType.RUNTIME_FAILED)
    assert len(failed) == 1
    assert failed[0].payload["reason"] == "every provider unavailable"
    assert failed[0].payload["from_state"] == RuntimeState.READY.value


def test_construction_with_no_event_bus_never_raises():
    manager = RuntimeManager()
    manager.transition(RuntimeState.SHUTDOWN)


def test_an_invalid_transition_never_publishes_an_event():
    bus = EventBus()
    manager = RuntimeManager(initial_state=RuntimeState.SHUTDOWN, event_bus=bus)

    manager.transition(RuntimeState.READY)

    assert bus.history() == []
