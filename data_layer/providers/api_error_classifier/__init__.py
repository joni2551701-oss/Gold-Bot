"""data_layer/providers/api_error_classifier -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `api_error_classifier.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `api_error_classifier.py`.
"""
from data_layer.providers.api_error_classifier.api_error_classifier import (
    requests,
    codes,
    ExternalAPIError,
    classify_api_error,
    classify_empty_response,
)

__all__ = [
    "requests",
    "codes",
    "ExternalAPIError",
    "classify_api_error",
    "classify_empty_response",
]
