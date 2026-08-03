# Mobile API Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MobileAPI modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Mobile App
↓
MobileAPI
↓
Authentication
↓
PlatformService
```
---
# Module Architecture
```text
MobileAPI
        │
        ├── API Receiver
        ├── Request Validator
        ├── Navigation Manager
        ├── Push Manager
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
Mobile Navigation ma'lumotlarini boshqaradi.
---
## Push Manager
Push Notification'larni boshqaradi.
---
## Response Builder
Mobile API Response yaratadi.
---
## Metadata Generator
Mobile Metadata yaratadi.
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
MobileAPI GoldBot Platform Layer ichidagi Mobile Application Integration va API Communication jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
