# Breakout Strategy Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Breakout Strategy Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
Range Analysis
↓
Support / Resistance Analysis
↓
Consolidation Detection
↓
Breakout Detection
↓
Volume Confirmation
↓
Retest Analysis
↓
Breakout Confluence
↓
Generate Strategy Result
↓
StrategyManager
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Indicator Context tayyor bo'lishi kerak.
3. Breakout tasdiqlanishi kerak.
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
Breakout Strategy
↓
Strategy Result
↓
StrategyManager
