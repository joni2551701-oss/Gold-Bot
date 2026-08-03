# EventDispatcher Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventDispatcher modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu EventDispatcher modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
Resolve Subscribers
↓
Dispatch Event
↓
EventSubscriber
↓
Target Module
```
---
# Single Dispatch Sequence
```text
Queued Event
↓
EventDispatcher
↓
Resolve Subscriber
↓
Dispatch
↓
Subscriber
↓
Completed
```
---
# Broadcast Sequence
```text
Queued Event
↓
EventDispatcher
↓
Resolve Subscribers
↓
Subscriber A
Subscriber B
Subscriber C
↓
Completed
```
---
# No Subscriber Sequence
```text
Queued Event
↓
EventDispatcher
↓
Resolve Subscribers
↓
No Match
↓
Discard or Log
```
---
# Recovery Sequence
```text
Dispatcher Failure
↓
Restore Routing Table
↓
Resume Dispatch
```
---
# Runtime Rules
1. Event faqat EventBus'dan olinadi.
2. Routing Subscriber Registry asosida bajariladi.
3. Event mazmuni o'zgarmaydi.
4. Dispatch tartibi saqlanadi.
5. Circular Dispatch taqiqlanadi.
---
# State Flow
```text
Idle
↓
Waiting Event
↓
Resolving
↓
Dispatching
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
EventBus
↓
EventDispatcher
↓
Resolve Subscribers
↓
Dispatch Event
↓
EventSubscriber
↓
Target Module
