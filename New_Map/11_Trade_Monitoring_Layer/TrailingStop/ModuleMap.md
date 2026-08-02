# Trailing Stop Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrailingStop ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
BreakevenManager
↓
TrailingStop
↓
PartialClose
```
---
# Module Architecture
```text
TrailingStop
        │
        ├── Rule Evaluator
        ├── Price Tracker
        ├── Stop Loss Calculator
        ├── State Manager
        ├── Trailing Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Rule Evaluator
Trailing qoidalarini tekshiradi.
---
## Price Tracker
Bozor narxini kuzatadi.
---
## Stop Loss Calculator
Yangi Stop Loss qiymatini hisoblaydi.
---
## State Manager
Trailing holatini boshqaradi.
---
## Trailing Report Builder
Trailing Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ BreakevenManager
✓ PartialClose
---
# Forbidden Dependencies
✗ RecoveryManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
✗ Database Layer
---
# Summary
TrailingStop GoldBot Trade Monitoring Layer ichidagi Dynamic Stop Loss boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
