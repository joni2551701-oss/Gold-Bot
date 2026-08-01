# Signal Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Signal Formatter
↓
SignalService
↓
AI Layer
```
---
# Module Architecture
```text
SignalService
        │
        ├── Request Handler
        ├── Request Validator
        ├── Signal Repository
        ├── Response Builder
        ├── Event Publisher
        ├── Status Manager
        └── Service Gateway
```
---
# Internal Components
## Request Handler
Signal so'rovlarini qabul qiladi.
---
## Request Validator
Signal so'rovini tekshiradi.
---
## Signal Repository
Signal Result'ni yuklaydi.
---
## Response Builder
Signal javobini yaratadi.
---
## Event Publisher
Signal Event yaratadi.
---
## Status Manager
Signal holatini boshqaradi.
---
## Service Gateway
Keyingi Layer bilan aloqani boshqaradi.
---
# Allowed Dependencies
✓ SignalFormatter
✓ Event System
✓ Signal Model
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
SignalService GoldBot Signal Layer uchun tashqi Service API vazifasini bajaruvchi Canonical Service modulidir.
