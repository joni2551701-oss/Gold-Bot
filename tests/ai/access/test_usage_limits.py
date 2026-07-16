"""Phase 61.0 TASK 6 — AI Usage Limits: in-memory per-user/capability daily ceiling."""

from ai.access.permissions import AIRole
from ai.access.usage_limits import UsageLimiter
from ai.capabilities.capability import Capability


def test_owner_has_unlimited_usage():
    limiter = UsageLimiter()
    for _ in range(500):
        limiter.record("owner_id", Capability.CHAT)
    result = limiter.check("owner_id", AIRole.OWNER, Capability.CHAT)
    assert result.allowed is True
    assert result.limit == 0


def test_free_role_is_blocked_after_reaching_its_daily_limit():
    limiter = UsageLimiter()
    for _ in range(10):
        limiter.record("free_user", Capability.CHAT)
    result = limiter.check("free_user", AIRole.FREE, Capability.CHAT)
    assert result.allowed is False
    assert result.used == 10


def test_usage_is_tracked_independently_per_capability():
    limiter = UsageLimiter()
    limiter.record("user_1", Capability.CHAT)
    result = limiter.check("user_1", AIRole.FREE, Capability.EXPLANATION)
    assert result.used == 0


def test_reset_clears_one_users_counters():
    limiter = UsageLimiter()
    limiter.record("user_1", Capability.CHAT)
    limiter.record("user_2", Capability.CHAT)
    limiter.reset("user_1")
    assert limiter.check("user_1", AIRole.FREE, Capability.CHAT).used == 0
    assert limiter.check("user_2", AIRole.FREE, Capability.CHAT).used == 1


def test_reset_without_argument_clears_everyone():
    limiter = UsageLimiter()
    limiter.record("user_1", Capability.CHAT)
    limiter.reset()
    assert limiter.check("user_1", AIRole.FREE, Capability.CHAT).used == 0


def test_check_does_not_increment_usage():
    limiter = UsageLimiter()
    limiter.check("user_1", AIRole.FREE, Capability.CHAT)
    limiter.check("user_1", AIRole.FREE, Capability.CHAT)
    assert limiter.check("user_1", AIRole.FREE, Capability.CHAT).used == 0


def test_set_limit_changes_this_instances_ceiling():
    limiter = UsageLimiter()
    limiter.set_limit(AIRole.PREMIUM, 1000)
    for _ in range(50):
        limiter.record("premium_user", Capability.CHAT)
    result = limiter.check("premium_user", AIRole.PREMIUM, Capability.CHAT)
    assert result.allowed is True
    assert result.limit == 1000


def test_set_limit_on_one_instance_never_leaks_into_a_fresh_instance():
    """Phase 61.4 TASK 3 fix: __init__ now always copies _DEFAULT_DAILY_LIMITS instead of aliasing it, so set_limit() can never mutate the shared default for other instances."""
    first = UsageLimiter()
    first.set_limit(AIRole.FREE, 9999)

    second = UsageLimiter()
    assert second.check("someone", AIRole.FREE, Capability.CHAT).limit == 10
