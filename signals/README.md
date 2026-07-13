# signals/

## Purpose
Defines the signal candidate data contract and routes context to
strategies for candidate generation.

## Responsibilities
- `models.py` — `SignalCandidate`, the immutable contract every
  strategy produces and every downstream layer (AI/Decision/Risk/
  Telegram) consumes.
- `signal_engine.py` — thin router to `strategies.StrategyManager`.

## Input
`ContextSnapshot` (from `context/`).

## Output
`List[SignalCandidate]`.

## Dependencies
`context/` and `strategies/`. No dependency on `ai/`, `decision/`,
`risk/`, `database/`, or `telegram/`.

## Future Roadmap
None planned. Candidate filtering/ranking (single-best-candidate
selection) intentionally lives in `core/pipeline.py`, not here — see
`docs/AUDIT_REPORT.md` for why.
