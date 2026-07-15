# ai/

## Purpose
Advisory-only AI evaluation layer. As of Phase 55, this is a
**foundation** for a future AI Assistant Core — no real AI/LLM call
happens anywhere in this directory.

## Flow
```
Signal Candidate + Context
      |
      v
AI Layer   -- advisory only, never approves/rejects itself
      |
      v
Decision Engine
```

## Responsibilities
- `ai_analyzer.py` — the production entry point `core/pipeline.py`
  calls. Currently a permanent-reject heuristic stub (documented,
  intentional — see the README's top-level Environment Variables
  table and `docs/AI_ARCHITECTURE.md`).
- `interfaces.py` — `AIAnalyzerInterface`/`MarketContext`/
  `UserContext`/`AIResponse`: the contract a future provider
  implements.
- `memory/`, `prompts/`, `profiles/`, `journal/`, `analyzer/` —
  Phase 55 foundation subpackages (memory, prompt templates, user
  profile model, trade journal, and a re-export of the canonical
  analyzer respectively). None are wired into the production pipeline.
- `learning_context.py` (Phase 60.6: Learning Loop Foundation, TASK 7;
  extended Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 6)
  — `LearningContext` + `build_learning_context()`: bundles
  already-computed `learning/` data (`recent_failures`/
  `successful_patterns`/`strategy_stats`, plus Phase 60.7's
  `patterns`/`failures`/`regimes`/`confidence`) into the Director's own
  AI-facing JSON shape. Generates no explanation/recommendation text
  itself — that is left to a future AI consumer, still bound by
  `AIAnalyzerInterface`'s advisory-only contract. See
  `docs/LEARNING_LOOP.md`.

## Input
`SignalCandidate` + `ContextSnapshot` (production `AIAnalyzer`); the
new foundation types (`MarketContext`/`UserContext`) for anything
built against `interfaces.py` in a future phase; an already-built
`Sequence[learning.models.LearningRecord]` for `learning_context.py`.

## Output
`AIAnalysisResult` (production); `AIResponse` (future interface
shape); `LearningContext` (`learning_context.py`).

## Dependencies
`context/` and `signals/` for the production/interface path. No
dependency on `database/` or `telegram/` — an AI provider must never
reach either directly (see `CLAUDE.md`'s Trading Safety rules).
`learning_context.py` (Phase 60.6, extended 60.7) additionally imports
`analytics.strategy_report.compute_win_rate`,
`learning.models`/`learning.pattern_detector`, and
`learning.confidence.compute_pattern_confidence` — read-only, no
trading-decision logic, and still no `database/`/`telegram/`
dependency.

## Future Roadmap
Full audit and folder-structure rationale in `docs/AI_ARCHITECTURE.md`.
The real work — replacing the permanent-reject stub with actual
heuristic/model scoring — is explicitly out of this phase's scope and
is the natural first v0.4 AI Assistant Core task.
