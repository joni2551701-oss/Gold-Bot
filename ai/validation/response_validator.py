"""
AI Layer — Response Validator (Phase 61.2: AI Runtime Foundation,
TASK 5).

`validate_response()` is the one gate every real provider call's
`ProviderResult` passes through before `ai/runtime/ai_service.py`
(TASK 6) caches, audits, or returns it. Composes `schemas.py`
(structural expectations) and `safety.py` (heuristic content checks) --
reimplements neither.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from ai.providers.base_provider import ProviderResult
from ai.validation.safety import check_safety
from ai.validation.schemas import DEFAULT_SCHEMA, ResponseSchema


@dataclass(frozen=True)
class ValidationResult:
    """Same "structured result, never raise" convention `signal_layer/signal_builder/schema.py`'s `ValidationResult` and `ai/context/`'s own dataclasses already use in this codebase."""
    accepted: bool
    errors: List[str] = field(default_factory=list)


def validate_response(result: ProviderResult, schema: Optional[ResponseSchema] = None) -> ValidationResult:
    """Never raises: every failure mode (wrong type, empty content, out-of-range confidence, unsafe content) produces a rejected ValidationResult, not an exception."""
    schema = schema if schema is not None else DEFAULT_SCHEMA
    errors: List[str] = []

    if not isinstance(result, ProviderResult):
        return ValidationResult(accepted=False, errors=["result is not a ProviderResult instance"])

    if not isinstance(result.content, str):
        errors.append("content is not a string")
    elif len(result.content.strip()) < schema.min_content_length:
        errors.append("content is empty or below the minimum required length")
    else:
        errors.extend(check_safety(result.content))

    for key in schema.required_metadata_keys:
        if key not in result.metadata:
            errors.append(f"missing required metadata key: {key!r}")

    confidence = result.metadata.get("confidence")
    if confidence is not None:
        low, high = schema.confidence_range
        if not isinstance(confidence, (int, float)) or not (low <= confidence <= high):
            errors.append(f"confidence {confidence!r} outside allowed range {schema.confidence_range}")

    return ValidationResult(accepted=len(errors) == 0, errors=errors)
