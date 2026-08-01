# ContextService Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextService modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ContextService modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
ContextEngine
↓
Receive Context Results
↓
Aggregate Context
↓
Validate Context
↓
Normalize Context
↓
Create Context Version
↓
Build Market Context
↓
Publish Context
↓
Indicator Layer
```
---
# Update Sequence
```text
Context Updated
↓
Rebuild Context
↓
Validate
↓
Publish New Context
```
---
# Runtime Rules
1. Barcha Context modullar yakunlanishi kerak.
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
Context Modules
↓
ContextService
↓
Market Context
↓
Indicator Layer
