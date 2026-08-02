# AMD Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
AMD Strategy
↓
Accumulation Analysis
↓
Manipulation Analysis
↓
Liquidity Sweep Detection
↓
Distribution Analysis
↓
Expansion Analysis
↓
AMD Confluence
↓
Generate Execution Output
↓
StrategyEngine
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. AMD bosqichlari ketma-ket bajariladi.
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
AMD Strategy
↓
Execution Output
↓
StrategyEngine
