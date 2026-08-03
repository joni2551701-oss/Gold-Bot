"""
AI Layer — AI Persona Model (Phase 63.0: Senior Trading AI Foundation,
TASK 1).

Pure identity data — no behavior. `Persona` never builds a prompt,
never calls `AIService`, and is never read by `ai/prompts/` or
`ai/runtime/` this phase (Rule 5: "Persona prompt yozmaydi. AI
chaqirmaydi. Faqat identity."). A future, separately-approved phase
decides how (or whether) a `Persona`'s fields feed into a real prompt.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    """
    name: the persona's display name (e.g. "Senior Trading AI").
    role: a one-line description of what the persona represents.
    tone: the intended voice (e.g. "calm, professional, data-driven").
    language_style: prose register the persona is meant to use (e.g.
        "concise, no hype, no guaranteed-profit language").
    disclaimer: the standing disclaimer text this persona is meant to
        carry (e.g. "Educational content only, not financial advice.") --
        stored, never auto-appended anywhere this phase.
    system_identity: a short, stable identifier a future prompt-builder
        would reference (e.g. "goldbot-senior-trading-ai-v1") -- not a
        prompt itself, just a stable name for one.
    """
    name: str
    role: str
    tone: str
    language_style: str
    disclaimer: str
    system_identity: str
