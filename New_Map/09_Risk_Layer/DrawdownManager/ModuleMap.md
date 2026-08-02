# Drawdown Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DrawdownManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
```
---
# Module Architecture
```text
DrawdownManager
        │
        ├── Equity Analyzer
        ├── Drawdown Calculator
        ├── Limit Validator
        ├── Drawdown Status Manager
        ├── Drawdown Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Equity Analyzer
Account Equity holatini tahlil qiladi.
---
## Drawdown Calculator
Current va Historical Drawdown hisoblaydi.
---
## Limit Validator
Drawdown limitlarini tekshiradi.
---
## Drawdown Status Manager
NORMAL, WARNING, LIMIT_REACHED yoki LOCKED holatini belgilaydi.
---
## Drawdown Report Builder
Yakuniy Drawdown Report yaratadi.
---
## Metadata Generator
Drawdown Metadata yaratadi.
---
# Allowed Dependencies
✓ MoneyManagement
✓ ExposureManager
---
# Forbidden Dependencies
✗ PortfolioManager
✗ RiskValidator
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
DrawdownManager GoldBot Risk Layer ichidagi Drawdown Monitoring va Capital Protection jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
