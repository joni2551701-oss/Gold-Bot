"""Phase 61.4 TASK 3 — telegram/owner/ai_commands.py tests. Not registered into command_router.py -- these call the functions directly."""

from ai.access.permissions import AIRole
from ai.access.usage_limits import UsageLimiter
from ai.audit.provider_stats import ProviderStats
from ai.audit.usage_accounting import UserUsageStats
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_status import HealthStatus
from ai.providers.provider_manager import ProviderStatus
from telegram.owner.ai_commands import (
    AICommandResult,
    ai_cost,
    ai_disable,
    ai_enable,
    ai_health,
    ai_limit,
    ai_provider,
    ai_runtime_online,
    ai_status,
    ai_usage,
    current_provider_for,
)


class _FakeProviderManager:
    def __init__(self, names):
        self._names = list(names)

    def list_providers(self):
        return list(self._names)

    def get_provider(self, name):
        return None

    def status_of(self, name):
        return ProviderStatus.FALLBACK


def test_ai_status_reports_online_when_a_provider_is_healthy():
    """ProviderHealthTracker() seeds every real registered provider name as ONLINE by default (Phase 61.1's own "optimistic default") -- an unrecorded name outside the registry is the ⚪ case instead."""
    provider_manager = _FakeProviderManager(["gemini", "some_unregistered_provider"])
    health_tracker = ProviderHealthTracker()

    result = ai_status(provider_manager=provider_manager, health_tracker=health_tracker)

    assert isinstance(result, AICommandResult)
    assert result.success is True
    assert "🟢 Online" in result.message
    assert "Gemini 🟢" in result.message
    assert "Some_Unregistered_Provider ⚪" in result.message


def test_ai_status_reports_offline_when_no_provider_is_healthy():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.OFFLINE)

    result = ai_status(provider_manager=provider_manager, health_tracker=health_tracker)

    assert "🔴 Offline" in result.message


def test_ai_status_lists_capability_enabled_state():
    capability_manager = CapabilityManager()
    capability_manager.disable(Capability.VISION)

    result = ai_status(provider_manager=_FakeProviderManager([]), capability_manager=capability_manager)

    assert "❌ Vision" in result.message


def test_ai_provider_reports_current_and_fallback():
    provider_manager = _FakeProviderManager(["gemini", "claude", "openai"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    health_tracker.record("claude", HealthStatus.ONLINE)

    result = ai_provider(Capability.ANALYSIS, provider_manager=provider_manager, health_tracker=health_tracker)

    assert result.success is True
    assert "Gemini" in result.message
    assert "Claude" in result.message


def test_ai_provider_with_no_available_candidate_reports_none():
    provider_manager = _FakeProviderManager([])
    health_tracker = ProviderHealthTracker()

    result = ai_provider(Capability.ANALYSIS, provider_manager=provider_manager, health_tracker=health_tracker)

    assert result.success is True
    assert "No available provider" in result.message


def test_ai_provider_health_reflects_real_success_rate_when_present():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    stats = {"gemini": ProviderStats(provider_name="gemini", total_calls=10, success_count=9, avg_latency_ms=100.0, total_tokens=0, total_cost=0.0)}

    result = ai_provider(Capability.ANALYSIS, provider_manager=provider_manager, health_tracker=health_tracker, provider_stats=stats)

    assert "90%" in result.message


def test_ai_provider_health_is_n_a_without_call_history():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)

    result = ai_provider(Capability.ANALYSIS, provider_manager=provider_manager, health_tracker=health_tracker)

    assert "N/A" in result.message


def test_ai_disable_turns_off_a_known_capability():
    capability_manager = CapabilityManager()
    result = ai_disable("vision", capability_manager=capability_manager)

    assert result.success is True
    assert capability_manager.is_enabled(Capability.VISION) is False


def test_ai_disable_rejects_an_unknown_capability():
    result = ai_disable("not_a_real_capability")
    assert result.success is False


def test_ai_enable_turns_on_a_known_capability():
    capability_manager = CapabilityManager()
    capability_manager.disable(Capability.VISION)
    result = ai_enable("vision", capability_manager=capability_manager)

    assert result.success is True
    assert capability_manager.is_enabled(Capability.VISION) is True


def test_ai_limit_sets_a_known_roles_daily_ceiling():
    usage_limiter = UsageLimiter()
    result = ai_limit("premium", 1000, usage_limiter=usage_limiter)

    assert result.success is True
    assert usage_limiter.check("someone", AIRole.PREMIUM, Capability.CHAT).limit == 1000


def test_ai_limit_rejects_an_unknown_role():
    result = ai_limit("not_a_real_role", 1000)
    assert result.success is False


def test_ai_limit_rejects_a_negative_limit():
    result = ai_limit("premium", -5)
    assert result.success is False


def test_ai_cost_matches_the_directors_worked_example_shape():
    provider_stats = {
        "gemini": ProviderStats(provider_name="gemini", total_calls=10, success_count=10, avg_latency_ms=100.0, total_tokens=0, total_cost=12.40),
        "openai": ProviderStats(provider_name="openai", total_calls=5, success_count=5, avg_latency_ms=100.0, total_tokens=0, total_cost=8.20),
    }
    result = ai_cost(provider_stats)

    assert result.success is True
    assert "Today AI Cost" in result.message
    assert "$12.40" in result.message
    assert "$8.20" in result.message
    assert "Total" in result.message
    assert "$20.60" in result.message


def test_ai_cost_with_no_call_history_reports_zero():
    result = ai_cost({})
    assert result.success is True
    assert "$0.00" in result.message


def test_ai_usage_reports_a_known_users_stats():
    user_usage = {
        "111": UserUsageStats(telegram_id="111", total_calls=3, total_tokens=150, total_cost=0.15, cost_by_provider={"gemini": 0.15}),
    }
    result = ai_usage("111", user_usage)

    assert result.success is True
    assert "111" in result.message
    assert "3" in result.message
    assert "$0.15" in result.message


def test_ai_usage_for_unknown_telegram_id_reports_no_usage_not_an_error():
    result = ai_usage("does-not-exist", {})
    assert result.success is True
    assert "No AI usage" in result.message


def test_ai_runtime_online_true_when_a_provider_is_healthy():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    assert ai_runtime_online(provider_manager, health_tracker) is True


def test_ai_runtime_online_false_when_nothing_is_healthy():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.OFFLINE)
    assert ai_runtime_online(provider_manager, health_tracker) is False


