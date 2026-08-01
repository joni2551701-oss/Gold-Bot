# Wyckoff Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
Wyckoff Strategy
↓
Market Cycle Analysis
↓
Accumulation Analysis
↓
Distribution Analysis
↓
Phase Detection
↓
Spring Detection
↓
Upthrust Detection
↓
Volume Confirmation
↓
Wyckoff Confluence
↓
Generate Strategy Result
↓
StrategyEngine
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. Wyckoff qoidalari ketma-ket bajariladi.
4. Validation Result'dan oldin bajariladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading
↓
Analyzing
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
Market Context
↓
Indicator Context
↓
Wyckoff Strategy
↓
Strategy Result
↓
StrategyEngine
