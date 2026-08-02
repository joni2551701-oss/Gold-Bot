# Liquidity Sweep Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity Sweep Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
Liquidity Pool Analysis
↓
Equal High / Equal Low Detection
↓
Stop Hunt Detection
↓
False Breakout Detection
↓
Sweep Confirmation
↓
Rejection Analysis
↓
Liquidity Confluence
↓
Generate Execution Output
↓
StrategyEngine
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. Liquidity bosqichlari ketma-ket bajariladi.
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
Liquidity Sweep Strategy
↓
Execution Output
↓
StrategyEngine
