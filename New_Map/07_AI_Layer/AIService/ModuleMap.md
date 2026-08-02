# AI Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
External Layers
↓
AIService
↓
AIEngine
↓
AICoordinator
```
---
# Module Architecture
```text
AIService
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
AI so'rovlarini qabul qiladi.
---
## Request Validator
So'rov formatini tekshiradi.
---
## Session Manager
AI Session holatini boshqaradi.
---
## Request Dispatcher
Request'ni AIEngine'ga uzatadi.
---
## Response Formatter
AI javobini standart formatga o'tkazadi.
---
## Service Monitor
Service holati va ishlashini kuzatadi.
---
# Allowed Dependencies
✓ AIEngine
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
AIService GoldBot AI Layer uchun yagona Service Gateway va Public API moduli hisoblanadi.
