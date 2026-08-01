# TrendIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrendIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
TrendIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
TrendIndicators
        │
        ├── EMA Calculator
        ├── SMA Calculator
        ├── WMA Calculator
        ├── HMA Calculator
        ├── SuperTrend Calculator
        ├── Ichimoku Calculator
        ├── Trend Strength Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## EMA Calculator
Exponential Moving Average hisoblaydi.
---
## SMA Calculator
Simple Moving Average hisoblaydi.
---
## WMA Calculator
Weighted Moving Average hisoblaydi.
---
## HMA Calculator
Hull Moving Average hisoblaydi.
---
## SuperTrend Calculator
SuperTrend indikatorini hisoblaydi.
---
## Ichimoku Calculator
Ichimoku Cloud komponentlarini hisoblaydi.
---
## Trend Strength Calculator
Trend kuchini baholaydi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Trend Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
TrendIndicators
↓
IndicatorService
```
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Market Context
✓ IndicatorService
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Ownership
TrendIndicators egalik qiladi.
✓ EMA
✓ SMA
✓ WMA
✓ HMA
✓ SuperTrend
✓ Ichimoku
✓ Trend Strength
✓ Trend Indicator State
---
# Module Rules
1. Har bir indikator mustaqil hisoblanadi.
2. Trend Strength barcha indikatorlardan foydalanishi mumkin.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
TrendIndicators GoldBot Indicator Layer ichidagi Trend Indicator Calculation modulidir.
