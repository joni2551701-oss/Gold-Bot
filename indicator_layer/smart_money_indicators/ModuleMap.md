# SmartMoneyIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SmartMoneyIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
SmartMoneyIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
SmartMoneyIndicators
        │
        ├── Liquidity Score Calculator
        ├── Order Block Strength Calculator
        ├── Fair Value Gap Score Calculator
        ├── Imbalance Score Calculator
        ├── Premium / Discount Calculator
        ├── AMD Score Calculator
        ├── Wyckoff Score Calculator
        ├── Institutional Activity Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## Liquidity Score Calculator
Liquidity sifatini baholaydi.
---
## Order Block Strength Calculator
Order Block kuchini baholaydi.
---
## Fair Value Gap Score Calculator
FVG sifatini baholaydi.
---
## Imbalance Score Calculator
Imbalance kuchini baholaydi.
---
## Premium / Discount Calculator
Premium va Discount holatini baholaydi.
---
## AMD Score Calculator
AMD holatini baholaydi.
---
## Wyckoff Score Calculator
Wyckoff holatini baholaydi.
---
## Institutional Activity Calculator
Institutional Activity Score yaratadi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Smart Money Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
SmartMoneyIndicators
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
SmartMoneyIndicators egalik qiladi.
✓ Liquidity Score
✓ Order Block Strength
✓ Fair Value Gap Score
✓ Imbalance Score
✓ Premium / Discount Score
✓ AMD Score
✓ Wyckoff Score
✓ Institutional Activity Score
✓ Smart Money Indicator State
---
# Module Rules
1. Context qayta hisoblanmaydi.
2. Faqat indikatorlar hisoblanadi.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
SmartMoneyIndicators GoldBot Indicator Layer ichidagi Smart Money Indicator Calculation moduli hisoblanadi.
