# Money Management Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MoneyManagement ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
```
---
# Module Architecture
```text
MoneyManagement
        │
        ├── Risk Policy Manager
        ├── Daily Risk Manager
        ├── Weekly Risk Manager
        ├── Monthly Risk Manager
        ├── Capital Allocator
        └── Metadata Generator
```
---
# Internal Components
## Risk Policy Manager
Risk siyosatini tekshiradi.
---
## Daily Risk Manager
Kunlik riskni nazorat qiladi.
---
## Weekly Risk Manager
Haftalik riskni nazorat qiladi.
---
## Monthly Risk Manager
Oylik riskni nazorat qiladi.
---
## Capital Allocator
Yakuniy Capital Allocation yaratadi.
---
## Metadata Generator
Money Metadata yaratadi.
---
# Allowed Dependencies
✓ PositionSizing
✓ DrawdownManager
---
# Forbidden Dependencies
✗ ExposureManager
✗ PortfolioManager
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
MoneyManagement GoldBot Risk Layer ichidagi Capital Management va Risk Policy boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
