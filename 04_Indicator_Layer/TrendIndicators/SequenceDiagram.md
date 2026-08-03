# TrendIndicators Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrendIndicators modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu TrendIndicators modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
TrendIndicators
↓
Load Price Data
↓
Calculate EMA
↓
Calculate SMA
↓
Calculate WMA
↓
Calculate HMA
↓
Calculate SuperTrend
↓
Calculate Ichimoku
↓
Calculate Trend Strength
↓
Generate Trend Indicator State
↓
IndicatorService
```
---
# Update Sequence
```text
New Candle
↓
Update Trend Indicators
↓
Validate Results
↓
Publish Trend Indicator State
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
TrendIndicators
↓
Trend Indicator State
↓
IndicatorService