def test_current_provider_for_matches_ai_providers_own_current_field():
    provider_manager = _FakeProviderManager(["gemini", "claude"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    health_tracker.record("claude", HealthStatus.ONLINE)

    current = current_provider_for(Capability.ANALYSIS, provider_manager, health_tracker)
    result = ai_provider(Capability.ANALYSIS, provider_manager=provider_manager, health_tracker=health_tracker)

    assert current is not None
    assert current.title() in result.message


def test_current_provider_for_is_none_when_nothing_available():
    provider_manager = _FakeProviderManager([])
    assert current_provider_for(Capability.ANALYSIS, provider_manager, ProviderHealthTracker()) is None


def test_ai_health_shows_per_provider_stats_breakdown():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    provider_stats = {
        "gemini": ProviderStats(
            provider_name="gemini", total_calls=12450, success_count=12336,
            avg_latency_ms=420.0, total_tokens=2_100_000, total_cost=14.23,
        ),
    }

    result = ai_health(provider_manager=provider_manager, provider_stats=provider_stats, health_tracker=health_tracker)

    assert result.success is True
    assert "AI HEALTH" in result.message
    assert "420 ms" in result.message
    assert "99." in result.message  # success rate percentage
    assert "12450" in result.message
    assert "2100000" in result.message
    assert "$14.23" in result.message
    assert "114" in result.message  # failure_count = total_calls - success_count = 114


def test_ai_health_reports_n_a_for_a_provider_with_no_call_history():
    provider_manager = _FakeProviderManager(["gemini"])
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)

    result = ai_health(provider_manager=provider_manager, provider_stats={}, health_tracker=health_tracker)

    assert result.success is True
    assert "N/A" in result.message


def test_ai_health_with_no_providers_registered():
    result = ai_health(provider_manager=_FakeProviderManager([]), provider_stats={}, health_tracker=ProviderHealthTracker())
    assert result.success is True
    assert "No providers registered." in result.message


def test_ai_explanation_status_reports_real_counts():
    """Phase 63.1 TASK 7 -- Templates is a fixed 3, Personas/Languages come from the real registries, never hardcoded."""
    from telegram.owner.ai_commands import ai_explanation_status

    result = ai_explanation_status()

    assert result.success is True
    assert "ACTIVE" in result.message
    assert "Templates:\n3" in result.message
    assert "Personas:\n1" in result.message
    assert "Languages:\n3" in result.message
