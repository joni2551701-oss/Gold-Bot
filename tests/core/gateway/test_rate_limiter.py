"""Tests for the Gateway rate limiter (module 10)."""

from core_layer.gateway.rate_limiter import RateLimiter

from _gfakes import at


def test_allows_up_to_capacity():
    rl = RateLimiter(capacity=3, refill_per_second=0.0)
    now = at(0)
    assert rl.allow("k", now) is True
    assert rl.allow("k", now) is True
    assert rl.allow("k", now) is True
    assert rl.allow("k", now) is False       # bucket empty, no refill


def test_refill_over_time():
    rl = RateLimiter(capacity=1, refill_per_second=1.0)
    assert rl.allow("k", at(0)) is True
    assert rl.allow("k", at(0)) is False
    assert rl.allow("k", at(1)) is True       # 1s later -> 1 token refilled


def test_keys_are_independent():
    rl = RateLimiter(capacity=1, refill_per_second=0.0)
    assert rl.allow("a", at(0)) is True
    assert rl.allow("b", at(0)) is True       # different key, own bucket
    assert rl.allow("a", at(0)) is False


def test_reset():
    rl = RateLimiter(capacity=1, refill_per_second=0.0)
    rl.allow("k", at(0))
    assert rl.allow("k", at(0)) is False
    rl.reset("k")
    assert rl.allow("k", at(0)) is True
