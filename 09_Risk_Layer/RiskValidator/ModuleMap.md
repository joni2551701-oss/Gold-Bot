# Risk Validator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskValidator ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PortfolioManager
↓
RiskValidator
↓
RiskService
```
---
# Module Architecture
```text
RiskValidator
        │
        ├── Report Aggregator
        ├── Policy Validator
        ├── Approval Evaluator
        ├── Reject Reason Builder
        ├── Validation Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Report Aggregator
Barcha Risk Reportlarni yig'adi.
---
## Policy Validator
Risk Policy va cheklovlarni tekshiradi.
---
## Approval Evaluator
APPROVED, REJECTED, REDUCE yoki BLOCKED holatini belgilaydi.
---
## Reject Reason Builder
Risk rad etilish sabablarini yaratadi.
---
## Validation Report Builder
Yakuniy Risk Validation Report yaratadi.
---
## Metadata Generator
Risk Validation Metadata yaratadi.
---
# Allowed Dependencies
✓ PortfolioManager
✓ RiskService
---
# Forbidden Dependencies
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
RiskValidator GoldBot Risk Layer ichidagi barcha Risk Validation jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
