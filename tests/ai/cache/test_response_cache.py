"""Phase 61.1 TASK 9 — AI Response Cache Foundation. Cache key must never be bare prompt text; TTL is enforced."""

from datetime import datetime, timedelta, timezone

import pytest

from ai.cache.cache_policy import CacheKey, CachePolicy, compute_context_hash
from ai.cache.response_cache import ResponseCache
from ai.capabilities.capability import Capability


def _make_key(**overrides):
    defaults = dict(
        capability=Capability.CHAT, context_version="1.0", provider_name="gemini",
        prompt_version="v1", context_hash=compute_context_hash({"symbol": "XAUUSD"}),
    )
    defaults.update(overrides)
    return CacheKey(**defaults)


def test_compute_context_hash_is_deterministic_regardless_of_key_order():
    hash_a = compute_context_hash({"a": 1, "b": 2})
    hash_b = compute_context_hash({"b": 2, "a": 1})
    assert hash_a == hash_b


def test_compute_context_hash_differs_for_different_payloads():
    assert compute_context_hash({"a": 1}) != compute_context_hash({"a": 2})


def test_cache_key_requires_all_five_fields():
    with pytest.raises(TypeError):
        CacheKey(capability=Capability.CHAT)


def test_put_and_get_round_trips():
    cache = ResponseCache()
    key = _make_key()
    cache.put(key, "gold is trending up", metadata={"tokens": 42})
    entry = cache.get(key)
    assert entry.content == "gold is trending up"
    assert entry.metadata["tokens"] == 42


def test_get_returns_none_for_a_missing_key():
    cache = ResponseCache()
    assert cache.get(_make_key()) is None


def test_different_context_hash_is_a_different_cache_entry():
    cache = ResponseCache()
    key_a = _make_key(context_hash=compute_context_hash({"symbol": "XAUUSD"}))
    key_b = _make_key(context_hash=compute_context_hash({"symbol": "EURUSD"}))
    cache.put(key_a, "answer for XAUUSD")
    assert cache.get(key_b) is None


def test_entry_expires_after_ttl():
    policy = CachePolicy(default_ttl_seconds=60)
    cache = ResponseCache(policy=policy)
    key = _make_key()
    cache.put(key, "cached answer")
    future = datetime.now(timezone.utc) + timedelta(seconds=120)
    assert cache.get(key, now=future) is None


def test_entry_within_ttl_is_still_valid():
    policy = CachePolicy(default_ttl_seconds=300)
    cache = ResponseCache(policy=policy)
    key = _make_key()
    cache.put(key, "cached answer")
    soon = datetime.now(timezone.utc) + timedelta(seconds=10)
    assert cache.get(key, now=soon) is not None


def test_is_expired_matches_get_behavior():
    cache = ResponseCache()
    key = _make_key()
    assert cache.is_expired(key) is True
    cache.put(key, "answer")
    assert cache.is_expired(key) is False


def test_clear_one_key():
    cache = ResponseCache()
    key_a = _make_key(provider_name="gemini")
    key_b = _make_key(provider_name="openai")
    cache.put(key_a, "a")
    cache.put(key_b, "b")
    cache.clear(key_a)
    assert cache.get(key_a) is None
    assert cache.get(key_b) is not None


def test_clear_without_argument_clears_everything():
    cache = ResponseCache()
    key = _make_key()
    cache.put(key, "answer")
    cache.clear()
    assert cache.get(key) is None


def test_cache_key_as_string_is_stable_for_identical_fields():
    key1 = _make_key()
    key2 = _make_key()
    assert key1.as_string() == key2.as_string()
