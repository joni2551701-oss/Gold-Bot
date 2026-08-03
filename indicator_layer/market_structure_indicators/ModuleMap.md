# MarketStructureIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketStructureIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
MarketStructureIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
MarketStructureIndicators
        │
        ├── Swing Strength Calculator
        ├── BOS Strength Calculator
        ├── CHoCH Strength Calculator
        ├── MSS Strength Calculator
        ├── Trend Quality Calculator
        ├── Breakout Quality Calculator
        ├── Range Quality Calculator
        ├── Structure Score Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## Swing Strength Calculator
Swing kuchini baholaydi.
---
## BOS Strength Calculator
Break of Structure sifatini baholaydi.
---
## CHoCH Strength Calculator
Change of Character kuchini baholaydi.
---
## MSS Strength Calculator
Market Structure Shift kuchini baholaydi.
---
## Trend Quality Calculator
Structure asosidagi trend sifatini hisoblaydi.
---
## Breakout Quality Calculator
Breakout sifatini hisoblaydi.
---
## Range Quality Calculator
Range sifatini hisoblaydi.
---
## Structure Score Calculator
Yagona Structure Score yaratadi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Structure Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
MarketStructureIndicators
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
MarketStructureIndicators egalik qiladi.
✓ Swing Strength
✓ BOS Strength
✓ CHoCH Strength
✓ MSS Strength
✓ Trend Quality
✓ Breakout Quality
✓ Range Quality
✓ Structure Score
✓ Structure Indicator State
---
# Module Rules
1. Market Structure qayta hisoblanmaydi.
2. Faqat indikatorlar hisoblanadi.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
MarketStructureIndicators GoldBot Indicator Layer ichidagi Market Structure Indicator Calculation moduli hisoblanadi.
