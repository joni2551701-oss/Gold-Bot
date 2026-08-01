# Trend Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trend modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Trend modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Market Structure
↓
Read Session
↓
Detect Primary Trend
↓
Detect Secondary Trend
↓
Analyze Trend Strength
↓
Detect Premium / Discount
↓
Generate Trend State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Market Structure
↓
Update Trend
↓
Publish Trend State
```
---
# Runtime Rules
1. Market Structure tayyor bo'lishi shart.
2. Trend har doim Structure asosida aniqlanadi.
3. Premium / Discount Trend bilan birga hisoblanadi.
4. Trend State uzluksiz yangilanadi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Trend Detection
↓
Trend Analysis
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
Trend
↓
Trend State
↓
ContextService
