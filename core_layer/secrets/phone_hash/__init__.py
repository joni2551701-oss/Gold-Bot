"""core_layer/secrets/phone_hash -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `phone_hash.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `phone_hash.py`.
"""
from core_layer.secrets.phone_hash.phone_hash import (
    hashlib,
    hmac,
    re,
    Optional,
    Secrets,
    hash_phone_number,
)

__all__ = [
    "hashlib",
    "hmac",
    "re",
    "Optional",
    "Secrets",
    "hash_phone_number",
]
