"""Phase 61.7 TASK 8 — Runtime Self Check."""

from ai.providers.circuit_breaker import CircuitBreakerConfig, ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_state import RuntimeState
from ai.runtime.self_check import CheckStatus, run_self_check


class _FakeProviderManager:
    def __init__(self, names):
        self._names = names

    def list_providers(self):
        return list(self._names)

    def get_provider(self, name):
        return object() if name in self._names else None


def test_self_check_with_no_providers_registered_reports_failed_and_overall_failed():
    report = run_self_check(provider_manager=_FakeProviderManager([]))

    provider_result = next(r for r in report.results if r.name == "Provider")
    assert provider_result.status == CheckStatus.FAILED
    assert report.overall_status == CheckStatus.FAILED


def test_self_check_with_registered_but_unhealthy_providers_reports_warning():
    from ai.providers.provider_status import HealthStatus

    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.OFFLINE, reason="test setup")
    provider_manager = _FakeProviderManager(["gemini"])

    report = run_self_check(provider_manager=provider_manager, health_tracker=health_tracker)

    provider_result = next(r for r in report.results if r.name == "Provider")
    assert provider_result.status == CheckStatus.WARNING


def test_self_check_runtime_reflects_injected_runtime_manager_state():
    manager = RuntimeManager(initial_state=RuntimeState.FAILED)

    report = run_self_check(runtime_manager=manager)

    runtime_result = next(r for r in report.results if r.name == "Runtime")
    assert runtime_result.status == CheckStatus.FAILED
    assert report.overall_status == CheckStatus.FAILED


def test_self_check_runtime_pass_when_healthy():
    manager = RuntimeManager()  # defaults to READY

    report = run_self_check(runtime_manager=manager)

    runtime_result = next(r for r in report.results if r.name == "Runtime")
    assert runtime_result.status == CheckStatus.PASS


def test_self_check_reports_every_expected_subsystem():
    report = run_self_check()
    names = {r.name for r in report.results}
    assert names == {"Provider", "Runtime", "Validation", "Cache", "Audit", "EventBus", "CircuitBreaker"}


def test_self_check_circuit_breaker_open_is_a_warning_not_a_failure():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=2))
    for _ in range(2):
        breaker.record_failure("gemini")
    provider_manager = _FakeProviderManager(["gemini"])

    report = run_self_check(provider_manager=provider_manager, circuit_breaker=breaker, health_tracker=health_tracker)

    breaker_result = next(r for r in report.results if r.name == "CircuitBreaker")
    assert breaker_result.status == CheckStatus.WARNING
    assert "gemini" in breaker_result.detail


def test_self_check_never_raises_with_all_defaults():
    report = run_self_check()
    assert report.overall_status in (CheckStatus.PASS, CheckStatus.WARNING, CheckStatus.FAILED)


def test_overall_status_is_pass_with_no_results():
    from ai.runtime.self_check import RuntimeSelfCheckReport
    assert RuntimeSelfCheckReport(results=[]).overall_status == CheckStatus.PASS
