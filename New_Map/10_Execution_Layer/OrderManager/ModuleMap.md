# Order Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
OrderValidator
↓
OrderManager
↓
OrderRouter
```
---
# Module Architecture
```text
OrderManager
        │
        ├── Order Builder
        ├── Order ID Generator
        ├── Lifecycle Manager
        ├── Status Manager
        ├── Order Package Builder
        └── Metadata Generator
```
---
# Internal Components
## Order Builder
Yangi Order obyektini yaratadi.
---
## Order ID Generator
Yagona Order ID yaratadi.
---
## Lifecycle Manager
Order Lifecycle'ni boshqaradi.
---
## Status Manager
Order holatini yangilaydi.
---
## Order Package Builder
OrderRouter uchun Order Package yaratadi.
---
## Metadata Generator
Order Metadata yaratadi.
---
# Allowed Dependencies
✓ OrderValidator
✓ OrderRouter
---
# Forbidden Dependencies
✗ BrokerGateway
✗ ExecutionMonitor
✗ Decision Layer
✗ Risk Layer
---
# Summary
OrderManager GoldBot Execution Layer ichidagi barcha Order Lifecycle jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
