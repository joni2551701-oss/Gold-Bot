# GoldBot Core Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Core Layer'ning rasmiy Architecture Contract hujjati hisoblanadi.
GoldBot Core Layer butun GoldBot Runtime boshqaruvi uchun yagona Canonical Core Layer hisoblanadi.
---
# Layer Responsibility
GoldBot Core Layer quyidagilar uchun javobgar.
✓ Runtime Initialization
✓ Runtime Orchestration
✓ Runtime Configuration
✓ Runtime Scheduling
✓ Runtime Pipeline
✓ Runtime Service Coordination
✓ Runtime Health Monitoring
✓ Runtime Shutdown
---
# Layer Boundary
System Runtime
↓
GoldBot Core Layer
↓
All Runtime Layers
↓
Boundary End
---
# Input Contract
• Startup Request
• Runtime Request
• Configuration
• Service Events
• Health Events
• Shutdown Request
---
# Output Contract
• Runtime Commands
• Layer Commands
• Runtime Events
• Health Status
• Shutdown Events
---
# Allowed Dependencies
✓ Event System
✓ Configuration Source
✓ Runtime Infrastructure
✓ Operating Environment
---
# Forbidden Dependencies
✗ Context Layer Logic
✗ Signal Layer Logic
✗ Decision Layer Logic
✗ Risk Layer Logic
✗ AI Layer Logic
✗ Execution Layer Logic
✗ Business Rules
✗ Trading Logic
---
# Runtime Contract
1. Startup Runtime'dan oldin bajarilishi shart.
2. Configuration Runtime boshlanishidan oldin tayyor bo'lishi shart.
3. ServiceRegistry barcha Service'larni boshqaradi.
4. CoreEngine Runtime markazi hisoblanadi.
5. CoreService Core koordinatsiyani bajaradi.
6. Pipeline barcha Layer Flow'ni boshqaradi.
7. Scheduler Runtime Timing'ni boshqaradi.
8. HealthMonitor Runtime sog'ligini kuzatadi.
9. Shutdown Runtime yakunini boshqaradi.
10. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
GoldBot Core Layer:
✓ Runtime boshqaradi.
✓ Layer'larni koordinatsiya qiladi.
✓ Configuration boshqaradi.
✓ Service Registry yuritadi.
✓ Monitoring bajaradi.
✓ Startup va Shutdown boshqaradi.
GoldBot Core Layer:
✗ Trading qarori chiqarmaydi.
✗ Signal yaratmaydi.
✗ AI Analysis bajarmaydi.
✗ Risk hisoblamaydi.
✗ Trade Execution bajarmaydi.
---
# Acceptance Criteria
✓ Runtime Initialization ishlaydi.
✓ Configuration ishlaydi.
✓ Service Registry ishlaydi.
✓ Pipeline ishlaydi.
✓ Scheduler ishlaydi.
✓ Health Monitoring ishlaydi.
✓ Shutdown ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
GoldBot Core Layer Contract GoldBot Runtime boshqaruvining rasmiy arxitektura shartnomasi hisoblanadi.
GoldBot Core Layer CoreEngine, CoreService, Pipeline, Scheduler, ServiceRegistry, Configuration, HealthMonitor, Startup va Shutdown modullaridan tashkil topgan yagona Canonical Runtime Management Layer hisoblanadi.
