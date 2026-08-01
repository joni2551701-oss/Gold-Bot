# IndicatorService Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorService modulining rasmiy Architecture Contract hujjati hisoblanadi.
IndicatorService Indicator Layer ichidagi barcha indikator modullarini yagona Indicator Context obyektiga birlashtiruvchi Canonical Service hisoblanadi.
---
# Module Responsibility
IndicatorService quyidagilar uchun javobgar.
✓ Indicator Aggregation
✓ Indicator Validation
✓ Indicator Normalization
✓ Indicator Version Management
✓ Indicator State Management
✓ Indicator Context Publishing
✓ Indicator Event Generation
IndicatorService bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Indicator Modules
↓
IndicatorService
↓
Strategy Layer
↓
Boundary End
---
# Input Contract
• Trend Indicator State
• Momentum Indicator State
• Volatility Indicator State
• Volume Indicator State
• Market Structure Indicator State
• Smart Money Indicator State
• Custom Indicator State
---
# Output Contract
• Indicator Context
• Indicator Version
• Indicator Metadata
• Indicator Status
---
# Allowed Dependencies
✓ IndicatorEngine
✓ TrendIndicators
✓ MomentumIndicators
✓ VolatilityIndicators
✓ VolumeIndicators
✓ MarketStructureIndicators
✓ SmartMoneyIndicators
✓ CustomIndicators
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer (calculation)
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
1. Barcha Indicator modullari natijasi qabul qilinishi shart.
2. Validation majburiy bosqich hisoblanadi.
3. Indicator Context yagona Canonical obyekt bo'lishi shart.
4. Har bir Indicator Context yangi Version olishi kerak.
5. Publish faqat muvaffaqiyatli Validation'dan keyin bajariladi.
6. Indicator Context immutable hisoblanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
IndicatorService:
✓ Indicator natijalarini birlashtiradi.
✓ Indicator Context yaratadi.
✓ Indicator Validation bajaradi.
✓ Indicator Version yaratadi.
✓ Indicator Context publish qiladi.
IndicatorService:
✗ Indicator hisoblamaydi.
✗ Strategy ishlatmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Barcha Indicator modullari agregatsiya qilinadi.
✓ Indicator Context yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ Indicator Version yaratiladi.
✓ Strategy Layer uchun tayyor Indicator Context uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
IndicatorService Contract GoldBot Indicator Layer ichidagi barcha indikator modullaridan olingan natijalarni yagona, versiyalangan va immutable **Indicator Context** obyektiga birlashtiruvchi rasmiy arxitektura shartnomasi hisoblanadi.
