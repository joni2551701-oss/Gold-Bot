# Core Service
Status: CANONICAL
---
# Purpose
CoreService — GoldBot Core Layer ichidagi markaziy Service Orchestrator hisoblanadi.
Uning asosiy vazifasi Core Layer modullarini yagona Runtime Service sifatida boshqarish va CoreEngine uchun yagona kirish nuqtasini (Entry Point) ta'minlashdir.
CoreService Business Logic bajarmaydi.
CoreService Trading qarori chiqarmaydi.
CoreService faqat Core Runtime Service'ni boshqaradi.
---
# Objective
CoreService quyidagi vazifalarni bajaradi:
• Core Service Orchestration
• Core Module Coordination
• Runtime Command Routing
• Lifecycle Coordination
• Runtime Health Coordination
• Service State Management
• Recovery Coordination
• Runtime Event Coordination
---
# Layer Position
```text
CoreEngine
↓
CoreService
├── Pipeline
├── Scheduler
├── ServiceRegistry
├── Configuration
├── HealthMonitor
├── Startup
└── Shutdown
```
---
# Responsibilities
CoreService:
✓ Core Module Coordination
✓ Runtime Command Routing
✓ Lifecycle Coordination
✓ Service State Management
✓ Recovery Coordination
✓ Health Coordination
✓ Runtime Event Coordination
---
# Not Responsible
CoreService:
✗ Market Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk Management
✗ Trade Execution
---
# Input
CoreService qabul qiladi:
• Runtime Commands
• Startup Events
• Shutdown Events
• Health Events
• Recovery Events
• Service Requests
---
# Output
CoreService yaratadi:
• Module Commands
• Runtime Events
• Service Status
• Lifecycle Events
• Health Status
---
# Managed Objects
CoreService quyidagilar bilan ishlaydi:
• Runtime State
• Service State
• Lifecycle State
• Core Metadata
• Runtime Events
---
# Workflow
```text
CoreEngine
↓
CoreService
↓
Route Command
↓
Target Core Module
↓
Receive Response
↓
Update Runtime State
```
---
# Golden Rules
1. CoreService Core Layer ichidagi yagona Service Entry Point hisoblanadi.
2. Core Module'lar CoreService orqali koordinatsiya qilinadi.
3. Runtime State doimo yangilanadi.
4. Recovery markazlashgan boshqariladi.
5. Business Logic bajarilmaydi.
6. Trading Logic bajarilmaydi.
7. Runtime izchil bo'lishi shart.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
CoreService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
CoreService GoldBot Core Layer ichidagi barcha Core modullarni boshqaruvchi yagona Canonical Service Orchestrator hisoblanadi.
