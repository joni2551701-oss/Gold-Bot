"""data_layer/providers/provider_errors -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `provider_errors.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `provider_errors.py`.
"""
from data_layer.providers.provider_errors.provider_errors import (
    Optional,
    ProviderError,
    ProviderAuthError,
    ProviderTimeoutError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderUnavailableError,
    provider_error_for_status,
)

__all__ = [
    "Optional",
    "ProviderError",
    "ProviderAuthError",
    "ProviderTimeoutError",
    "ProviderRateLimitError",
    "ProviderResponseError",
    "ProviderUnavailableError",
    "provider_error_for_status",
]
