# Web API Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat WebAPI modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Web Dashboard
↓
WebAPI
↓
Authentication
↓
PlatformService
```
---
# Module Architecture
```text
WebAPI
        │
        ├── API Receiver
        ├── Request Validator
        ├── Dashboard Manager
        ├── WebSocket Manager
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
## Dashboard Manager
Dashboard Navigation va UI ma'lumotlarini boshqaradi.
---
## WebSocket Manager
Real-Time Event va Live Update'larni boshqaradi.
---
## Response Builder
Web API Response yaratadi.
---
## Metadata Generator
Web Metadata yaratadi.
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
WebAPI GoldBot Platform Layer ichidagi Web Dashboard Integration va API Communication jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
