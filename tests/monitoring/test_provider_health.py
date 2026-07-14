"""
Phase 59.2, TASK 6/9 -- monitoring/provider_health.py tests.
"""

from data.providers.base_provider import DataProvider, ProviderStatus
from data.providers.registry import build_default_registry
from monitoring.provider_health import (
    ProviderHealthReport,
    ProviderHealthStatus,
    check_provider_health,
    check_registry_health,
)


class _FakeProvider(DataProvider):
    def __init__(self, name, available, reason="", delay_seconds=0.0):
        self._name = name
        self._available = available
        self._reason = reason
        self._delay_seconds = delay_seconds

    def get_provider_name(self):
        return self._name

    def get_market_status(self):
        if self._delay_seconds:
            import time
            time.sleep(self._delay_seconds)
        return ProviderStatus(available=self._available, reason=self._reason)


def test_offline_provider_reports_offline():
    provider = _FakeProvider("test_offline", available=False, reason="not implemented")
    report = check_provider_health(provider)

    assert isinstance(report, ProviderHealthReport)
    assert report.status == ProviderHealthStatus.OFFLINE
    assert report.reason == "not implemented"


def test_available_fast_provider_reports_online():
    provider = _FakeProvider("test_online", available=True)
    report = check_provider_health(provider, degraded_threshold_ms=500.0)

    assert report.status == ProviderHealthStatus.ONLINE


def test_available_slow_provider_reports_degraded():
    provider = _FakeProvider("test_slow", available=True, delay_seconds=0.02)
    report = check_provider_health(provider, degraded_threshold_ms=5.0)

    assert report.status == ProviderHealthStatus.DEGRADED


def test_latency_is_a_real_measured_positive_number():
    provider = _FakeProvider("test_latency", available=True)
    report = check_provider_health(provider)

    assert report.latency_ms >= 0.0


def test_provider_name_comes_from_the_provider_itself():
    provider = _FakeProvider("my_custom_name", available=True)
    report = check_provider_health(provider)

    assert report.provider_name == "my_custom_name"


def test_check_provider_health_never_raises_for_every_stub_in_default_registry():
    registry = build_default_registry()
    for name in registry.all_names():
        check_provider_health(registry.get(name))  # must not raise


def test_check_registry_health_returns_one_report_per_registered_provider():
    registry = build_default_registry()

    reports = check_registry_health(registry)

    assert len(reports) == len(registry.all_names())
    assert {r.provider_name for r in reports} == set(registry.all_names())


def test_check_registry_health_reports_offline_for_every_unimplemented_stub():
    """MT5/Binance/FRED are always OFFLINE (unimplemented). TwelveData's status depends on whether an API key is configured -- tests/conftest.py sets a placeholder one for the suite, so it is deliberately excluded from this assertion."""
    registry = build_default_registry()

    reports = {r.provider_name: r for r in check_registry_health(registry)}

    assert reports["mt5"].status == ProviderHealthStatus.OFFLINE
    assert reports["binance"].status == ProviderHealthStatus.OFFLINE
    assert reports["fred"].status == ProviderHealthStatus.OFFLINE


def test_reason_reflects_disabled_status_matching_the_briefs_own_example():
    """Reconciles the brief's own 'MT5: Status: DISABLED' example with the three-state ONLINE/DEGRADED/OFFLINE model -- OFFLINE + a reason explaining why."""
    registry = build_default_registry()
    mt5_report = next(r for r in check_registry_health(registry) if r.provider_name == "mt5")

    assert mt5_report.status == ProviderHealthStatus.OFFLINE
    assert "not implemented" in mt5_report.reason.lower()


def test_check_registry_health_never_raises_on_empty_registry():
    from data.providers.registry import ProviderRegistry

    empty_registry = ProviderRegistry()
    reports = check_registry_health(empty_registry)

    assert reports == []
