# SMC Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SMC Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
SMC Strategy
↓
Market Structure Analysis
↓
BOS Analysis
↓
CHoCH Analysis
↓
Liquidity Analysis
↓
Order Block Analysis
↓
Fair Value Gap Analysis
↓
Imbalance Analysis
↓
Premium / Discount Analysis
↓
SMC Confluence
↓
Generate Execution Output
↓
StrategyEngine
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. SMC qoidalari ketma-ket bajariladi.
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
SMC Strategy
↓
Execution Output
↓
StrategyEngine
