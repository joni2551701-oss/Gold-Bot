"""
AI Layer — memory foundation (Phase 55).

Future shape:

    User -> Trading History -> AI Memory -> Personal Assistant

ContextMemory is where a future v0.4+ AI Assistant Core would keep
short-term conversational/analysis context per user (e.g. "what did I
just tell this user in the last exchange") so a follow-up question
doesn't need to be re-explained from scratch. This is foundation
only: an in-process, in-memory store with no persistence and no
database integration, exactly as this phase's spec requires
("Database integration: QILINMASIN. Faqat interface.").

Not wired into core/pipeline.py, decision/decision_engine.py, or any
Telegram handler -- nothing calls this yet.
"""

from typing import Any, Dict, Optional


class ContextMemory:
    """
    Minimal per-key in-memory store. `key` is left as a plain string
    (e.g. a telegram_id) rather than typed further, since the shape of
    what gets stored is intentionally undecided at this stage -- a
    future phase defines that once a real use case exists.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def save(self, key: str, value: Any) -> None:
        """Stores `value` under `key`, overwriting any existing entry."""
        self._store[key] = value

    def load(self, key: str) -> Optional[Any]:
        """Returns the stored value for `key`, or None if nothing is stored."""
        return self._store.get(key)

    def clear(self, key: Optional[str] = None) -> None:
        """Clears one key's entry, or every entry if `key` is omitted."""
        if key is None:
            self._store.clear()
        else:
            self._store.pop(key, None)
