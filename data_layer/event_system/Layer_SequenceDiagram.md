# Event System Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Event System Layer Runtime Sequence'ni tavsiflaydi.
---
# Complete Runtime Sequence
```text
System Start
↓
EventService
↓
Initialize EventPublisher
↓
Initialize EventBus
↓
Initialize EventDispatcher
↓
Initialize EventSubscriber
↓
Initialize EventLifecycle
↓
Ready
```
---
# Runtime Event Sequence
```text
Module
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
# Recovery Sequence
```text
Failure
↓
EventService
↓
Restore Event Queue
↓
Restore Subscribers
↓
Resume Runtime
```
---
# Shutdown Sequence
```text
Shutdown
↓
Stop Event Flow
↓
Release Resources
↓
Stopped
```
---
# Runtime Rules
1. EventService Runtime'ni boshqaradi.
2. Event Flow doim EventBus orqali o'tadi.
3. Dispatch EventDispatcher orqali bajariladi.
4. Lifecycle barcha Event'larni kuzatadi.
5. Circular Runtime taqiqlanadi.
---
# Summary
Canonical Runtime Sequence:
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
