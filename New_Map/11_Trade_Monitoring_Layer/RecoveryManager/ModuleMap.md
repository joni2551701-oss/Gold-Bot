# Recovery Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RecoveryManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PartialClose
↓
RecoveryManager
↓
Database Layer
```
---
# Module Architecture
```text
RecoveryManager
        │
        ├── Restart Detector
        ├── Position Loader
        ├── State Restorer
        ├── Recovery Validator
        ├── Recovery Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Restart Detector
Restart holatini aniqlaydi.
---
## Position Loader
Broker'dan ochiq Position'larni yuklaydi.
---
## State Restorer
Trade State va Monitoring Session'ni tiklaydi.
---
## Recovery Validator
Tiklangan ma'lumotlarni tekshiradi.
---
## Recovery Report Builder
Recovery Report yaratadi.
---
## Metadata Generator
Recovery Metadata yaratadi.
---
# Allowed Dependencies
✓ PartialClose
✓ Database Layer
---
# Forbidden Dependencies
✗ PositionMonitor
✗ TradeLifecycleManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
---
# Summary
RecoveryManager GoldBot Trade Monitoring Layer ichidagi Restart Recovery va State Restoration jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
