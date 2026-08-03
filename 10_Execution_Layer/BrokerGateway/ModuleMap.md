# Broker Gateway Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BrokerGateway ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
OrderRouter
↓
BrokerGateway
↓
ExecutionMonitor
```
---
# Module Architecture
```text
BrokerGateway
        │
        ├── Connection Manager
        ├── Authentication Manager
        ├── Request Builder
        ├── API Client
        ├── Response Parser
        ├── Communication Logger
        └── Metadata Generator
```
---
# Internal Components
## Connection Manager
Broker bilan ulanishni boshqaradi.
---
## Authentication Manager
API autentifikatsiyasini boshqaradi.
---
## Request Builder
Broker API uchun Request yaratadi.
---
## API Client
HTTP/WebSocket orqali Broker bilan ishlaydi.
---
## Response Parser
Broker javoblarini standart formatga o'tkazadi.
---
## Communication Logger
Barcha Request va Response'larni log qiladi.
---
## Metadata Generator
Gateway Metadata yaratadi.
---
# Allowed Dependencies
✓ OrderRouter
✓ ExecutionMonitor
---
# Forbidden Dependencies
✗ OrderManager
✗ OrderValidator
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
BrokerGateway GoldBot Execution Layer ichidagi barcha tashqi Broker Communication jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
