"""core_layer/gateway/authentication -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `authentication.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `authentication.py`.
"""
from core_layer.gateway.authentication.authentication import (
    annotations,
    ABC,
    abstractmethod,
    Dict,
    Optional,
    GatewayRequest,
    Principal,
    ANONYMOUS,
    Authenticator,
    AllowAllAuthenticator,
    TokenAuthenticator,
)

__all__ = [
    "annotations",
    "ABC",
    "abstractmethod",
    "Dict",
    "Optional",
    "GatewayRequest",
    "Principal",
    "ANONYMOUS",
    "Authenticator",
    "AllowAllAuthenticator",
    "TokenAuthenticator",
]
