# EventService Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventService modulining ichki arxitekturasi va komponentlarini tavsiflaydi.
---
# Module Position
```text
Modules
↓
EventService
↓
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
EventLifecycle
```
---
# Module Architecture
```text
EventService
        │
        ├── Request Manager
        ├── Module Coordinator
        ├── Runtime Manager
        ├── Lifecycle Manager
        ├── Recovery Manager
        ├── Health Monitor
        ├── State Manager
        └── Event Reporter
```
---
# Internal Components
## Request Manager
Runtime so'rovlarini qabul qiladi.
---
## Module Coordinator
Event modullarini boshqaradi.
---
## Runtime Manager
Runtime Event Flow'ni nazorat qiladi.
---
## Lifecycle Manager
Startup, Restart va Shutdown boshqaradi.
---
## Recovery Manager
Nosozliklardan tiklanishni boshqaradi.
---
## Health Monitor
Event System sog'ligini kuzatadi.
---
## State Manager
Runtime holatini boshqaradi.
---
## Event Reporter
Service Runtime hodisalarini yaratadi.
---
# Dependency Map
```text
Modules
↓
EventService
↓
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
EventLifecycle
```
---
# Allowed Dependencies
✓ EventPublisher
✓ EventBus
✓ EventDispatcher
✓ EventSubscriber
✓ EventLifecycle
✓ Configuration Layer
✓ Event Bus Infrastructure
---
# Forbidden Dependencies
✗ Context Layer
✗ Analysis Layer
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ Signal Layer
✗ AI Layer
✗ Platform Layer
✗ Business Layer
✗ Learning Layer
✗ Media Layer
✗ Future Expansion Layer
---
# Ownership
EventService egalik qiladi.
✓ Runtime Lifecycle
✓ Event Coordination
✓ Module State
✓ Recovery State
✓ Health State
✓ Runtime Events
---
# Module Rules
1. EventService yagona Canonical Orchestrator hisoblanadi.
2. Barcha Event modullari markazlashgan boshqariladi.
3. Runtime Lifecycle izchil bo'lishi shart.
4. Health Monitoring doim ishlaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
EventService Event System ichidagi barcha Event modullarini boshqaruvchi yagona Canonical Orchestrator moduli hisoblanadi.
