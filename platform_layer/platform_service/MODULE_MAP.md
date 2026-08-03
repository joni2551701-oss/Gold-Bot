# Platform Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PlatformService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Platform Channels
↓
PlatformService
↓
Internal Services
```
---
# Module Architecture
```text
PlatformService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Route Manager
        ├── Session Coordinator
        ├── Response Formatter
        └── Metadata Generator
```
---
# Internal Components
## Request Receiver
Platform Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Route Manager
Request'ni tegishli Service'ga yo'naltiradi.
---
## Session Coordinator
Platform Session'ni boshqaradi.
---
## Response Formatter
Javobni standart formatga o'tkazadi.
---
## Metadata Generator
Platform Metadata yaratadi.
---
# Allowed Dependencies
✓ Authentication
✓ DatabaseService
✓ AIService
✓ DecisionService
✓ RiskService
✓ ExecutionService
✓ MonitoringService
---
# Forbidden Dependencies
✗ Telegram
✗ MobileAPI
✗ WebAPI
✗ DesktopAPI
---
# Summary
PlatformService Platform Layer ichidagi barcha Service Routing va Platform Coordination'ni boshqaruvchi Canonical Gateway modulidir.
