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
---
# Forbidden Dependencies
✗ StrategyManager (to'g'ridan-to'g'ri)
✗ StrategyLibrary (to'g'ridan-to'g'ri)
✗ StrategyProfiles (to'g'ridan-to'g'ri)
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Summary
StrategyService GoldBot Strategy Layer uchun tashqi Service API vazifasini bajaradi.
