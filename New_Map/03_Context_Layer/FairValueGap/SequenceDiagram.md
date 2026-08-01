# FairValueGap Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat FairValueGap modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu FairValueGap modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Market Structure
↓
Read Order Blocks
↓
Detect Bullish FVG
↓
Detect Bearish FVG
↓
Validate FVG
↓
Detect Gap Fill
↓
Detect Invalidation
↓
Generate FVG State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update FVG
↓
Update Gap Fill
↓
Update Invalidation
↓
Publish FVG State
```
---
# Runtime Rules
1. Market Structure avval tayyor bo'lishi kerak.
2. Order Block Context hisobga olinadi.
3. Validation majburiy.
4. Gap Fill uzluksiz kuzatiladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Detecting
↓
Validating
↓
Monitoring
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
FairValueGap
↓
FVG State
↓
ContextService
