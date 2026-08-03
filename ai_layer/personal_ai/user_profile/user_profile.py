"""
AI Layer — user profile foundation (Phase 55).

Goal: give a future AI Assistant Core a typed shape for "what does the
AI layer know about this user" -- experience level, preferred
strategy, risk style, language -- so a personalized response doesn't
require re-deriving that from raw database rows on every call.

Distinct from database.user_models.UserRecord (the real,
database-backed settings record platform_layer/telegram/user_service.py reads and
writes): UserRecord is the source of truth for a user's actual
settings; AIUserProfile is a lightweight, AI-facing *projection* of a
subset of that data, plus fields (experience_level) that don't exist
in the users table at all. This phase does not connect the two --
"Databasega ulanmasin. Hozir: faqat model." -- no repository, no
service, nothing reads database.user_repository here.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AIUserProfile:
    """
    Pure data model. No database access, no service layer, no
    behavior beyond the plain data it carries.
    """
    telegram_id: str
    experience_level: Optional[str] = None  # e.g. "beginner" | "intermediate" | "advanced"
    preferred_strategy: Optional[str] = None
    risk_style: Optional[str] = None  # e.g. "conservative" | "moderate" | "aggressive"
    language: Optional[str] = None
