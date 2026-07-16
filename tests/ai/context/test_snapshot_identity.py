"""Phase 61.1.1 TASK 2/5 — Cache Freshness Correction: snapshot_id is content-derived, never time/random-derived."""

from ai.context.context_builder import build_ai_context
from ai.context.context_snapshot import AIContext
from ai.interfaces import MarketContext
from ai.cache.cache_policy import build_cache_key_from_context
from ai.capabilities.capability import Capability
from ai.cache.response_cache import ResponseCache

import pytest


def test_identical_content_produces_identical_snapshot_id():
    ctx1 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    ctx2 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    assert ctx1.snapshot_id == ctx2.snapshot_id


def test_identical_content_has_different_built_at_but_same_snapshot_id():
    """Proves snapshot_id is NOT built_at-derived -- the one thing the brief explicitly forbids."""
    ctx1 = build_ai_context()
    ctx2 = build_ai_context()
    assert ctx1.built_at != ctx2.built_at
    assert ctx1.snapshot_id == ctx2.snapshot_id


def test_different_content_produces_different_snapshot_id():
    ctx1 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    ctx2 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="downtrend"))
    assert ctx1.snapshot_id != ctx2.snapshot_id


def test_snapshot_id_is_none_for_a_directly_constructed_context():
    ctx = AIContext()
    assert ctx.snapshot_id is None


def test_build_cache_key_from_context_rejects_a_context_without_snapshot_id():
    ctx = AIContext()
    with pytest.raises(ValueError):
        build_cache_key_from_context(ctx, Capability.CHAT, "gemini", "v1")


def test_build_cache_key_from_context_pulls_snapshot_id_from_ai_context():
    ctx = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    key = build_cache_key_from_context(ctx, Capability.CHAT, "gemini", "v1")
    assert key.snapshot_id == ctx.snapshot_id


def test_same_snapshot_id_is_a_cache_hit():
    ctx1 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    ctx2 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))

    cache = ResponseCache()
    key1 = build_cache_key_from_context(ctx1, Capability.CHAT, "gemini", "v1")
    cache.put(key1, "gold is trending up")

    key2 = build_cache_key_from_context(ctx2, Capability.CHAT, "gemini", "v1")
    entry = cache.get(key2)
    assert entry is not None
    assert entry.content == "gold is trending up"


def test_different_snapshot_id_is_a_cache_miss():
    ctx1 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))
    ctx2 = build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="downtrend"))

    cache = ResponseCache()
    key1 = build_cache_key_from_context(ctx1, Capability.CHAT, "gemini", "v1")
    cache.put(key1, "gold is trending up")

    key2 = build_cache_key_from_context(ctx2, Capability.CHAT, "gemini", "v1")
    assert cache.get(key2) is None


def test_cache_key_requires_snapshot_id_field():
    from ai.cache.cache_policy import CacheKey
    with pytest.raises(TypeError):
        CacheKey(
            capability=Capability.CHAT, context_version="1.0", provider_name="gemini",
            prompt_version="v1", context_hash="somehash",
        )
