# IndicatorEngine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorEngine modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu IndicatorEngine modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
IndicatorEngine
↓
Load Configuration
↓
Resolve Dependencies
        │
        ├──────── Execute Trend Indicators
        ├──────── Execute Momentum Indicators
        ├──────── Execute Volatility Indicators
        └──────── Execute Volume Indicators
                 │
                 ▼
          Synchronization Point
                 │
                 ▼
      Execute MarketStructure Indicators
                 │
                 ▼
      Execute SmartMoney Indicators
                 │
                 ▼
         Execute Custom Indicators
                 │
                 ▼
           Validate Results
                 │
                 ▼
            IndicatorService
                 │
                 ▼
           Indicator Context
```
---
# Update Sequence
```text
Market Context Updated
↓
Restart Pipeline
↓
Recalculate Indicators
↓
Publish Indicator Context
```
---
# Runtime Rules
1. Market Context tayyor bo'lishi kerak.
2. Dependency tekshiriladi.
3. Trend, Momentum, Volatility, Volume Indicators bir-birining natijasiga bog'liq emas va parallel ishga tushadi.
4. MarketStructure, SmartMoney, Custom Indicators Synchronization Point'dan keyin ketma-ket ishga tushadi.
5. Validation Publish'dan oldin bajariladi.
6. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Resolving Dependencies
↓
Executing
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
IndicatorEngine
↓
Indicator Modules
↓
IndicatorService
↓
Indicator Context
