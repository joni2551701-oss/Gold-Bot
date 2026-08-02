# ContextEngine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
ContextEngine Context Layer ichidagi barcha Context modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
---
# Module Responsibility
ContextEngine quyidagilar uchun javobgar.
✓ Context Orchestration
✓ Module Coordination
✓ Context Aggregation
✓ Context Validation
✓ Runtime State Management
✓ Context Event Generation
ContextEngine bajarmaydi.
✗ Yakuniy Market Context obyektini yaratish (ContextService vazifasi)
✗ Indicator Calculation
✗ Strategy Execution
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Market Data
↓
ContextEngine
↓
Context Modules
↓
ContextService
↓
Boundary End
---
# Input Contract
- Context Request
- Validated Market Data
- Market Events
- Runtime State
- Module Results
---
# Output Contract
- Context Analysis Results
- Context Status
- Context Events
- Runtime Context
- Validation Result
---
# Allowed Dependencies
✓ MarketStructure
✓ Liquidity
✓ OrderBlock
✓ FairValueGap
✓ Wyckoff
✓ AMD
✓ Session
✓ Trend
✓ VolumeProfile
✓ ContextService
✓ Event System
---
# Forbidden Dependencies
✗ Indicator Layer
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
- Initializing
- Running
- Aggregating
- Validating
- Completed
- Failed
---
# Runtime Contract
1. ContextEngine Context Layer ichidagi yagona Canonical Orchestrator hisoblanadi.
2. Har bir Context modul mustaqil bajarilishi shart.
3. ContextEngine faqat koordinatsiya qiladi.
4. Context Analysis Results barcha modullar tugagandan keyin ContextService'ga uzatiladi.
5. Validation majburiy bosqich hisoblanadi.
6. Indicator va Signal hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
ContextEngine:
✓ Context modullarini ishga tushiradi.
✓ Natijalarni yig'adi.
✓ Context Analysis Results'ni ContextService'ga uzatadi.
✓ Context State boshqaradi.
✓ Context Event yaratadi.
ContextEngine:
✗ Yakuniy Market Context obyektini yaratmaydi.
✗ Indicator hisoblamaydi.
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Context modullar koordinatsiya qilinadi.
✓ Context Analysis Results muvaffaqiyatli ContextService'ga uzatiladi.
✓ Validation ishlaydi.
✓ Runtime State boshqariladi.
✓ Context Events yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ContextEngine Contract GoldBot Context Layer markaziy Orchestrator komponentining rasmiy arxitektura shartnomasi hisoblanadi.
ContextEngine barcha Context modullarini yagona Canonical Runtime Pipeline orqali boshqaradi va Context Analysis Results'ni ContextService'ga uzatadi. Yakuniy Market Context obyektini faqat ContextService yaratadi.
