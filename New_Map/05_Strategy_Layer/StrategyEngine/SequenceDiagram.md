# StrategyEngine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyEngine Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
StrategyManager (Activated Strategy)
↓
Market Context
↓
Indicator Context
↓
StrategyEngine
↓
Execute Strategy
↓
Coordinate Pipeline
↓
Collect Result
↓
Validate Strategy Result
↓
Aggregate Strategy Result
↓
StrategyService
```
---
# Update Sequence
```text
Context Updated
↓
Re-Execute Strategy
↓
Recalculate Strategy
↓
Publish Strategy Result
```
---
# Runtime Rules
1. StrategyManager tomonidan faollashtirilgan Strategiya mavjud bo'lishi kerak.
2. Context tayyor bo'lishi kerak.
3. Indicator Context tayyor bo'lishi kerak.
4. Strategy Discovery, Selection va Profile Loading bu sequence'da bajarilmaydi (StrategyManager'da bajarilgan).
5. Validation Publish'dan oldin bajariladi.
6. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading
↓
Executing
↓
Validating
↓
Publishing
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence
StrategyManager (Activated Strategy)
↓
StrategyEngine
↓
Strategy Result
↓
StrategyService
