# EventService
Status: CANONICAL
---
# Purpose
EventService — Event System Layer'ning markaziy Orchestrator komponentidir.
Uning asosiy vazifasi Event System ichidagi barcha modullarni yagona Runtime Pipeline ichida boshqarish va koordinatsiya qilishdir.
EventService Event yaratmaydi.
EventService Event uzatmaydi.
EventService Event iste'mol qilmaydi.
U faqat Event System Runtime'ni boshqaradi.
---
# Objective
EventService quyidagi vazifalarni bajaradi:
• Event System Orchestration
• Runtime Lifecycle Coordination
• Event Flow Coordination
• Module Coordination
• Recovery Coordination
• Health Monitoring
• Event Pipeline Management
• Runtime State Management
---
# Layer Position
```text
Modules
↓
EventService
├── EventPublisher
├── EventBus
├── EventDispatcher
├── EventSubscriber
└── EventLifecycle
↓
GoldBot Core
```
---
# Responsibilities
EventService:
✓ Event System Coordination
✓ Runtime Lifecycle
✓ Module Coordination
✓ Event Flow Management
✓ Recovery Coordination
✓ Health Monitoring
✓ Runtime State Management
---
# Not Responsible
EventService:
✗ Event Creation
✗ Event Routing
✗ Event Dispatch
✗ Event Subscription
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
EventService qabul qiladi:
• Runtime Requests
• Startup Request
• Shutdown Request
• Restart Request
• Recovery Request
• Module Events
---
# Output
EventService yaratadi:
• Module Commands
• Runtime Events
• Lifecycle Events
• Recovery Commands
• Health Status
---
# Controlled Modules
EventService boshqaradi:
• EventPublisher
• EventBus
• EventDispatcher
• EventSubscriber
• EventLifecycle
---
# Workflow
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
```
---
# Golden Rules
1. EventService Event System'ning yagona Canonical Orchestrator'i hisoblanadi.
2. Event modullari faqat EventService koordinatsiyasi ostida ishlaydi.
3. Runtime Lifecycle markazlashgan holda boshqariladi.
4. Recovery avtomatik ishlashi mumkin.
5. Health Monitoring doimiy ishlaydi.
6. EventService Event mazmunini o'zgartirmaydi.
7. EventService Business Logic bajarmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
EventService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
EventService Event System ichidagi barcha Runtime Event Pipeline, Lifecycle va Module Coordination jarayonlarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
