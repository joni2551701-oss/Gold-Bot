# Wyckoff Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Wyckoff modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Market Structure
↓
Read Liquidity
↓
Detect Market Phase
↓
Detect Spring
↓
Detect Upthrust
↓
Detect SOS
↓
Detect SOW
↓
Generate Wyckoff State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Market Phase
↓
Update Wyckoff Events
↓
Publish Wyckoff State
```
---
# Runtime Rules
1. Market Structure avval tayyor bo'lishi kerak.
2. Liquidity hisobga olinadi.
3. Market Phase birinchi aniqlanadi.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Phase Detection
↓
Event Detection
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
Wyckoff
↓
Wyckoff State
↓
ContextService
