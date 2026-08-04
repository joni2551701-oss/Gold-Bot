# IMPLEMENTATION.md — data_layer/providers/provider_errors

## `provider_errors.py`

Public surface:

- `Optional`
- `ProviderError`
- `ProviderAuthError`
- `ProviderTimeoutError`
- `ProviderRateLimitError`
- `ProviderResponseError`
- `ProviderUnavailableError`
- `provider_error_for_status`

## Design Notes

Converted from a flat `provider_errors.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `provider_errors.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
