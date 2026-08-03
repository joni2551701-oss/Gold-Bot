# SmartMoneyIndicators Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SmartMoneyIndicators modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu SmartMoneyIndicators modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
SmartMoneyIndicators
↓
Load Liquidity State
↓
Load Order Block State
↓
Load Fair Value Gap State
↓
Load Wyckoff State
↓
Load AMD State
↓
Calculate Liquidity Score
↓
Calculate Order Block Strength
↓
Calculate Fair Value Gap Score
↓
Calculate Imbalance Score
↓
Calculate Premium / Discount Score
↓
Calculate AMD Score
↓
Calculate Wyckoff Score
↓
Calculate Institutional Activity Score
↓
Generate Smart Money Indicator State
↓
IndicatorService
```
---
# Update Sequence
```text
Market Context Updated
↓
Update Smart Money Indicators
↓
Validate Results
↓
Publish Smart Money Indicator State
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Context qayta hisoblanmaydi.
3. Indicator'lar deterministik hisoblanadi.
4. Validation Publish'dan oldin bajariladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading
↓
Calculating
↓
Validating
↓
Publishing
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
SmartMoneyIndicators
↓
Smart Money Indicator State
↓
IndicatorService
