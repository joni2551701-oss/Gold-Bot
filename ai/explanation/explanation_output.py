"""
AI Layer — Explanation Output Contract (Phase 63.0: Senior Trading AI
Foundation, TASK 3; extended Phase 63.1: AI Explanation Intelligence
Layer, TASK 1).

Pure data shape -- no generation logic. As of Phase 63.1,
`explanation_builder.py`'s `ExplanationBuilder` is the first real
writer of this shape (a deterministic, template-based builder — no AI
provider call); `explanation_engine.py`'s own `RuntimeResponse` path
remains separate and still does not populate this contract.

Added as a new file inside the existing `ai/explanation/` package
(Module Reuse Principle step 2 — extend an existing package, not a new
top-level one) rather than editing `explanation_engine.py` itself,
since this is a new data contract, not a change to that module's
existing, already-tested behavior.

Phase 63.1 TASK 1 extension: six new optional fields
(`market_context`, `technical_reasoning`, `fundamental_reasoning`,
`risk_reasoning`, `educational_note`, `persona`) added with safe
defaults -- Constitution Article 9's permitted "add a new optional
field" shape on a LOCKed module. No existing field renamed, removed,
or had its type changed.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ai.content_types import ContentType


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
    content_type: which `ai.content_types.ContentType` this
        explanation is shaped for, if any.
    metadata: free-form, provider/generation-specific detail, same
        convention `ai.providers.base_provider.ProviderResult.metadata`
        already uses.
    market_context: (Phase 63.1) plain-language market-condition
        sentence (e.g. "Gold remains bullish on H1.") -- distinct from
        `ai.interfaces.MarketContext`, which is a data object; this is
        already-rendered text.
    technical_reasoning: (Phase 63.1) the technical-analysis sentence
        behind this explanation (e.g. "Liquidity sweep confirmed near
        demand zone.").
    fundamental_reasoning: (Phase 63.1) the fundamental/macro sentence,
        if any -- optional, most explanations today have none.
    risk_reasoning: (Phase 63.1) the specific risk sentence for this
        explanation (e.g. "Invalidation below previous liquidity
        low.") -- distinct from `risk_note`'s standing disclaimer text.
    educational_note: (Phase 63.1) an optional teaching aside, used by
        EDUCATION-mode explanations.
    persona: (Phase 63.1) the `ai.persona.persona.Persona.name` this
        explanation was built with, if any -- a plain string reference
        (matching `language`'s own plain-string convention), never a
        live `Persona` object stored on this frozen dataclass.
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
    market_context: Optional[str] = None
    technical_reasoning: Optional[str] = None
    fundamental_reasoning: Optional[str] = None
    risk_reasoning: Optional[str] = None
    educational_note: Optional[str] = None
    persona: Optional[str] = None
