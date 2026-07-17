"""
AI Layer — Explanation Output Contract (Phase 63.0: Senior Trading AI
Foundation, TASK 3).

Pure data shape -- no generation logic. Not read by
`explanation_engine.py` this phase (Rule: "AI hali ishlatmaydi" — AI
does not use it yet); a future, separately-approved phase decides
whether/how `ExplanationEngine`'s real `RuntimeResponse` gets adapted
into this richer shape, the same "contract now, wiring later" pattern
`ai/content/content_schema.py`'s `ContentResult` already established
in Phase 61.5.

Added as a new file inside the existing `ai/explanation/` package
(Module Reuse Principle step 2 — extend an existing package, not a new
top-level one) rather than editing `explanation_engine.py` itself,
since this is a new data contract, not a change to that module's
existing, already-tested behavior.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ai.content.content_types import ContentType


@dataclass(frozen=True)
class ExplanationOutput:
    """
    title: short headline for the explanation.
    summary: one-paragraph plain-language summary.
    body: the full explanation text.
    risk_note: standing risk-awareness text (e.g. "Markets can move
        against any analysis; this is not a guarantee.") -- stored,
        never auto-appended anywhere this phase.
    invalidation: what would make this explanation's reasoning
        outdated or wrong (e.g. "if price closes below X").
    confidence: 0.0-1.0, the explanation's own confidence in its
        reasoning -- distinct from any trading signal's confidence.
    language: language code the text is written in (e.g. "en", "uz",
        "ru") -- a plain string this phase, not yet validated against
        `translation/language_registry.py` (Phase 63.0 TASK 6, a
        separate, independent package).
    content_type: which `ai.content.content_types.ContentType` this
        explanation is shaped for, if any.
    metadata: free-form, provider/generation-specific detail, same
        convention `ai.providers.base_provider.ProviderResult.metadata`
        already uses.
    """
    title: str
    summary: str
    body: str
    risk_note: str
    invalidation: str
    confidence: float
    language: str
    content_type: Optional[ContentType] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
