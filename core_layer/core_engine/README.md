# Core Engine
Status: CANONICAL
---
# Purpose
CoreEngine — GoldBot Core Layer ichidagi asosiy Runtime Engine hisoblanadi.
Uning asosiy vazifasi GoldBot Runtime'ni boshqarish, barcha Layer'larni ishga tushirish va tizimning uzluksiz ishlashini ta'minlashdir.
CoreEngine Business Logic bajarmaydi.
CoreEngine Trading qarori chiqarmaydi.
CoreEngine faqat GoldBot Runtime'ni boshqaradi.
---
# Objective
CoreEngine quyidagi vazifalarni bajaradi:
• Runtime Management
• Layer Orchestration
• Module Coordination
• Startup Coordination
• Shutdown Coordination
• Runtime State Management
• Health Supervision
• Recovery Coordination
---
# Layer Position
```text
GoldBot
↓
CoreEngine
↓
Pipeline
↓
All GoldBot Layers
```
---
# Responsibilities
CoreEngine:
✓ Runtime Management
✓ Layer Initialization
✓ Module Coordination
✓ Runtime State
✓ Recovery Coordination
✓ Health Monitoring
✓ Lifecycle Coordination
---
# Not Responsible
CoreEngine:
✗ Market Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk Management
✗ Trade Execution
---
# Input
CoreEngine qabul qiladi:
• Startup Request
• Shutdown Request
• Restart Request
• Runtime Events
• Health Events
• Recovery Events
---
# Output
CoreEngine yaratadi:
• Runtime Commands
• Layer Commands
• Startup Events
• Shutdown Events
• Recovery Events
---
# Managed Objects
CoreEngine quyidagilar bilan ishlaydi:
• Runtime State
• Layer State
• Module State
• Health State
• Lifecycle Metadata
---
# Workflow
```text
System Start
↓
Initialize Runtime
↓
Initialize Layers
↓
Running
↓
Shutdown
```
---
# Golden Rules
1. CoreEngine GoldBot Runtime'ning yagona yuragi hisoblanadi.
2. Barcha Layer'lar CoreEngine orqali ishga tushadi.
3. Runtime State doimo nazorat qilinadi.
4. Recovery markazlashgan boshqariladi.
5. Business Logic bajarilmaydi.
6. Trading qarori chiqarilmaydi.
7. Runtime izchil bo'lishi shart.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
CoreEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
CoreEngine GoldBot Runtime'ni boshqaruvchi, barcha Layer va Service'larni koordinatsiya qiluvchi yagona Canonical Runtime Engine hisoblanadi.
