# Execution Monitor Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionMonitor ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
BrokerGateway
↓
ExecutionMonitor
↓
Trade Monitoring Layer
```
---
# Module Architecture
```text
ExecutionMonitor
        │
        ├── Status Tracker
        ├── Fill Detector
        ├── Partial Fill Tracker
        ├── Timeout Detector
        ├── Retry Manager
        ├── Execution Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Status Tracker
Order Status o'zgarishlarini kuzatadi.
---
## Fill Detector
To'liq bajarilgan Order'larni aniqlaydi.
---
## Partial Fill Tracker
Qisman bajarilgan Order'larni kuzatadi.
---
## Timeout Detector
Execution Timeout holatini aniqlaydi.
---
## Retry Manager
Retry kerakligini aniqlaydi.
---
## Execution Report Builder
Execution Report yaratadi.
---
## Metadata Generator
Monitoring Metadata yaratadi.
---
# Allowed Dependencies
✓ BrokerGateway
✓ Trade Monitoring Layer
---
# Forbidden Dependencies
✗ OrderValidator
✗ OrderManager
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
ExecutionMonitor GoldBot Execution Layer ichidagi barcha Execution Event va Status Monitoring jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
