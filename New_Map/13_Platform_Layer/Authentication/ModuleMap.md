# Authentication Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Authentication ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Platform
↓
Authentication
↓
PlatformService
↓
DatabaseService
```
---
# Module Architecture
```text
Authentication
        │
        ├── Register Manager
        ├── Login Manager
        ├── Session Manager
        ├── Token Manager
        ├── Access Controller
        └── Metadata Generator
```
---
# Internal Components
## Register Manager
Yangi foydalanuvchini ro'yxatdan o'tkazadi va User ID yaratadi.
---
## Login Manager
Login jarayonini boshqaradi.
---
## Session Manager
Session yaratadi va boshqaradi.
---
## Token Manager
Access Token yaratadi va tekshiradi.
---
## Access Controller
Role va Permission'larni tekshiradi.
---
## Metadata Generator
Authentication Metadata yaratadi.
---
# Allowed Dependencies
✓ PlatformService
✓ DatabaseService
---
# Forbidden Dependencies
✗ AIService
✗ DecisionService
✗ RiskService
✗ ExecutionService
✗ MonitoringService
✗ Telegram (to'g'ridan-to'g'ri)
✗ MobileAPI (to'g'ridan-to'g'ri)
✗ WebAPI (to'g'ridan-to'g'ri)
✗ DesktopAPI (to'g'ridan-to'g'ri)
✗ NotificationCenter
---
# Summary
Authentication GoldBot Platform Layer ichidagi Identity va Access Management jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
