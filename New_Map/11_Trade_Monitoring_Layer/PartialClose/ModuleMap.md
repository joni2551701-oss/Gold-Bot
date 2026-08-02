# Partial Close Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PartialClose ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
TrailingStop
↓
PartialClose
↓
RecoveryManager
```
---
# Module Architecture
```text
PartialClose
        │
        ├── Rule Evaluator
        ├── Volume Calculator
        ├── Position Updater
        ├── State Manager
        ├── Partial Close Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Rule Evaluator
Partial Close qoidalarini tekshiradi.
---
## Volume Calculator
Yopiladigan Volume'ni hisoblaydi.
---
## Position Updater
Position hajmini yangilaydi.
---
## State Manager
Partial Close holatini boshqaradi.
---
## Partial Close Report Builder
Partial Close Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ TrailingStop
✓ RecoveryManager
---
# Forbidden Dependencies
✗ PositionMonitor
✗ TradeLifecycleManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
---
# Summary
PartialClose GoldBot Trade Monitoring Layer ichidagi Partial Position Management jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
