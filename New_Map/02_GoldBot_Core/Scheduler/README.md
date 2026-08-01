# Scheduler
Status: CANONICAL
---
# Purpose
Scheduler — GoldBot Core Layer ichidagi Runtime Scheduling komponentidir.
Uning asosiy vazifasi GoldBot Runtime davomida barcha rejalashtirilgan (Scheduled) vazifalarni belgilangan vaqt, interval yoki trigger asosida ishga tushirishdir.
Scheduler Business Logic bajarmaydi.
Scheduler Trading qarori chiqarmaydi.
Scheduler faqat Task Scheduling va Execution Timing'ni boshqaradi.
---
# Objective
Scheduler quyidagi vazifalarni bajaradi:
• Task Scheduling
• Periodic Task Execution
• Time-based Execution
• Trigger-based Execution
• Schedule Management
• Execution Coordination
• Runtime Timing
• Retry Scheduling
---
# Layer Position
```text
CoreEngine
↓
Scheduler
↓
Pipeline
↓
GoldBot Layers
```
---
# Responsibilities
Scheduler:
✓ Task Scheduling
✓ Runtime Timing
✓ Trigger Monitoring
✓ Periodic Execution
✓ Retry Scheduling
✓ Execution Queue
✓ Schedule State Management
---
# Not Responsible
Scheduler:
✗ Business Logic
✗ Market Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Trade Execution
---
# Input
Scheduler qabul qiladi:
• Schedule Request
• Runtime Trigger
• Timer Event
• Retry Request
• Startup Request
---
# Output
Scheduler yaratadi:
• Scheduled Task
• Execution Trigger
• Runtime Event
• Retry Schedule
• Schedule Status
---
# Managed Objects
Scheduler quyidagilar bilan ishlaydi:
• Schedule
• Timer
• Trigger
• Execution Queue
• Schedule Metadata
---
# Workflow
```text
Schedule Task
↓
Register Schedule
↓
Wait Trigger
↓
Execute
↓
Complete
↓
Next Schedule
```
---
# Golden Rules
1. Har bir Scheduled Task ro'yxatdan o'tadi.
2. Execution vaqti qat'iy kuzatiladi.
3. Trigger bir marta qayta ishlanadi.
4. Retry Scheduling qo'llab-quvvatlanadi.
5. Scheduler Task mazmunini o'zgartirmaydi.
6. Business Logic bajarilmaydi.
7. Runtime Timing aniq bo'lishi shart.
8. Circular Scheduling taqiqlanadi.
---
# Related Documents
```text
Scheduler/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Scheduler GoldBot Runtime davomida barcha Scheduled Task va Trigger'larni boshqaruvchi yagona Canonical Scheduling komponentidir.
