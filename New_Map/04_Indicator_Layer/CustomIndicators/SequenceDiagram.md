# CustomIndicators Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat CustomIndicators modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu CustomIndicators modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Load Indicator Context
↓
Load Proprietary Configuration
↓
Calculate Custom Indicators
↓
Calculate Composite Scores
↓
Validate Results
↓
Generate Custom Indicator State
↓
IndicatorService
```
---
# Update Sequence
```text
Market Context Updated
↓
Update Custom Indicators
↓
Validate Results
↓
Publish Custom Indicator State
```
---
# Runtime Rules
1. Indicator Context tayyor bo'lishi kerak.
2. Klassik indikatorlar qayta hisoblanmaydi.
3. Composite indikatorlar deterministik hisoblanadi.
4. Validation Publish'dan oldin bajariladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading
↓
Calculating
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
CustomIndicators
↓
Custom Indicator State
↓
IndicatorService
