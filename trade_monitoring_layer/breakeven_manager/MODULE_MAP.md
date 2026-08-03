# Breakeven Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BreakevenManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
```
---
# Module Architecture
```text
BreakevenManager
        │
        ├── Rule Evaluator
        ├── Trigger Detector
        ├── Stop Loss Updater
        ├── State Manager
        ├── Break Even Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Rule Evaluator
Break Even qoidalarini tekshiradi.
---
## Trigger Detector
Break Even Trigger'ni aniqlaydi.
---
## Stop Loss Updater
Stop Loss qiymatini yangilaydi.
---
## State Manager
Break Even holatini boshqaradi.
---
## Break Even Report Builder
Break Even Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ SLTPMonitor
✓ TrailingStop
---
# Forbidden Dependencies
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
✗ Database Layer
---
# Summary
BreakevenManager GoldBot Trade Monitoring Layer ichidagi Break Even boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
