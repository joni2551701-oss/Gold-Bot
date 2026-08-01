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
Market Context
↓
Indicator Context
↓
StrategyEngine
↓
Load Strategy
↓
Load Strategy Profile
↓
Execute Strategy
↓
Validate Strategy Result
↓
Generate Strategy Result
↓
StrategyService
```
---
# Update Sequence
```text
Context Updated
↓
Reload Strategy
↓
Recalculate Strategy
↓
Publish Strategy Result
```
---
# Runtime Rules
1. Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. Strategy Profile yuklanishi kerak.
4. Validation Publish'dan oldin bajariladi.
5. Circular Dependency taqiqlanadi.
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
Market Context
↓
Indicator Context
↓
StrategyEngine
↓
Strategy Result
↓
StrategyService
