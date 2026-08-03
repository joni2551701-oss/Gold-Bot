"""
AI Layer — Response Safety Checks (Phase 61.2: AI Runtime Foundation,
TASK 5).

Two bounded, heuristic checks over a provider's returned text:

1. **Trade-directive language.** `ai/ai_prompt.py`'s own
   `SYSTEM_PROMPT` already forbids the (unrelated, existing) signal
   validator's AI call from generating a signal; this module applies
   the same "AI never issues a trade directive" principle to the new
   real-provider text responses this phase introduces, as a second,
   independent safety net -- CLAUDE.md's Trading Safety rules apply to
   every AI output, not just the one call site that already enforced
   it via a system prompt.
2. **Leaked-credential pattern.** Defense in depth for Rule 2 ("API
   key never logged/returned") -- the real safeguard is that
   `ai/providers/gemini_provider.py` never puts the key in a prompt or
   forwards user input capable of echoing it back, but a heuristic
   pattern check here catches an accidental leak (e.g. a
   misconfigured prompt) before a response is cached, audited, or
   returned to a caller.

Both checks are heuristic, not exhaustive -- they exist to catch an
obvious violation early, not to replace the structural guarantees
(Rule 1/2 in `ai/providers/gemini_provider.py`, "AI never approves a
trade" in `decision_layer/decision_engine/decision_engine.py`) that actually make those
properties true.
"""

import re
from typing import List

_FORBIDDEN_TRADE_DIRECTIVES = (
    "BUY NOW", "SELL NOW", "OPEN TRADE", "CLOSE TRADE", "PLACE ORDER",
    "EXECUTE TRADE", "ENTER POSITION",
)

# Google API key shape (Gemini/other Google Cloud keys): "AIza" + 35
# more alphanumeric/-/_ characters. Narrow and specific on purpose --
# a broad "looks like a secret" heuristic would false-positive on
# ordinary long tokens/hashes a legitimate response might contain.
_LEAKED_KEY_PATTERN = re.compile(r"AIza[0-9A-Za-z_\-]{35}")


def check_safety(content: str) -> List[str]:
    """Never raises: returns an empty list for safe content, one string per violation otherwise."""
    violations: List[str] = []

    upper_content = content.upper()
    for phrase in _FORBIDDEN_TRADE_DIRECTIVES:
        if phrase in upper_content:
            violations.append(f"contains trade-directive phrase: {phrase!r}")

    if _LEAKED_KEY_PATTERN.search(content):
        violations.append("content appears to contain a leaked API key pattern")

    return violations
