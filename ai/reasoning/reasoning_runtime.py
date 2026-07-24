"""
AI Layer — Reasoning Runtime (Phase 63.4, TASK 3).

`ReasoningRuntime` is deterministic and structural only -- it never
calls `AIService`/`BaseAIProvider`, never makes a network call, and
never computes a probability, correlation score, or any derived
number itself. The caller fully assembles a `ReasoningResult`
(`conclusion`, `confidence`, `steps`) before `reason()` ever sees it;
this class's only job is storage, ordering, and simple deterministic
reads over already-supplied data -- the same "compute now, connect
later" posture `ai/explanation/explanation_builder.py` and
`ai/memory/memory_runtime.py` already established.

Reasoning sits between Memory and Conversation in the Official
Intelligence Pipeline (`docs/roadmap/AI_EVOLUTION.md`). Per the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`), this module never imports
`ai/explanation/`, `ai/content/`, `ai/conversation/`, `broadcast/`,
`media/`, or `translation/` -- every one of those sits downstream of
Reasoning in the chain.
"""

from typing import Dict, List, Optional, Sequence

from ai.reasoning.models import ReasoningResult


class ReasoningRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager -- a caller/test never needs a pre-populated runtime to exercise this class."""

    def __init__(self) -> None:
        self._results: Dict[str, ReasoningResult] = {}
        self._order: List[str] = []

    def reason(self, result: ReasoningResult) -> ReasoningResult:
        """Stores `result` under its own key, overwriting any existing entry with that key, and returns it unchanged. Never computes a new value -- the caller supplies the fully-formed ReasoningResult."""
        if result.key not in self._results:
            self._order.append(result.key)
        self._results[result.key] = result
        return result

    def explain(self, key: str) -> Optional[str]:
        """Returns the stored result's own `conclusion` text. Never raises: an unknown key returns None."""
        result = self._results.get(key)
        return result.conclusion if result is not None else None

    def summarize(self, key: str) -> Optional[str]:
        """Joins each stored step's `label: value` into one short string. Never raises: an unknown key returns None."""
        result = self._results.get(key)
        if result is None:
            return None
        return "; ".join(f"{step.label}: {step.value}" for step in result.steps)

    def evaluate(self, key: str) -> Optional[float]:
        """Returns the stored result's own `confidence`. Never raises: an unknown key returns None."""
        result = self._results.get(key)
        return result.confidence if result is not None else None

    def compare(self, key_a: str, key_b: str) -> Optional[float]:
        """Returns `confidence(key_a) - confidence(key_b)`. Never raises: either key missing returns None."""
        result_a = self._results.get(key_a)
        result_b = self._results.get(key_b)
        if result_a is None or result_b is None:
            return None
        return result_a.confidence - result_b.confidence

    def chain(self, keys: Sequence[str]) -> Sequence[ReasoningResult]:
        """Returns the stored results for `keys`, in the given order. An unknown key is silently skipped rather than raising."""
        return tuple(self._results[key] for key in keys if key in self._results)

    def history(self) -> Sequence[ReasoningResult]:
        """Returns every stored result, in the order `reason()` first stored each key."""
        return tuple(self._results[key] for key in self._order)
