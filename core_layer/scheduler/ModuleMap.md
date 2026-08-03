# Scheduler Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Scheduler modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
CoreEngine
↓
Scheduler
↓
Pipeline
```
---
# Module Architecture
```text
Scheduler
      │
      ├── Schedule Manager
      ├── Timer Manager
      ├── Trigger Manager
      ├── Queue Manager
      ├── Retry Manager
      ├── State Manager
      ├── Event Generator
      └── Execution Coordinator
```
---
# Internal Components
## Schedule Manager
Schedule'larni boshqaradi.
---
## Timer Manager
Timer'larni boshqaradi.
---
## Trigger Manager
Trigger'larni kuzatadi.
---
## Queue Manager
Execution Queue'ni boshqaradi.
---
## Retry Manager
Retry Scheduling boshqaradi.
---
## State Manager
Scheduler holatini boshqaradi.
---
## Event Generator
Schedule Event yaratadi.
---
## Execution Coordinator
Pipeline bilan Execution'ni muvofiqlashtiradi.
---
# Dependency Map
```text
CoreEngine
↓
Scheduler
↓
Pipeline
```
---
# Allowed Dependencies
✓ CoreEngine
✓ Pipeline
✓ Event System
✓ Configuration
✓ ServiceRegistry
---
# Forbidden Dependencies
✗ Data Layer
✗ Context Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
Scheduler egalik qiladi.
✓ Schedule Registry
✓ Timer State
✓ Trigger State
✓ Execution Queue
✓ Schedule Metadata
---
# Module Rules
1. Scheduler yagona Scheduling Engine.
2. Timer markazlashgan boshqariladi.
3. Trigger yagona marta qayta ishlanadi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Scheduler GoldBot Runtime Scheduling boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
