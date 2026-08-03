# ContextEngine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextEngine modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ContextEngine modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
Market Data
↓
ContextEngine
↓
Initialize Context Pipeline
↓
Run MarketStructure
↓
Run Liquidity
↓
Run OrderBlock
↓
Run FairValueGap
↓
Run Wyckoff
↓
Run AMD
↓
Run Session
↓
Run Trend
↓
Run VolumeProfile
↓
Aggregate Results
↓
Validate Context
↓
Build Market Context
↓
ContextService
```
---
# Runtime Request Sequence
```text
Context Request
↓
ContextEngine
↓
Dispatch Context Modules
↓
Collect Results
↓
Build Context
↓
Return Market Context
```
---
# Failure Sequence
```text
Context Module Failure
↓
Capture Error
↓
Generate Context Event
↓
Continue Remaining Modules
↓
Build Partial Context
↓
Report Status
```
---
# Runtime Rules
1. Context modullar ketma-ket ishlaydi.
2. Har bir modul mustaqil natija yaratadi.
3. ContextEngine barcha natijalarni yig'adi.
4. Validation Context build'dan oldin bajariladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Running
↓
Aggregating
↓
Validating
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence
Market Data
↓
ContextEngine
↓
Context Modules
↓
Market Context
↓
ContextService
