"""core_layer/gateway/authorization -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `authorization.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `authorization.py`.
"""
from core_layer.gateway.authorization.authorization import (
    annotations,
    ABC,
    abstractmethod,
    Dict,
    Optional,
    Set,
    Principal,
    Authorizer,
    AllowAllAuthorizer,
    RoleAuthorizer,
)

__all__ = [
    "annotations",
    "ABC",
    "abstractmethod",
    "Dict",
    "Optional",
    "Set",
    "Principal",
    "Authorizer",
    "AllowAllAuthorizer",
    "RoleAuthorizer",
]
