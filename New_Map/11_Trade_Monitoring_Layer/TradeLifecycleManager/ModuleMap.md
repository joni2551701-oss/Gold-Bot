# Trade Lifecycle Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeLifecycleManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
```
---
# Module Architecture
```text
TradeLifecycleManager
        │
        ├── State Manager
        ├── Transition Validator
        ├── Event Processor
        ├── Lifecycle Controller
        ├── Lifecycle Report Builder
        └── Metadata Generator
```
---
# Internal Components
## State Manager
Trade holatini boshqaradi.
---
## Transition Validator
State Transition qoidalarini tekshiradi.
---
## Event Processor
Trade Event'larni qayta ishlaydi.
---
## Lifecycle Controller
Trade Lifecycle'ni boshqaradi.
---
## Lifecycle Report Builder
Lifecycle Report yaratadi.
---
## Metadata Generator
Lifecycle Metadata yaratadi.
---
# Allowed Dependencies
✓ PositionMonitor
✓ SLTPMonitor
---
# Forbidden Dependencies
✗ BreakevenManager
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
---
# Summary
TradeLifecycleManager GoldBot Trade Monitoring Layer ichidagi Trade Lifecycle va State Machine boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
