# Order Validator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderValidator ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ExecutionEngine
↓
OrderValidator
↓
OrderManager
```
---
# Module Architecture
```text
OrderValidator
        │
        ├── Structure Validator
        ├── Price Validator
        ├── Volume Validator
        ├── SLTP Validator
        ├── Symbol Validator
        ├── Validation Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Structure Validator
Order formatini tekshiradi.
---
## Price Validator
Entry Price to'g'riligini tekshiradi.
---
## Volume Validator
Lot Size va Volume Step tekshiradi.
---
## SLTP Validator
Stop Loss va Take Profit parametrlarini tekshiradi.
---
## Symbol Validator
Instrument parametrlarini tekshiradi.
---
## Validation Report Builder
Validation Report yaratadi.
---
## Metadata Generator
Validation Metadata yaratadi.
---
# Allowed Dependencies
✓ ExecutionEngine
✓ OrderManager
---
# Forbidden Dependencies
✗ BrokerGateway
✗ OrderRouter
✗ ExecutionMonitor
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
OrderValidator GoldBot Execution Layer ichidagi barcha Order Validation jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
