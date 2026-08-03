# CoreService Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat CoreService modulining rasmiy Architecture Contract hujjati hisoblanadi.
CoreService GoldBot Core Layer ichidagi barcha Core Service va Runtime Coordination'ni boshqaruvchi yagona Canonical Service Orchestrator hisoblanadi.
---
# Module Responsibility
CoreService quyidagilar uchun javobgar.
✓ Core Module Coordination
✓ Runtime Command Routing
✓ Lifecycle Coordination
✓ Recovery Coordination
✓ Health Coordination
✓ Runtime State Management
✓ Service Event Coordination
CoreService bajarmaydi.
✗ Business Logic
✗ Market Analysis
✗ Strategy
✗ AI Analysis
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Module Boundary
CoreEngine
↓
CoreService
↓
Core Modules
↓
Boundary End
---
# Input Contract
• Runtime Command
• Startup Event
• Shutdown Event
• Recovery Event
• Health Event
• Service Request
---
# Output Contract
• Module Command
• Runtime Event
• Service Status
• Lifecycle Event
• Health Status
---
# Allowed Dependencies
✓ Pipeline
✓ Scheduler
✓ ServiceRegistry
✓ Configuration
✓ HealthMonitor
✓ Startup
✓ Shutdown
✓ Event System
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
1. CoreService GoldBot ichidagi yagona Canonical Core Service hisoblanadi.
2. Barcha Core Module'lar CoreService orqali koordinatsiya qilinadi.
3. Runtime Command Routing markazlashgan bajariladi.
4. Runtime State doimo yangilanadi.
5. Recovery va Health Coordination qo'llab-quvvatlanadi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
CoreService:
✓ Core Module'larni boshqaradi.
✓ Runtime Event'larni koordinatsiya qiladi.
✓ Lifecycle boshqaradi.
✓ Health holatini muvofiqlashtiradi.
CoreService:
✗ Trading Logic bajarmaydi.
✗ Signal yaratmaydi.
✗ Qaror chiqarmaydi.
✗ AI hisob-kitoblarini bajarmaydi.
---
# Acceptance Criteria
✓ Core Module Coordination ishlaydi.
✓ Runtime Command Routing ishlaydi.
✓ Recovery Coordination ishlaydi.
✓ Health Coordination ishlaydi.
✓ Runtime State boshqariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
CoreService Contract GoldBot Core Layer markaziy Service komponentining rasmiy arxitektura shartnomasi hisoblanadi.
CoreService GoldBot Core Layer ichidagi barcha modullarni yagona Runtime Service sifatida boshqaruvchi Canonical Service Orchestrator hisoblanadi.
