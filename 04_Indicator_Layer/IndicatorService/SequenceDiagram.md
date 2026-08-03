# IndicatorService Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorService modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu IndicatorService modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
IndicatorEngine
↓
Receive Indicator Results
↓
Aggregate Indicators
↓
Validate Indicator Context
↓
Normalize Indicator Context
↓
Create Version
↓
Build Indicator Context
↓
Publish
↓
Strategy Layer
```
---
# Update Sequence
```text
Indicator Updated
↓
Rebuild Indicator Context
↓
Validate
↓
Publish New Indicator Context
```
---
# Runtime Rules
1. Barcha Indicator modullari yakunlanishi kerak.
2. Validation Aggregation'dan keyin bajariladi.
3. Publish oxirgi bosqich hisoblanadi.
4. Har bir Context yangi Version oladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Aggregating
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
Indicator Modules
↓
IndicatorService
↓
Indicator Context
↓
Strategy Layer
