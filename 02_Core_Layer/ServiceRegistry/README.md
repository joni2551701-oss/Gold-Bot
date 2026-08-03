# Service Registry
Status: CANONICAL
---
# Purpose
ServiceRegistry — GoldBot Core Layer ichidagi barcha Service va Component'larni ro'yxatdan o'tkazish hamda ularga markazlashgan kirishni ta'minlovchi komponentdir.
Uning asosiy vazifasi Runtime davomida Service Discovery va Service Resolution jarayonlarini boshqarishdir.
ServiceRegistry Service yaratmaydi.
ServiceRegistry Business Logic bajarmaydi.
ServiceRegistry faqat Service Registry'ni boshqaradi.
---
# Objective
ServiceRegistry quyidagi vazifalarni bajaradi:
• Service Registration
• Service Discovery
• Service Resolution
• Service Lifecycle Tracking
• Dependency Registration
• Runtime Registry Management
• Health Registration
• Registry State Management
---
# Layer Position
```text
CoreEngine
↓
ServiceRegistry
↓
GoldBot Services
```
---
# Responsibilities
ServiceRegistry:
✓ Service Registration
✓ Service Discovery
✓ Service Resolution
✓ Dependency Registry
✓ Runtime Registry
✓ Service Lifecycle Tracking
✓ Registry State
---
# Not Responsible
ServiceRegistry:
✗ Service Execution
✗ Business Logic
✗ Market Analysis
✗ Strategy
✗ AI Analysis
✗ Decision
✗ Trade Execution
---
# Input
ServiceRegistry qabul qiladi:
• Register Request
• Unregister Request
• Resolve Request
• Discovery Request
• Health Update
---
# Output
ServiceRegistry yaratadi:
• Registered Service
• Service Reference
• Registry Event
• Registry Status
• Service Metadata
---
# Managed Objects
ServiceRegistry quyidagilar bilan ishlaydi:
• Registered Services
• Service Metadata
• Dependency Graph
• Registry State
• Lifecycle Metadata
---
# Workflow
```text
Register Service
↓
Store Metadata
↓
Resolve Request
↓
Return Service
↓
Runtime
```
---
# Golden Rules
1. Har bir Service Registry'da ro'yxatdan o'tadi.
2. Har bir Service noyob Identifier oladi.
3. Resolve faqat Registry orqali amalga oshiriladi.
4. Registry Runtime davomida yagona manba hisoblanadi.
5. ServiceRegistry Service ishlatmaydi.
6. Business Logic bajarilmaydi.
7. Registry State doim yangilanadi.
8. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
ServiceRegistry/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ServiceRegistry GoldBot Runtime davomida barcha Service va Component'larni boshqaruvchi yagona Canonical Registry komponentidir.
