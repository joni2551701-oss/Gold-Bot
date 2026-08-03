# Exposure Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExposureManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
```
---
# Module Architecture
```text
ExposureManager
        │
        ├── Position Analyzer
        ├── Pending Order Analyzer
        ├── Symbol Exposure Calculator
        ├── Direction Exposure Calculator
        ├── Exposure Validator
        ├── Exposure Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Position Analyzer
Ochiq pozitsiyalarni tahlil qiladi.
---
## Pending Order Analyzer
Pending Orderlarni hisobga oladi.
---
## Symbol Exposure Calculator
Har bir instrument bo'yicha Exposure hisoblaydi.
---
## Direction Exposure Calculator
BUY va SELL yo'nalishlari bo'yicha Exposure hisoblaydi.
---
## Exposure Validator
Exposure limitlarini tekshiradi.
---
## Exposure Report Builder
Yakuniy Exposure Report yaratadi.
---
## Metadata Generator
Exposure Metadata yaratadi.
---
# Allowed Dependencies
✓ DrawdownManager
✓ PortfolioManager
---
# Forbidden Dependencies
✗ RiskValidator
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
ExposureManager GoldBot Risk Layer ichidagi Exposure Monitoring va Exposure Validation jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
