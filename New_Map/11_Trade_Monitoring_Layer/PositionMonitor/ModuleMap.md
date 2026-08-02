# Position Monitor Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionMonitor ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
MonitoringService
↓
PositionMonitor
↓
TradeLifecycleManager
```
---
# Module Architecture
```text
PositionMonitor
        │
        ├── Position Tracker
        ├── Synchronization Manager
        ├── State Detector
        ├── Event Generator
        ├── Position Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Position Tracker
Ochiq Position'larni kuzatadi.
---
## Synchronization Manager
Broker bilan Position holatini sinxronlaydi.
---
## State Detector
Position holatidagi o'zgarishlarni aniqlaydi.
---
## Event Generator
Position Event'larni yaratadi.
---
## Position Report Builder
Position Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ MonitoringService
✓ TradeLifecycleManager
---
# Forbidden Dependencies
✗ SLTPMonitor
✗ BreakevenManager
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
---
# Summary
PositionMonitor GoldBot Trade Monitoring Layer ichidagi barcha Position Monitoring jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
