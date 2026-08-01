# VolumeProfile Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolumeProfile modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu VolumeProfile modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Volume Data
↓
Build Volume Profile
↓
Calculate POC
↓
Calculate Value Area
↓
Detect VAH
↓
Detect VAL
↓
Detect HVN
↓
Detect LVN
↓
Generate Volume Profile State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Volume
↓
Rebuild Profile
↓
Update POC
↓
Publish Volume Profile State
```
---
# Runtime Rules
1. Volume Data mavjud bo'lishi shart.
2. Profile birinchi yaratiladi.
3. POC Profile'dan hisoblanadi.
4. Value Area POC asosida aniqlanadi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading
↓
Building Profile
↓
Calculating
↓
Ready
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
Volume Profile
↓
Volume Profile State
↓
ContextService
