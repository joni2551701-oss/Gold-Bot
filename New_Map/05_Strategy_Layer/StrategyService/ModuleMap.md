# Strategy Service Module Map
Status: CANONICAL
---
# Module Position
```text
Signal Layer
↓
StrategyService
↓
StrategyEngine
```
---
# Module Architecture
```text
StrategyService
        │
        ├── Request Handler
        ├── Request Validator
        ├── Engine Dispatcher
        ├── Result Handler
        ├── Event Publisher
        ├── Status Manager
        └── Response Builder
```
---
# Internal Components
## Request Handler
Strategy so'rovlarini qabul qiladi.
---
## Request Validator
So'rovni tekshiradi.
---
## Engine Dispatcher
So'rovni StrategyEngine'ga uzatadi.
---
## Result Handler
Strategy natijasini qabul qiladi.
---
## Event Publisher
Strategy Event yaratadi.
---
## Status Manager
Service holatini boshqaradi.
---
## Response Builder
Yakuniy javobni tayyorlaydi.
---
# Allowed Dependencies
✓ StrategyEngine
✓ StrategyManager
✓ StrategyLibrary
✓ StrategyProfiles
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
StrategyService GoldBot Strategy Layer uchun tashqi Service API vazifasini bajaradi.
