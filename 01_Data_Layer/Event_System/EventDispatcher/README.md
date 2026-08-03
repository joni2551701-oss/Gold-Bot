# Event Dispatcher
Status: CANONICAL
---
# Purpose
EventDispatcher — GoldBot Event System ichidagi Event Routing komponentidir.
Uning asosiy vazifasi EventBus'dan kelgan Event'larni mos EventSubscriber'larga yo'naltirish (Dispatch qilish) hisoblanadi.
EventDispatcher Event yaratmaydi.
EventDispatcher Event saqlamaydi.
EventDispatcher faqat Event Routing bajaradi.
---
# Objective
EventDispatcher quyidagi vazifalarni bajaradi:
• Event Routing
• Subscriber Resolution
• Event Dispatch
• Broadcast Dispatch
• Priority Dispatch
• Delivery Coordination
• Runtime Event Distribution
• Routing Validation
---
# Layer Position
```text
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
Target Module
```
---
# Responsibilities
EventDispatcher:
✓ Event Routing
✓ Subscriber Resolution
✓ Event Dispatch
✓ Broadcast Dispatch
✓ Delivery Coordination
✓ Runtime Event Distribution
✓ Routing Validation
---
# Not Responsible
EventDispatcher:
✗ Event Creation
✗ Event Publishing
✗ Event Queue
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
EventDispatcher qabul qiladi:
• Routed Event
• Runtime Event
• Lifecycle Event
• Error Event
• Recovery Event
---
# Output
EventDispatcher yaratadi:
• Routed Delivery
• Broadcast Delivery
• Dispatch Result
• Delivery Events
---
# Managed Objects
EventDispatcher quyidagilar bilan ishlaydi:
• Routing Table
• Subscriber Registry
• Dispatch State
• Delivery Metadata
---
# Workflow
```text
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
# Golden Rules
1. EventDispatcher Event yaratmaydi.
2. EventDispatcher Event mazmunini o'zgartirmaydi.
3. Har bir Event Routing Table orqali Dispatch qilinadi.
4. Broadcast Event barcha mos Subscriber'larga yuboriladi.
5. EventBus Dispatcher uchun yagona Event manbai hisoblanadi.
6. EventDispatcher Business Logic bajarmaydi.
7. Runtime davomida Routing izchil bo'lishi kerak.
8. Circular Dispatch taqiqlanadi.
---
# Related Documents
```text
EventDispatcher/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
EventDispatcher GoldBot Event System ichidagi yagona Canonical Event Routing komponentidir.
Uning vazifasi:
• EventBus'dan Event qabul qilish;
• Subscriber'larni aniqlash;
• Event'larni Dispatch qilish;
• Runtime Event Distribution'ni boshqarish.
