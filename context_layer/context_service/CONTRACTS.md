# ContextService Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextService modulining rasmiy Architecture Contract hujjati hisoblanadi.
ContextService GoldBot Context Layer ichidagi barcha Context modullarini yagona Market Context obyektiga birlashtiruvchi Canonical Service hisoblanadi.
---
# Module Responsibility
ContextService quyidagilar uchun javobgar.
✓ Context Aggregation
✓ Context Validation
✓ Context Normalization
✓ Context Version Management
✓ Context State Management
✓ Market Context Publishing
✓ Context Event Generation
ContextService bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Context Modules
↓
ContextService
↓
Indicator Layer
↓
Boundary End
---
# Input Contract
• Market Structure State
• Liquidity State
• Order Block State
• Fair Value Gap State
• Wyckoff State
• AMD State
• Session State
• Trend State
• Volume Profile State
---
# Output Contract
• Market Context
• Context Version
• Context Metadata
• Context Status
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
✓ OrderBlock
✓ FairValueGap
✓ Wyckoff
✓ AMD
✓ Session
✓ Trend
✓ VolumeProfile
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Receiving
• Aggregating
• Validating
• Publishing
• Completed
• Failed
---
# Runtime Contract
1. Barcha Context modullar natijasi qabul qilinishi shart.
2. Validation majburiy bosqich hisoblanadi.
3. Market Context yagona Canonical obyekt bo'lishi shart.
4. Har bir Context yangi Version olishi kerak.
5. Publish faqat muvaffaqiyatli Validation'dan keyin bajariladi.
6. Context immutable hisoblanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
ContextService:
✓ Context natijalarini birlashtiradi.
✓ Market Context yaratadi.
✓ Context Validation bajaradi.
✓ Context Version yaratadi.
✓ Context Publish qiladi.
ContextService:
✗ Indicator hisoblamaydi.
✗ Strategy ishlatmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Barcha Context modullar agregatsiya qilinadi.
✓ Market Context yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ Context Version yaratiladi.
✓ Indicator Layer uchun tayyor Context uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ContextService Contract GoldBot Context Layer ichidagi barcha Context modullaridan olingan natijalarni yagona, versiyalangan va immutable **Market Context** obyektiga birlashtiruvchi rasmiy arxitektura shartnomasi hisoblanadi.
