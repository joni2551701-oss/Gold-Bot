# Risk Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Decision Layer
↓
RiskService (Entry)
↓
RiskEngine
↓
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
↓
RiskValidator
↓
RiskService (Exit)
↓
Execution Layer
```
---
# Module Architecture
```text
RiskService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Session Manager
        ├── Request Dispatcher
        ├── Response Formatter
        └── Service Monitor
```
---
# Internal Components
## Request Receiver
Decision Layer'dan Risk Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Risk Session holatini boshqaradi.
---
## Request Dispatcher
RiskEngine'ga so'rov yuboradi.
---
## Response Formatter
RiskValidator'dan qaytgan Risk Approval'ni standart formatga o'tkazadi va Execution Layer'ga uzatadi.
---
## Service Monitor
RiskService holatini kuzatadi.
---
# Allowed Dependencies
✓ RiskEngine
✓ RiskValidator
---
# Forbidden Dependencies
✗ PositionSizing (to'g'ridan-to'g'ri)
✗ MoneyManagement (to'g'ridan-to'g'ri)
✗ DrawdownManager (to'g'ridan-to'g'ri)
✗ ExposureManager (to'g'ridan-to'g'ri)
✗ PortfolioManager (to'g'ridan-to'g'ri)
✗ Database Layer
✗ Platform Layer
✗ DecisionEngine
---
# Summary
RiskService GoldBot Risk Layer uchun ikki tomonlama Boundary Gateway va Public API modulidir.
