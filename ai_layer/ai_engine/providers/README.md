# ai_layer / ai_engine / providers

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `base_provider.py` -- AI Layer — Provider Interface Foundation (Phase 61.0: AI Infrastructure
- `circuit_breaker.py` -- AI Layer — Provider Circuit Breaker (Phase 61.6: AI Operations &
- `claude_provider.py` -- AI Layer — Real Claude Provider (Phase 61.5: AI Production Integration
- `gemini_provider.py` -- AI Layer — Real Gemini Provider (Phase 61.2: AI Runtime Foundation,
- `grok_provider.py` -- AI Layer — Real Grok Provider (Phase 61.5: AI Production Integration
- `openai_provider.py` -- AI Layer — Real OpenAI Provider (Phase 61.5: AI Production Integration
- `placeholder_providers.py` -- AI Layer — Placeholder Providers (Phase 61.0: AI Infrastructure
- `provider_capabilities.py` -- AI Layer — Provider Capability Matrix (Phase 61.1: AI Provider
- `provider_failover.py` -- AI Layer — Provider Failover (Phase 61.1: AI Provider Reliability
- `provider_health.py` -- AI Layer — Provider Health Tracker (Phase 61.1: AI Provider
- `provider_manager.py` -- AI Layer — Provider Manager (Phase 61.0: AI Infrastructure Foundation,
- `provider_registry.py` -- AI Layer — Provider Registry (Phase 61.0: AI Infrastructure
- `provider_status.py` -- AI Layer — Provider Health Status (Phase 61.1: AI Provider Reliability
- `runtime_errors.py` -- AI Layer — Provider Runtime Errors (Phase 61.2: AI Runtime Foundation,

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `base_provider.py`: class `ProviderResult`
- `base_provider.py`: class `BaseAIProvider`
- `circuit_breaker.py`: class `CircuitState`
- `circuit_breaker.py`: class `CircuitBreakerConfig`
- `circuit_breaker.py`: class `ProviderCircuitBreaker`
- `claude_provider.py`: class `ClaudeProvider`
- `gemini_provider.py`: class `GeminiProvider`
- `grok_provider.py`: class `GrokProvider`
- `openai_provider.py`: class `OpenAIProvider`
- `placeholder_providers.py`: class `_StubProviderMixin`
- `placeholder_providers.py`: class `LocalLLMProvider`
- `provider_capabilities.py`: function `supports()`
- `provider_capabilities.py`: function `capabilities_of()`
- `provider_failover.py`: function `select_available()`
- `provider_health.py`: class `ProviderHealthRecord`
- `provider_health.py`: class `ProviderHealthTracker`
- `provider_manager.py`: class `ProviderStatus`
- `provider_manager.py`: class `ProviderManager`
- `provider_registry.py`: class `ProviderDescriptor`
- `provider_registry.py`: function `build_provider_registry()`
- `provider_status.py`: class `HealthStatus`
- `runtime_errors.py`: class `ProviderRuntimeError`
- `runtime_errors.py`: class `ProviderTimeoutError`
- `runtime_errors.py`: class `ProviderRateLimitError`
- `runtime_errors.py`: class `ProviderInvalidResponseError`
- `runtime_errors.py`: class `ProviderUnavailableError`
- `runtime_errors.py`: function `classify_provider_exception()`
- `runtime_errors.py`: function `record_provider_failure()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
