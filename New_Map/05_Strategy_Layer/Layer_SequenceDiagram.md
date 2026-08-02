# Strategy Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Strategy Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
StrategyLibrary
↓
StrategyProfiles
↓
StrategyManager (Discovery, Selection, Profile Loading, Activation)
↓
Context Layer
↓
Indicator Layer
↓
StrategyEngine (Execution, Coordination, Result Aggregation)
↓
Strategy Result
↓
StrategyService
↓
Signal Layer
```
---
# Runtime Rules
1. Context tayyor bo'lishi kerak.
2. Indicator tayyor bo'lishi kerak.
3. Strategy Profile yuklanishi kerak.
4. Strategy Validation bajarilishi kerak.
5. Strategy Result Signal Layer'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Selecting
↓
Loading
↓
Executing
↓
Validating
↓
Completed
```
---
# Summary
Context
↓
Indicators
↓
Strategy
↓
Strategy Result
↓
Signal Layer
