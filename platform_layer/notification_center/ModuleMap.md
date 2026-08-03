# Notification Center Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat NotificationCenter ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Internal Services
↓
NotificationCenter
↓
Platform Channels
```
---
# Module Architecture
```text
NotificationCenter
        │
        ├── Notification Receiver
        ├── Notification Validator
        ├── Priority Manager
        ├── Delivery Router
        ├── Delivery Tracker
        └── Metadata Generator
```
---
# Internal Components
## Notification Receiver
Notification Event'larni qabul qiladi.
---
## Notification Validator
Notification ma'lumotlarini tekshiradi.
---
## Priority Manager
Notification ustuvorligini belgilaydi.
---
## Delivery Router
Notification'ni kerakli platformaga yuboradi.
---
## Delivery Tracker
Yuborilish holatini kuzatadi.
---
## Metadata Generator
Notification Metadata yaratadi.
---
# Allowed Dependencies
✓ PlatformService
✓ Telegram
✓ MobileAPI
✓ WebAPI
✓ DesktopAPI
---
# Forbidden Dependencies
✗ Authentication
✗ DatabaseService
✗ AIService
✗ DecisionService
✗ ExecutionService
---
# Summary
NotificationCenter GoldBot Platform Layer ichidagi barcha Notification Delivery jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
