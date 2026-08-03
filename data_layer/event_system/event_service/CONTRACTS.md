# EventService Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventService modulining rasmiy Architecture Contract hujjati hisoblanadi.
EventService Event System ichidagi barcha Runtime Event Pipeline va Lifecycle boshqaruvini amalga oshiruvchi yagona Canonical Orchestrator hisoblanadi.
---
# Module Responsibility
EventService quyidagilar uchun javobgar.
✓ Event System Orchestration
✓ Runtime Lifecycle Management
✓ Module Coordination
✓ Recovery Coordination
✓ Health Monitoring
✓ Runtime State Management
✓ Event Flow Coordination
EventService bajarmaydi.
✗ Event Creation
✗ Event Publishing
✗ Event Routing
✗ Event Dispatch
✗ Event Subscription
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Module Boundary
Modules
↓
EventService
↓
Event Modules
↓
Boundary End
---
# Input Contract
• Runtime Request
• Startup Request
• Shutdown Request
• Restart Request
• Recovery Request
• Module Events
---
# Output Contract
• Module Commands
• Runtime Events
• Lifecycle Events
• Recovery Commands
• Health Status
---
# Allowed Dependencies
✓ EventPublisher
✓ EventBus
✓ EventDispatcher
✓ EventSubscriber
✓ EventLifecycle
✓ Configuration Layer
✓ Event Bus Infrastructure
---
# Forbidden Dependencies
✗ Context Layer
✗ Analysis Layer
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ Signal Layer
✗ AI Layer
✗ Platform Layer
✗ Business Layer
✗ Learning Layer
✗ Media Layer
✗ Future Expansion Layer
---
# State Contract
• Initializing
• Ready
• Running
• Recovering
• Restarting
• Stopping
• Stopped
• Failed
---
# Runtime Contract
1. EventService Event System ichidagi yagona Canonical Orchestrator hisoblanadi.
2. Barcha Event modullari faqat EventService koordinatsiyasi ostida ishlaydi.
3. Runtime Lifecycle markazlashgan holda boshqariladi.
4. Recovery avtomatik bajarilishi mumkin.
5. Health Monitoring doim ishlashi shart.
6. EventService Event mazmunini o'zgartirmaydi.
7. Business Logic bajarilmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
EventService:
✓ Runtime boshqaradi.
✓ Module Coordination bajaradi.
✓ Recovery boshqaradi.
✓ Lifecycle boshqaradi.
✓ Health Monitoring bajaradi.
EventService:
✗ Event yaratmaydi.
✗ Event Publish qilmaydi.
✗ Event Dispatch qilmaydi.
✗ Event Subscribe qilmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
---
# Contract Violations
Quyidagilar Architecture Violation hisoblanadi.
• EventService → Context Layer import
• EventService → Strategy Layer import
• EventService → Decision Layer import
• EventService → AI Layer import
• EventService → Business Layer import
• Event modullarini EventService'dan tashqaridan boshqarish
• Runtime Lifecycle'ni chetlab o'tish
• Circular Dependency
---
# Acceptance Criteria
✓ Runtime Lifecycle ishlaydi.
✓ Event modullari koordinatsiya qilinadi.
✓ Recovery ishlaydi.
✓ Health Monitoring ishlaydi.
✓ Runtime State saqlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
EventService Contract Event System ichidagi markaziy Orchestrator komponentining rasmiy arxitektura shartnomasi hisoblanadi.
EventService GoldBot Event System uchun Runtime Pipeline, Module Coordination, Recovery va Lifecycle boshqaruvini amalga oshiruvchi yagona Canonical modul hisoblanadi.
