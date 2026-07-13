# decision/

## Purpose
Blends signal confidence and AI confidence into one final trade
verdict: APPROVE, REJECT, or NO_TRADE.

## Flow
```
Signal Candidate + AI Analysis
      |
      v
Decision Engine   -- confidence blending + threshold logic
      |
      v
Risk Manager
```

## Responsibilities
`decision_engine.py`'s `DecisionEngine.evaluate()`: averages
`SignalCandidate.confidence` and `AIAnalysisResult.confidence`; if AI
did not approve → REJECT; if the blend is below `min_confidence`
(0.50) → NO_TRADE; if below `approve_confidence` (0.80) → REJECT;
otherwise → APPROVE.

## Input
`SignalCandidate` (from `signals/`) + `AIAnalysisResult` (from `ai/`).

## Output
`TradeDecision` (`action`, `confidence`, `reason`, plus the original
signal/AI-analysis objects).

## Dependencies
`ai/` (for `AIAnalysisResult`) and `signals/` (for `SignalCandidate`).
No dependency on `database/`, `telegram/`, or `risk/`.

## Future Expansion
None planned. Confidence-threshold values are the one thing
`CLAUDE.md`'s Trading Safety rules name explicitly as "never modify
... without approval."
