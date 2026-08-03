# MomentumIndicators Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MomentumIndicators modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu MomentumIndicators modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
MomentumIndicators
↓
Load Price Data
↓
Calculate RSI
↓
Calculate Stochastic
↓
Calculate CCI
↓
Calculate ROC
↓
Calculate Momentum
↓
Calculate MACD Histogram
↓
Calculate Momentum Strength
↓
Generate Momentum Indicator State
↓
IndicatorService
```
---
# Update Sequence
```text
New Candle
↓
Update Momentum Indicators
↓
Validate Results
↓
Publish Momentum Indicator State
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. OHLC Data tekshiriladi.
3. Indikatorlar ketma-ket hisoblanadi.
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
MomentumIndicators
↓
Momentum Indicator State
↓
IndicatorService
