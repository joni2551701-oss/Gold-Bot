# Platform Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Platform Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
User
        │
        ▼
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   Telegram      MobileAPI         WebAPI         DesktopAPI
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
                Authentication
                       │
                       ▼
                PlatformService
                       │
                       ▼
                Internal Service
                       │
                       ▼
                NotificationCenter
                       │
                       ▼
        Telegram / MobileAPI / WebAPI / DesktopAPI
                       │
                       ▼
                     User
```
---
# Runtime Rules
1. User Request mavjud bo'lishi shart.
2. Telegram, MobileAPI, WebAPI, DesktopAPI mustaqil parallel kanallar sifatida ishlaydi.
3. Authentication muvaffaqiyatli bajarilishi shart.
3. PlatformService Request'ni marshrutlashi shart.
4. Internal Service javob qaytarishi shart.
5. Notification kerak bo'lsa yuborilishi shart.
6. User Response standart formatda qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Receiving Request
↓
Authenticating
↓
Routing
↓
Processing
↓
Responding
↓
Completed
```
---
# Summary
User
↓
Platform Layer
↓
GoldBot Core
↓
User
