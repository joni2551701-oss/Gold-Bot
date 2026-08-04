"""
Core — Phone Number Hashing (Phase 61.4: AI Product & Control Layer,
TASK 4).

"Telefon raqamni ochiq saqlamaslik" (never store the raw phone
number) -- this module is the one place a phone number is ever
touched before being discarded; only its hash is ever persisted
(`database_layer/user_repository/user_models.py`'s `UserRecord.phone_hash`).

Uses HMAC-SHA256 with a pepper (`core_layer.secrets.Secrets.PHONE_HASH_SALT`),
not a bare `hashlib.sha256(phone)` -- a phone number has far less
entropy than a typical secret (a fixed country-code prefix + a handful
of digits), so an unsalted hash is practically reversible via a
rainbow table built by hashing every plausible number. A caller must
still never log or persist the raw phone string; this module only
protects the value that *is* persisted.

If `PHONE_HASH_SALT` is unset, a built-in default pepper is used so
`hash_phone_number()` still produces a deterministic value (required
for `ai/access/trial_manager.py`'s "same phone = same trial" matching
to work across restarts) -- but the module-level docstring on
`_DEFAULT_PEPPER` explains why a real deployment must set the
environment variable instead of relying on this fallback.
"""

import hashlib
import hmac
import re
from typing import Optional

from core_layer.secrets import Secrets

# Fallback pepper only -- every deployment should set PHONE_HASH_SALT
# via core_layer.secrets.Secrets.PHONE_HASH_SALT instead. Committed to
# source control, so it provides no real secrecy on its own; it exists
# only so hash_phone_number() is still deterministic (never raises,
# never produces a different hash for the same phone number across
# two calls) when a deployment has not yet configured a real pepper.
_DEFAULT_PEPPER = "goldbot-phone-hash-default-pepper-v1"


def _normalize_phone(phone: str) -> str:
    """Strips everything except leading '+' and digits, so '+998 90 123-45-67' and '998901234567' hash identically."""
    stripped = re.sub(r"[^\d+]", "", phone)
    if stripped.startswith("+"):
        return stripped
    return "+" + stripped


def hash_phone_number(phone: str, salt: Optional[str] = None) -> str:
    """
    Deterministic, salted hash of a phone number -- the raw `phone`
    argument is never returned, logged, or stored by this function.
    Never raises: an empty/whitespace-only phone still produces a
    (useless but well-formed) hash rather than crashing a registration
    flow on bad input; validating that a phone number is well-formed
    is a caller's job, not this function's.
    """
    resolved_salt = salt if salt is not None else (Secrets().PHONE_HASH_SALT or _DEFAULT_PEPPER)
    normalized = _normalize_phone(phone or "")
    return hmac.new(resolved_salt.encode("utf-8"), normalized.encode("utf-8"), hashlib.sha256).hexdigest()
