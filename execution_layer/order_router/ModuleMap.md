# Order Router Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderRouter ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
OrderManager
↓
OrderRouter
↓
BrokerGateway
```
---
# Module Architecture
```text
OrderRouter
        │
        ├── Policy Loader
        ├── Broker Selector
        ├── Exchange Selector
        ├── Route Validator
        ├── Routed Order Builder
        └── Metadata Generator
```
---
# Internal Components
## Policy Loader
Routing Policy yuklaydi.
---
## Broker Selector
Mos Broker tanlaydi.
---
## Exchange Selector
Mos Exchange tanlaydi.
---
## Route Validator
Tanlangan Route'ni tekshiradi.
---
## Routed Order Builder
BrokerGateway uchun Routed Order yaratadi.
---
## Metadata Generator
Routing Metadata yaratadi.
---
# Allowed Dependencies
✓ OrderManager
✓ BrokerGateway
---
# Forbidden Dependencies
✗ ExecutionMonitor
✗ ExecutionService
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
OrderRouter GoldBot Execution Layer ichidagi Broker Routing va Order Dispatch jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
