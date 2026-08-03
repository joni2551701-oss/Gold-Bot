"""Phase 61.6 TASK 8 — Runtime Configuration Profiles."""

from ai_layer.ai_engine.cache.cache_policy import CachePolicy
from ai_layer.ai_engine.runtime.runtime_profiles import (
    DEVELOPMENT_PROFILE,
    PRODUCTION_PROFILE,
    TESTING_PROFILE,
    apply_provider_priority,
    resolve_profile,
)


def test_three_named_profiles_exist_with_distinct_names():
    assert DEVELOPMENT_PROFILE.name == "development"
    assert TESTING_PROFILE.name == "testing"
    assert PRODUCTION_PROFILE.name == "production"


def test_production_profile_matches_the_codebase_own_existing_production_defaults():
    assert PRODUCTION_PROFILE.timeout_seconds == 15  # matches gemini_provider.py's _REQUEST_TIMEOUT_SECONDS
    assert PRODUCTION_PROFILE.cache_ttl_seconds == 300  # matches CachePolicy's own default_ttl_seconds


def test_production_profile_requires_confidence_metadata_testing_and_development_do_not():
    assert "confidence" in PRODUCTION_PROFILE.validation_schema.required_metadata_keys
    assert "confidence" not in DEVELOPMENT_PROFILE.validation_schema.required_metadata_keys
    assert "confidence" not in TESTING_PROFILE.validation_schema.required_metadata_keys


def test_testing_profile_disables_caching():
    assert TESTING_PROFILE.cache_ttl_seconds == 0


def test_to_cache_policy_produces_a_real_cache_policy_instance():
    policy = PRODUCTION_PROFILE.to_cache_policy()
    assert isinstance(policy, CachePolicy)
    assert policy.default_ttl_seconds == 300


def test_resolve_profile_is_case_insensitive():
    assert resolve_profile("PRODUCTION") is PRODUCTION_PROFILE
    assert resolve_profile("Development") is DEVELOPMENT_PROFILE
    assert resolve_profile(" testing ") is TESTING_PROFILE


def test_resolve_profile_unknown_name_returns_none_never_fabricates():
    assert resolve_profile("staging") is None


def test_apply_provider_priority_reorders_named_providers_first():
    candidates = ["gemini", "openai", "claude", "grok"]

    reordered = apply_provider_priority(candidates, priority=("claude", "grok"))

    assert reordered == ["claude", "grok", "gemini", "openai"]


def test_apply_provider_priority_empty_priority_returns_candidates_unchanged():
    candidates = ["gemini", "openai"]

    assert apply_provider_priority(candidates, priority=()) == candidates


def test_apply_provider_priority_never_invents_a_candidate_not_already_present():
    candidates = ["gemini", "openai"]

    reordered = apply_provider_priority(candidates, priority=("claude", "gemini"))

    assert reordered == ["gemini", "openai"]
    assert "claude" not in reordered


def test_default_profiles_all_have_no_provider_priority_override():
    assert DEVELOPMENT_PROFILE.provider_priority == ()
    assert TESTING_PROFILE.provider_priority == ()
    assert PRODUCTION_PROFILE.provider_priority == ()
