"""
AI Layer — Response Validation Schemas (Phase 61.2: AI Runtime
Foundation, TASK 5).

Declares what "a valid `ai.providers.base_provider.ProviderResult`"
means -- pure data, no validation logic itself (that lives in
`response_validator.py`). A caller with different requirements builds
its own `ResponseSchema` rather than this module growing per-capability
special cases.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ResponseSchema:
    """
    min_content_length: `ProviderResult.content`, stripped, must be at
        least this long. 1 by default -- rejects an empty/whitespace-only
        response.
    required_metadata_keys: keys `ProviderResult.metadata` must carry.
        Empty by default -- `ProviderResult` itself only requires
        `content`; a specific capability's caller can require more
        (e.g. `("confidence",)`).
    confidence_range: if `metadata["confidence"]` is present, it must
        fall within this inclusive range.
    """
    min_content_length: int = 1
    required_metadata_keys: Tuple[str, ...] = ()
    confidence_range: Tuple[float, float] = (0.0, 1.0)


DEFAULT_SCHEMA = ResponseSchema()
