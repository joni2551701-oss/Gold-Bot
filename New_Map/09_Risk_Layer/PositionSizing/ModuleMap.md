# Position Sizing Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionSizing ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
RiskEngine
↓
PositionSizing
↓
MoneyManagement
```
---
# Module Architecture
```text
PositionSizing
        │
        ├── Risk Amount Calculator
        ├── Position Calculator
        ├── Lot Calculator
        ├── Symbol Validator
        ├── Position Package Builder
        └── Metadata Generator
```
---
# Internal Components
## Risk Amount Calculator
Pul ko'rinishidagi Risk Amount hisoblaydi.
---
## Position Calculator
Nazariy Position Size hisoblaydi.
---
## Lot Calculator
Broker uchun yakuniy Lot Size hisoblaydi.
---
## Symbol Validator
Min Lot, Max Lot va Volume Step'ni tekshiradi.
---
## Position Package Builder
MoneyManagement uchun Position Package yaratadi.
---
## Metadata Generator
Position Metadata yaratadi.
---
# Allowed Dependencies
✓ RiskEngine
✓ MoneyManagement
---
# Forbidden Dependencies
✗ DrawdownManager
✗ ExposureManager
✗ PortfolioManager
✗ Execution Layer
---
# Summary
PositionSizing GoldBot Risk Layer ichidagi barcha Position Size Calculation jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
