# VolumeIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolumeIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
VolumeIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
VolumeIndicators
        │
        ├── VWAP Calculator
        ├── VWMA Calculator
        ├── OBV Calculator
        ├── MFI Calculator
        ├── CMF Calculator
        ├── A/D Line Calculator
        ├── Volume Strength Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## VWAP Calculator
Volume Weighted Average Price hisoblaydi.
---
## VWMA Calculator
Volume Weighted Moving Average hisoblaydi.
---
## OBV Calculator
On Balance Volume hisoblaydi.
---
## MFI Calculator
Money Flow Index hisoblaydi.
---
## CMF Calculator
Chaikin Money Flow hisoblaydi.
---
## A/D Line Calculator
Accumulation/Distribution Line hisoblaydi.
---
## Volume Strength Calculator
Volume kuchini baholaydi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Volume Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
VolumeIndicators
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
VolumeIndicators egalik qiladi.
✓ VWAP
✓ VWMA
✓ OBV
✓ MFI
✓ CMF
✓ A/D Line
✓ Volume Strength
✓ Volume Indicator State
---
# Module Rules
1. Har bir indikator mustaqil hisoblanadi.
2. Volume Strength barcha indikatorlardan foydalanishi mumkin.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
VolumeIndicators GoldBot Indicator Layer ichidagi Volume Indicator Calculation moduli hisoblanadi.
