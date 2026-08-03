# Pipeline
Status: CANONICAL
---
# Purpose
Pipeline — GoldBot Core Layer ichidagi Runtime Pipeline boshqaruv komponentidir.
Uning asosiy vazifasi GoldBot Layer'lari va Service'lari orasidagi ma'lumotlar oqimini (Flow) yagona tartib asosida boshqarishdir.
Pipeline Business Logic bajarmaydi.
Pipeline Decision qabul qilmaydi.
Pipeline Data yaratmaydi.
U faqat Runtime Flow'ni boshqaradi.
---
# Objective
Pipeline quyidagi vazifalarni bajaradi:
• Runtime Flow Management
• Layer Routing
• Stage Coordination
• Pipeline Execution
• Runtime Synchronization
• Error Propagation
• Recovery Coordination
• Pipeline State Management
---
# Layer Position
```text
CoreEngine
↓
Pipeline
↓
GoldBot Layers
```
---
# Responsibilities
Pipeline:
✓ Runtime Flow Management
✓ Stage Coordination
✓ Layer Routing
✓ Runtime Synchronization
✓ Pipeline State Management
✓ Error Propagation
✓ Recovery Coordination
---
# Not Responsible
Pipeline:
✗ Market Analysis
✗ Strategy
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
✗ Data Storage
---
# Input
Pipeline qabul qiladi:
• Runtime Commands
• Pipeline Requests
• Layer Responses
• Runtime Events
---
# Output
Pipeline yaratadi:
• Pipeline Commands
• Layer Commands
• Runtime Events
• Pipeline Status
---
# Managed Objects
Pipeline quyidagilar bilan ishlaydi:
• Runtime Flow
• Pipeline State
• Pipeline Metadata
• Execution Order
---
# Workflow
```text
CoreEngine
↓
Pipeline
↓
Data Layer
↓
Context Layer
↓
Signal Layer
↓
AI Layer
↓
Decision Layer
↓
Risk Layer
↓
Execution Layer
```
---
# Golden Rules
1. Pipeline qat'iy ketma-ket ishlaydi.
2. Har bir Layer oldingi Layer natijasini qabul qiladi.
3. Pipeline Stage o'tkazib yuborilmaydi.
4. Runtime State doimo yangilanadi.
5. Error yuqoriga uzatiladi.
6. Pipeline Business Logic bajarmaydi.
7. Pipeline Data'ni o'zgartirmaydi.
8. Circular Pipeline taqiqlanadi.
---
# Related Documents
```text
Pipeline/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Pipeline GoldBot Runtime ichidagi barcha Layer va Service'lar o'rtasidagi Execution Flow'ni boshqaruvchi yagona Canonical Pipeline komponentidir.
