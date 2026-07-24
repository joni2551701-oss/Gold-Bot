"""
AI Layer — AI Runtime Response (Phase 61.2: AI Runtime Foundation,
TASK 6; extended Phase 61.3: AI Intelligence Layer, TASK 8).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RuntimeResponse:
    """
    accepted: False for every rejection path (access denied, capability
        disabled, no prompt derivable, no available provider, every
        provider failed, validation rejected) -- `content` is always
        None when this is False, never a partial/fabricated answer.
    from_cache: True when `content` came from `ai/cache/response_cache.py`
        rather than a fresh provider call this request.
    errors: validator errors (empty unless a provider response was
        rejected by `ai.validation.response_validator.validate_response()`).
    request_id (Phase 61.3, TASK 8): the `ai.audit.request_log.AIRequestLogEntry.request_id`
        this specific provider attempt was logged under -- reuses that
        existing UUID, no new ID scheme. `None` for every path where no
        single request-log entry corresponds to this response: an
        early rejection before a provider was even attempted (access/
        capability/prompt), a cache hit (never logged as a request --
        no provider call happened), or the final "every provider
        failed" rejection after multiple attempts (no single attempt
        to point to). Pass this to `ai.audit.trace.trace_request()` to
        look up the full request/response record.
    """
    accepted: bool
    content: Optional[str]
    provider_name: Optional[str]
    reason: str
    from_cache: bool = False
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    request_id: Optional[str] = None
