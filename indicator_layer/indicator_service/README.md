# Indicator Service
Status: CANONICAL
---
# Purpose
IndicatorService Indicator Layer ichidagi barcha indikator modullarining natijalarini birlashtiruvchi yagona Canonical Service hisoblanadi.
Uning asosiy vazifasi barcha Indicator modullaridan olingan natijalarni yagona Indicator Context obyektiga aylantirish va Strategy Layer uchun taqdim etishdir.
IndicatorService indikatorlarni hisoblamaydi.
IndicatorService signal yaratmaydi.
IndicatorService AI ishlatmaydi.
IndicatorService faqat Indicator Aggregation bajaradi.
---
# Objective
IndicatorService quyidagi vazifalarni bajaradi:
• Indicator Aggregation
• Indicator Validation
• Indicator Normalization
• Indicator Versioning
• Indicator State Management
• Indicator Publishing
• Indicator Lifecycle Management
• Indicator Context Generation
---
# Layer Position
```text
IndicatorEngine
↓
TrendIndicators
MomentumIndicators
VolatilityIndicators
VolumeIndicators
MarketStructureIndicators
SmartMoneyIndicators
CustomIndicators
↓
IndicatorService
↓
Strategy Layer
```
---
# Responsibilities
IndicatorService:
✓ Indicator natijalarini birlashtiradi
✓ Indicator Context yaratadi
✓ Indicator Validation bajaradi
✓ Indicator Version yaratadi
✓ Indicator State boshqaradi
✓ Indicator Context publish qiladi
---
# Not Responsible
IndicatorService:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
IndicatorService qabul qiladi:
• Trend Indicator State
• Momentum Indicator State
• Volatility Indicator State
• Volume Indicator State
• Market Structure Indicator State
• Smart Money Indicator State
• Custom Indicator State
---
# Output
IndicatorService yaratadi:
• Indicator Context
• Indicator Metadata
• Indicator Version
• Indicator Status
---
# Workflow
```text
Indicator Modules
↓
Aggregate Indicators
↓
Validate Indicator Context
↓
Normalize
↓
Build Indicator Context
↓
Publish
↓
Strategy Layer
```
---
# Golden Rules
1. IndicatorService yagona Indicator Context yaratadi.
2. Indicator natijalari o'zgartirilmaydi.
3. Validation majburiy.
4. Indicator Context immutable hisoblanadi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
IndicatorService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
IndicatorService GoldBot Indicator Layer ichidagi barcha indikator natijalarini yagona Indicator Context obyektiga birlashtiruvchi Canonical Service hisoblanadi.
