# Risk Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
RiskService
↓
RiskEngine
↓
PositionSizing
```
---
# Module Architecture
```text
RiskEngine
        │
        ├── Input Validator
        ├── Account Analyzer
        ├── Context Builder
        ├── Risk Aggregator
        ├── Risk Package Builder
        └── Metadata Generator
```
---
# Internal Components
## Input Validator
Validated Risk Request va Account ma'lumotlarini tekshiradi.
---
## Account Analyzer
Balans, Equity va Margin holatini tahlil qiladi.
---
## Context Builder
Risk Context yaratadi.
---
## Risk Aggregator
Risk bilan bog'liq barcha ma'lumotlarni yig'adi.
---
## Risk Package Builder
Keyingi modullar uchun Risk Package yaratadi.
---
## Metadata Generator
Risk Metadata yaratadi.
---
# Allowed Dependencies
✓ RiskService
✓ PositionSizing
✓ MoneyManagement
---
# Forbidden Dependencies
✗ Decision Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
RiskEngine GoldBot Risk Layer ichidagi barcha Risk Assessment jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
