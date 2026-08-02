# SLTP Monitor Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SLTPMonitor ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
```
---
# Module Architecture
```text
SLTPMonitor
        │
        ├── Price Tracker
        ├── Stop Loss Detector
        ├── Take Profit Detector
        ├── Trigger Validator
        ├── Monitoring Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Price Tracker
Bozor narxini kuzatadi.
---
## Stop Loss Detector
SL Trigger'ni aniqlaydi.
---
## Take Profit Detector
TP Trigger'ni aniqlaydi.
---
## Trigger Validator
Trigger haqiqiyligini tekshiradi.
---
## Monitoring Report Builder
Monitoring Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ TradeLifecycleManager
✓ BreakevenManager
---
# Forbidden Dependencies
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
✗ Decision Layer
---
# Summary
SLTPMonitor GoldBot Trade Monitoring Layer ichidagi Stop Loss va Take Profit Monitoring jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
