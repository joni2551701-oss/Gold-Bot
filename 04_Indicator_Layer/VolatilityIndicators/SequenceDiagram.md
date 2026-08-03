# VolatilityIndicators Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolatilityIndicators modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu VolatilityIndicators modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
VolatilityIndicators
↓
Load Price Data
↓
Calculate ATR
↓
Calculate Bollinger Bands
↓
Calculate Keltner Channel
↓
Calculate Donchian Channel
↓
Calculate Standard Deviation
↓
Calculate Volatility Score
↓
Generate Volatility Indicator State
↓
IndicatorService
```
---
# Update Sequence
```text
New Candle
↓
Update Volatility Indicators
↓
Validate Results
↓
Publish Volatility Indicator State
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
VolatilityIndicators
↓
Volatility Indicator State
↓
IndicatorService
