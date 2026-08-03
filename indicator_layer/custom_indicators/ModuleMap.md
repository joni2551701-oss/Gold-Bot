# CustomIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat CustomIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
CustomIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
CustomIndicators
        │
        ├── Composite Score Calculator
        ├── Market Confidence Calculator
        ├── Liquidity Pressure Calculator
        ├── Institutional Strength Calculator
        ├── Smart Trend Calculator
        ├── Risk Environment Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## Composite Score Calculator
Yagona Composite Market Score yaratadi.
---
## Market Confidence Calculator
Bozor ishonchlilik indeksini hisoblaydi.
---
## Liquidity Pressure Calculator
Liquidity bosimini baholaydi.
---
## Institutional Strength Calculator
Institutional faollik darajasini baholaydi.
---
## Smart Trend Calculator
GoldBot Smart Trend indeksini yaratadi.
---
## Risk Environment Calculator
Bozor xavf muhitini baholaydi.
---
## Validation Manager
Natijalarni tekshiradi.
---
## State Manager
Custom Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
Indicator Modules
↓
CustomIndicators
↓
IndicatorService
```
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Indicator Context
✓ IndicatorService
✓ Event System
---
# Forbidden Dependencies
✗ Context Layer (calculation)
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
CustomIndicators egalik qiladi.
✓ Composite Market Score
✓ Market Confidence Index
✓ Liquidity Pressure Index
✓ Institutional Strength Index
✓ Smart Trend Index
✓ Risk Environment Index
✓ Custom Indicator State
---
# Module Rules
1. Proprietary indikatorlar faqat mavjud indikatorlar asosida hisoblanadi.
2. Klassik indikatorlar o'zgartirilmaydi.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
CustomIndicators GoldBot Indicator Layer ichidagi proprietary Indicator Calculation moduli hisoblanadi.
