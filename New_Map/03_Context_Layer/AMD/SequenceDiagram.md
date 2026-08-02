# AMD Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu AMD modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Market Structure
↓
Read Liquidity
↓
Detect Accumulation
↓
Detect Manipulation
↓
Detect Distribution
↓
Validate Phase
↓
Generate AMD State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Phase
↓
Update AMD State
↓
Publish Context
```
---
# Runtime Rules
1. Market Structure avval tayyor bo'lishi kerak.
2. Liquidity hisobga olinadi.
3. Phase ketma-ketligi tekshiriladi.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Accumulation
↓
Manipulation
↓
Distribution
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
AMD
↓
AMD State
↓
ContextService
