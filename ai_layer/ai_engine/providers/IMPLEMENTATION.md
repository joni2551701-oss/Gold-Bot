# IMPLEMENTATION.md -- ai_layer/ai_engine/providers

## `base_provider.py`

AI Layer — Provider Interface Foundation (Phase 61.0: AI Infrastructure

Classes: `ProviderResult`, `BaseAIProvider`

## `circuit_breaker.py`

AI Layer — Provider Circuit Breaker (Phase 61.6: AI Operations &

Classes: `CircuitState`, `CircuitBreakerConfig`, `ProviderCircuitBreaker`

## `claude_provider.py`

AI Layer — Real Claude Provider (Phase 61.5: AI Production Integration

Classes: `ClaudeProvider`

## `gemini_provider.py`

AI Layer — Real Gemini Provider (Phase 61.2: AI Runtime Foundation,

Classes: `GeminiProvider`

## `grok_provider.py`

AI Layer — Real Grok Provider (Phase 61.5: AI Production Integration

Classes: `GrokProvider`

## `openai_provider.py`

AI Layer — Real OpenAI Provider (Phase 61.5: AI Production Integration

Classes: `OpenAIProvider`

## `placeholder_providers.py`

AI Layer — Placeholder Providers (Phase 61.0: AI Infrastructure

Classes: `_StubProviderMixin`, `LocalLLMProvider`

## `provider_capabilities.py`

AI Layer — Provider Capability Matrix (Phase 61.1: AI Provider

Top-level functions: `supports()`, `capabilities_of()`

## `provider_failover.py`

AI Layer — Provider Failover (Phase 61.1: AI Provider Reliability

Top-level functions: `select_available()`

## `provider_health.py`

AI Layer — Provider Health Tracker (Phase 61.1: AI Provider

Classes: `ProviderHealthRecord`, `ProviderHealthTracker`

## `provider_manager.py`

AI Layer — Provider Manager (Phase 61.0: AI Infrastructure Foundation,

Classes: `ProviderStatus`, `ProviderManager`

## `provider_registry.py`

AI Layer — Provider Registry (Phase 61.0: AI Infrastructure

Classes: `ProviderDescriptor`

Top-level functions: `build_provider_registry()`

## `provider_status.py`

AI Layer — Provider Health Status (Phase 61.1: AI Provider Reliability

Classes: `HealthStatus`

## `runtime_errors.py`

AI Layer — Provider Runtime Errors (Phase 61.2: AI Runtime Foundation,

Classes: `ProviderRuntimeError`, `ProviderTimeoutError`, `ProviderRateLimitError`, `ProviderInvalidResponseError`, `ProviderUnavailableError`

Top-level functions: `classify_provider_exception()`, `record_provider_failure()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
