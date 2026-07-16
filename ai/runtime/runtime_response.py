"""
AI Layer — AI Runtime Response (Phase 61.2: AI Runtime Foundation,
TASK 6).
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
    """
    accepted: bool
    content: Optional[str]
    provider_name: Optional[str]
    reason: str
    from_cache: bool = False
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
