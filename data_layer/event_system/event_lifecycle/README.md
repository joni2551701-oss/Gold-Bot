# Event Lifecycle
Status: CANONICAL
---
# Purpose
EventLifecycle — GoldBot Event System ichidagi barcha Event'larning hayot siklini (Lifecycle) boshqaruvchi komponentidir.
Uning asosiy vazifasi Event yaratilgan vaqtdan boshlab yakuniy iste'mol qilinishigacha bo'lgan barcha bosqichlarni nazorat qilishdir.
EventLifecycle Event yaratmaydi.
EventLifecycle Event uzatmaydi.
EventLifecycle Event'ni qayta ishlamaydi.
U faqat Event holatini boshqaradi.
---
# Objective
EventLifecycle quyidagi vazifalarni bajaradi:
• Event State Management
• Event Lifecycle Tracking
• Event Status Transition
• Event Timeout Monitoring
• Event Retry Coordination
• Event Completion Tracking
• Event Failure Tracking
• Event Cleanup
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
EventLifecycle
```
---
# Responsibilities
EventLifecycle:
✓ Event State boshqarish
✓ Event Lifecycle kuzatish
✓ Timeout Monitoring
✓ Retry Coordination
✓ Completion Detection
✓ Failure Detection
✓ Cleanup Management
---
# Not Responsible
EventLifecycle:
✗ Event Creation
✗ Event Publishing
✗ Event Routing
✗ Event Delivery
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
EventLifecycle qabul qiladi:
• Event Created
• Event Published
• Event Routed
• Event Delivered
• Event Failed
• Retry Request
---
# Output
EventLifecycle yaratadi:
• Lifecycle Status
• Retry Event
• Timeout Event
• Completion Event
• Cleanup Event
---
# Managed Objects
EventLifecycle quyidagilar bilan ishlaydi:
• Event State
• Event Status
• Retry Counter
• Timeout
• Lifecycle Metadata
---
# Workflow
```text
Event Created
↓
Published
↓
Queued
↓
Dispatched
↓
Delivered
↓
Completed
or
Failed
```
---
# Golden Rules
1. Har bir Event Lifecycle orqali kuzatiladi.
2. Event State izchil yangilanadi.
3. Completed Event qayta ishlanmaydi.
4. Failed Event Retry qilinishi mumkin.
5. Timeout nazorat qilinadi.
6. Lifecycle Business Logic bajarmaydi.
7. Event mazmuni o'zgartirilmaydi.
8. Circular Lifecycle taqiqlanadi.
---
# Related Documents
```text
EventLifecycle/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
EventLifecycle GoldBot Event System ichidagi barcha Event'larning Runtime Lifecycle boshqaruvini amalga oshiruvchi yagona Canonical modul hisoblanadi.
