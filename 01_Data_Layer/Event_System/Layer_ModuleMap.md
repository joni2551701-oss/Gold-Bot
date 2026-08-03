# Event System Layer Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Event System Layer ichidagi barcha modullar va ularning o'zaro bog'lanishini tavsiflaydi.
---
# Layer Architecture
```text
Event System Layer
         │
         ▼
     EventService
         │
 ┌───────┼──────────────┐
 ▼       ▼              ▼
EventPublisher
EventBus
EventDispatcher
EventSubscriber
EventLifecycle
```
---
# Layer Modules
## EventService
Layer Orchestrator.
---
## EventPublisher
Event Producer.
---
## EventBus
Event Transport.
---
## EventDispatcher
Event Routing.
---
## EventSubscriber
Event Consumer.
---
## EventLifecycle
Lifecycle Tracking.
---
# Dependency Map
```text
Source Module
↓
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
Target Module
↓
EventLifecycle
```
---
# Ownership
Layer egalik qiladi.
✓ Event Transport
✓ Event Routing
✓ Event Delivery
✓ Event Lifecycle
✓ Runtime Event Flow
---
# Rules
1. EventService yagona Orchestrator.
2. EventPublisher yagona Producer.
3. EventBus yagona Transport.
4. EventDispatcher yagona Router.
5. EventSubscriber yagona Consumer.
6. EventLifecycle yagona Lifecycle Manager.
7. Circular Dependency taqiqlanadi.
---
# Summary
Event System Layer GoldBot ichidagi barcha Runtime Event almashinuvini boshqaruvchi Canonical Communication Layer hisoblanadi.
