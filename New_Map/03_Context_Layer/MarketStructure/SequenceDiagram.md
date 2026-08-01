# MarketStructure Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketStructure modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu MarketStructure modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
MarketStructure
↓
Detect Swing High
↓
Detect Swing Low
↓
Build Structure
↓
Detect BOS
↓
Detect CHoCH
↓
Detect MSS
↓
Generate Structure State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
MarketStructure
↓
Update Swings
↓
Update Structure
↓
Publish Structure State
```
---
# Runtime Rules
1. Swing birinchi aniqlanadi.
2. Structure keyin quriladi.
3. BOS Structure'dan keyin tekshiriladi.
4. CHoCH BOS'dan keyin tekshiriladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Swing Detection
↓
Structure Analysis
↓
Structure Ready
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
Swing Detection
↓
Market Structure
↓
ContextService
