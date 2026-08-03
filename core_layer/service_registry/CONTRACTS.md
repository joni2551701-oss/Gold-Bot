# ServiceRegistry Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ServiceRegistry modulining rasmiy Architecture Contract hujjati hisoblanadi.
ServiceRegistry GoldBot Runtime davomida barcha Service Registration va Discovery jarayonlarini boshqaruvchi yagona Canonical Registry hisoblanadi.
---
# Module Responsibility
ServiceRegistry quyidagilar uchun javobgar.
✓ Service Registration
✓ Service Discovery
✓ Service Resolution
✓ Dependency Registry
✓ Service Metadata
✓ Registry State
✓ Lifecycle Tracking
ServiceRegistry bajarmaydi.
✗ Service Execution
✗ Business Logic
✗ Strategy
✗ AI Analysis
✗ Decision
✗ Trade Execution
---
# Module Boundary
CoreEngine
↓
ServiceRegistry
↓
Registered Services
↓
Boundary End
---
# Input Contract
• Register Request
• Resolve Request
• Discovery Request
• Unregister Request
• Health Update
---
# Output Contract
• Service Reference
• Registry Status
• Registry Event
• Service Metadata
---
# Allowed Dependencies
✓ CoreEngine
✓ Configuration
✓ HealthMonitor
✓ Event System
---
# Forbidden Dependencies
✗ Data Layer
✗ Context Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Ready
• Registering
• Resolving
• Updating
• Failed
---
# Runtime Contract
1. ServiceRegistry GoldBot ichidagi yagona Canonical Registry hisoblanadi.
2. Har bir Service Registry'da ro'yxatdan o'tishi shart.
3. Resolve faqat Registry orqali amalga oshiriladi.
4. Har bir Service noyob Identifier oladi.
5. Registry Runtime davomida yagona Service Source hisoblanadi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
ServiceRegistry:
✓ Service ro'yxatdan o'tkazadi.
✓ Service topadi.
✓ Dependency boshqaradi.
✓ Registry holatini boshqaradi.
ServiceRegistry:
✗ Service ishga tushirmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
✗ Qaror chiqarmaydi.
---
# Acceptance Criteria
✓ Service Registration ishlaydi.
✓ Service Discovery ishlaydi.
✓ Service Resolution ishlaydi.
✓ Dependency Registry ishlaydi.
✓ Registry State boshqariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ServiceRegistry Contract GoldBot Runtime Registry komponentining rasmiy arxitektura shartnomasi hisoblanadi.
ServiceRegistry GoldBot ichidagi barcha Service va Component'lar uchun yagona Canonical Registry va Discovery markazi hisoblanadi.
