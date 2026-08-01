# CoreEngine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat CoreEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
CoreEngine GoldBot Runtime'ni boshqaruvchi yagona Canonical Runtime Engine hisoblanadi.
---
# Module Responsibility
CoreEngine quyidagilar uchun javobgar.
✓ Runtime Management
✓ Layer Orchestration
✓ Startup Management
✓ Shutdown Management
✓ Recovery Coordination
✓ Health Supervision
✓ Runtime State Management
CoreEngine bajarmaydi.
✗ Market Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Module Boundary
GoldBot
↓
CoreEngine
↓
Pipeline
↓
Boundary End
---
# Input Contract
• Startup Request
• Shutdown Request
• Restart Request
• Runtime Event
• Recovery Event
• Health Event
---
# Output Contract
• Runtime Command
• Layer Command
• Startup Event
• Shutdown Event
• Recovery Event
---
# Allowed Dependencies
✓ Pipeline
✓ ServiceRegistry
✓ Configuration
✓ HealthMonitor
✓ Startup
✓ Shutdown
---
# Forbidden Dependencies
✗ Data Layer internals
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
• Running
• Recovering
• Stopping
• Stopped
• Failed
---
# Runtime Contract
1. CoreEngine GoldBot ichidagi yagona Runtime Engine hisoblanadi.
2. Barcha Layer'lar CoreEngine orqali boshqariladi.
3. Runtime State doim yangilanadi.
4. Startup va Shutdown markazlashgan boshqariladi.
5. Recovery avtomatik qo'llab-quvvatlanadi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
CoreEngine:
✓ Runtime boshqaradi.
✓ Layer'larni koordinatsiya qiladi.
✓ Recovery boshqaradi.
✓ Health kuzatadi.
CoreEngine:
✗ Trading Logic bajarmaydi.
✗ Signal yaratmaydi.
✗ Qaror chiqarmaydi.
✗ AI hisob-kitoblarini bajarmaydi.
---
# Acceptance Criteria
✓ Runtime ishga tushadi.
✓ Layer Initialization ishlaydi.
✓ Recovery ishlaydi.
✓ Shutdown xavfsiz bajariladi.
✓ Runtime State boshqariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
CoreEngine Contract GoldBot Runtime Engine'ning rasmiy arxitektura shartnomasi hisoblanadi.
CoreEngine GoldBot'ning barcha qatlamlari va servislarini boshqaruvchi yagona Canonical Runtime Engine hisoblanadi.
