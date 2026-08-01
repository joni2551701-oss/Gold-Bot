# MomentumIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MomentumIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
MomentumIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
MomentumIndicators
        │
        ├── RSI Calculator
        ├── Stochastic Calculator
        ├── CCI Calculator
        ├── ROC Calculator
        ├── Momentum Calculator
        ├── MACD Histogram Calculator
        ├── Momentum Strength Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## RSI Calculator
Relative Strength Index hisoblaydi.
---
## Stochastic Calculator
Stochastic Oscillator hisoblaydi.
---
## CCI Calculator
Commodity Channel Index hisoblaydi.
---
## ROC Calculator
Rate of Change hisoblaydi.
---
## Momentum Calculator
Momentum qiymatini hisoblaydi.
---
## MACD Histogram Calculator
MACD Histogram hisoblaydi.
---
## Momentum Strength Calculator
Momentum kuchini baholaydi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Momentum Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
MomentumIndicators
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
MomentumIndicators egalik qiladi.
✓ RSI
✓ Stochastic
✓ CCI
✓ ROC
✓ Momentum
✓ MACD Histogram
✓ Momentum Strength
✓ Momentum Indicator State
---
# Module Rules
1. Har bir indikator mustaqil hisoblanadi.
2. Momentum Strength barcha indikatorlardan foydalanishi mumkin.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
MomentumIndicators GoldBot Indicator Layer ichidagi Momentum Indicator Calculation moduli hisoblanadi.
