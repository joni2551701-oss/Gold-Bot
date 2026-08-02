# IndicatorEngine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
IndicatorEngine Indicator Layer ichidagi barcha indikator modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
---
# Module Responsibility
IndicatorEngine quyidagilar uchun javobgar.
✓ Pipeline Management
✓ Module Orchestration
✓ Dependency Resolution
✓ Runtime State Management
✓ Validation Trigger
✓ Result Handoff to IndicatorService
✓ Runtime Event Generation
IndicatorEngine bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Market Context
↓
IndicatorEngine
↓
Indicator Modules
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• Runtime Configuration
• Indicator Settings
---
# Output Contract
• Execution Order
• Indicator Results
• Runtime Metadata
• Execution Events
---
# Allowed Dependencies
✓ Context Layer
✓ Event System
✓ Indicator Modules
✓ IndicatorService
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Resolving Dependencies
• Executing
• Validating
• Publishing
• Completed
• Failed
---
# Runtime Contract
1. Market Context mavjud bo'lishi shart.
2. Dependency Resolution bajarilishi majburiy.
3. Indicator modullari belgilangan tartibda ishga tushiriladi.
4. Validation Publish'dan oldin bajariladi.
5. IndicatorEngine formulalarni hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
IndicatorEngine:
✓ Pipeline boshqaradi.
✓ Execution boshqaradi.
✓ Validation boshlaydi.
✓ Runtime State yaratadi.
✓ IndicatorService'ga natijalarni uzatadi.
IndicatorEngine:
✗ Indicator hisoblamaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Pipeline muvaffaqiyatli ishga tushadi.
✓ Barcha Indicator modullari bajariladi.
✓ Validation muvaffaqiyatli yakunlanadi.
✓ Natijalar IndicatorService'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
IndicatorEngine Contract Indicator Layer ichidagi barcha indikator modullarining ishlashini boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
