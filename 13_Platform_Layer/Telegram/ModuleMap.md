# Telegram Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Telegram modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Telegram User
↓
Telegram
↓
Authentication
↓
PlatformService
```
---
# Module Architecture
```text
Telegram
        │
        ├── Update Receiver
        ├── Command Handler
        ├── Callback Handler
        ├── Navigation Manager
        ├── Message Builder
        ├── Media Manager
        └── Metadata Generator
```
---
# Internal Components
## Update Receiver
Telegram Update'larni qabul qiladi.
---
## Command Handler
/start, /help va boshqa Command'larni boshqaradi.
---
## Callback Handler
Inline Keyboard Callback'larini qayta ishlaydi.
---
## Navigation Manager
Reply Keyboard va Inline Keyboard navigatsiyasini boshqaradi.
---
## Message Builder
Telegram xabarlarini yaratadi.
---
## Media Manager
Photo, Video, Voice, Document va boshqa Media'larni boshqaradi.
---
## Metadata Generator
Telegram Metadata yaratadi.
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
Telegram GoldBot Platform Layer ichidagi Telegram Bot Integration va User Interaction jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
