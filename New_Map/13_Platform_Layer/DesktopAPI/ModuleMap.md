# Desktop API Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DesktopAPI modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Desktop Client
↓
DesktopAPI
↓
Authentication
↓
PlatformService
```
---
# Module Architecture
```text
DesktopAPI
        │
        ├── API Receiver
        ├── Request Validator
        ├── Navigation Manager
        ├── Real-Time Manager
        ├── Response Builder
        └── Metadata Generator
```
---
# Internal Components
## API Receiver
REST va WebSocket Request'larni qabul qiladi.
---
## Request Validator
API Request formatini tekshiradi.
---
## Navigation Manager
Desktop Navigation va UI ma'lumotlarini boshqaradi.
---
## Real-Time Manager
Live Event va Real-Time Update'larni boshqaradi.
---
## Response Builder
Desktop API Response yaratadi.
---
## Metadata Generator
Desktop Metadata yaratadi.
---
# Allowed Dependencies
✓ Authentication
✓ PlatformService
✓ NotificationCenter
---
# Forbidden Dependencies
✗ DatabaseService
✗ AIService
✗ DecisionService
✗ RiskService
✗ ExecutionService
✗ MonitoringService
---
# Summary
DesktopAPI GoldBot Platform Layer ichidagi Desktop Client Integration va API Communication jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
