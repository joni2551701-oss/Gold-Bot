# Liquidity Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Liquidity modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Liquidity
↓
Read Market Structure
↓
Detect Equal High
↓
Detect Equal Low
↓
Build Liquidity Pools
↓
Detect Liquidity Sweep
↓
Detect Liquidity Grab
↓
Generate Liquidity State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Liquidity
↓
Update Pools
↓
Update Sweeps
↓
Publish Liquidity State
```
---
# Runtime Rules
1. Market Structure avval tayyor bo'lishi kerak.
2. Equal High/Low birinchi aniqlanadi.
3. Liquidity Pool keyin yaratiladi.
4. Sweep va Grab oxirida tekshiriladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Liquidity Detection
↓
Pool Analysis
↓
Sweep Detection
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
Liquidity
↓
Liquidity State
↓
ContextService
