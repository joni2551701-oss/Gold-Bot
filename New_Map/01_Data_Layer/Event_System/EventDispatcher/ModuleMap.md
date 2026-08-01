# EventDispatcher Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventDispatcher modulining ichki arxitekturasi va komponentlarini tavsiflaydi.
---
# Module Position
```text
EventBus
↓
EventDispatcher
↓
EventSubscriber
```
---
# Module Architecture
```text
EventDispatcher
        │
        ├── Routing Manager
        ├── Subscriber Resolver
        ├── Dispatch Manager
        ├── Broadcast Manager
        ├── Delivery Manager
        ├── State Manager
        └── Event Reporter
```
---
# Internal Components
## Routing Manager
Routing Table'ni boshqaradi.
---
## Subscriber Resolver
Mos Subscriber'larni aniqlaydi.
---
## Dispatch Manager
Event Dispatch bajaradi.
---
## Broadcast Manager
Broadcast Event'larni boshqaradi.
---
## Delivery Manager
Delivery jarayonini nazorat qiladi.
---
## State Manager
Dispatcher holatini boshqaradi.
---
## Event Reporter
Dispatch Runtime hodisalarini yaratadi.
---
# Dependency Map
```text
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
Target Module
```
---
# Allowed Dependencies
✓ EventBus
✓ EventSubscriber
✓ EventLifecycle
✓ Configuration Layer
---
# Forbidden Dependencies
✗ EventPublisher
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Trading Logic
---
# Ownership
EventDispatcher egalik qiladi.
✓ Routing Table
✓ Subscriber Registry
✓ Dispatch State
✓ Delivery State
---
# Module Rules
1. EventDispatcher yagona Canonical Routing komponentidir.
2. Dispatch Routing Table orqali amalga oshiriladi.
3. Subscriber Resolution avtomatik bajariladi.
4. Event mazmuni o'zgarmaydi.
5. Circular Dependency taqiqlanadi.
---
# Summary
EventDispatcher GoldBot Event System ichidagi yagona Canonical Event Routing moduli hisoblanadi.
