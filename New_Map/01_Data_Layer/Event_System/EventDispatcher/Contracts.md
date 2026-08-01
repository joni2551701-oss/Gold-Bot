# EventDispatcher Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventDispatcher modulining rasmiy Architecture Contract hujjati hisoblanadi.
EventDispatcher GoldBot Event System ichidagi barcha Event Routing jarayonlari uchun yagona Canonical Dispatcher hisoblanadi.
---
# Module Responsibility
EventDispatcher quyidagilar uchun javobgar.
✓ Event Routing
✓ Subscriber Resolution
✓ Event Dispatch
✓ Broadcast Dispatch
✓ Delivery Coordination
✓ Runtime Event Distribution
✓ Dispatch Validation
EventDispatcher bajarmaydi.
✗ Event Creation
✗ Event Publishing
✗ Event Queue
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Module Boundary
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
Boundary End
---
# Input Contract
• Routed Event
• Runtime Event
• Lifecycle Event
• Recovery Event
---
# Output Contract
• Dispatched Event
• Broadcast Delivery
• Delivery Status
• Dispatch Events
---
# Allowed Dependencies
✓ EventBus
✓ EventSubscriber
✓ EventLifecycle
✓ Configuration Layer
---
# Forbidden Dependencies
✗ EventPublisher
✗ Context Layer
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Platform Layer
✗ Business Layer
---
# State Contract
• Initializing
• Ready
• Resolving
• Dispatching
• Completed
• Failed
---
# Runtime Contract
1. EventDispatcher yagona Canonical Routing komponenti hisoblanadi.
2. Event faqat EventBus orqali qabul qilinadi.
3. Subscriber Routing Table orqali aniqlanadi.
4. Event mazmuni o'zgartirilmaydi.
5. Broadcast barcha mos Subscriber'larga yuboriladi.
6. Circular Dispatch qat'iyan taqiqlanadi.
---
# Architecture Rules
EventDispatcher:
✓ Event Routing bajaradi.
✓ Subscriber aniqlaydi.
✓ Event Dispatch qiladi.
✓ Delivery Coordination bajaradi.
EventDispatcher:
✗ Event yaratmaydi.
✗ Event Publish qilmaydi.
✗ Event Queue boshqarmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
---
# Acceptance Criteria
✓ Routing ishlaydi.
✓ Subscriber Resolution ishlaydi.
✓ Event Dispatch ishlaydi.
✓ Broadcast ishlaydi.
✓ Delivery muvaffaqiyatli yakunlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
EventDispatcher Contract GoldBot Event System ichidagi Canonical Event Routing komponentining rasmiy arxitektura shartnomasi hisoblanadi.
EventDispatcher EventBus orqali kelgan barcha Event'larni tegishli EventSubscriber'larga yetkazuvchi yagona ruxsat etilgan modul hisoblanadi.
