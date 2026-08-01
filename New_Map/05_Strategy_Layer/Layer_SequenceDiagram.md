# Strategy Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Strategy Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Context Layer
↓
Indicator Layer
↓
StrategyService
↓
StrategyManager
↓
StrategyProfiles
↓
StrategyEngine
↓
StrategyLibrary
↓
Selected Strategy
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
