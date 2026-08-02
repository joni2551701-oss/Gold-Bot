# ICT Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ICT Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
ICT Strategy
↓
Market Structure Analysis
↓
Liquidity Analysis
↓
Order Block Analysis
↓
Fair Value Gap Analysis
↓
Premium / Discount Analysis
↓
Session Analysis
↓
ICT Confluence
↓
Generate Strategy Result
↓
StrategyManager
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. ICT qoidalari ketma-ket bajariladi.
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
ICT Strategy
↓
Strategy Result
↓
StrategyManager
