# Indicator Engine
Status: CANONICAL
---
# Purpose
IndicatorEngine Indicator Layer ichidagi barcha indikator modullarini boshqaruvchi Canonical Orchestrator hisoblanadi.
Uning asosiy vazifasi Indicator Pipeline'ni boshqarish, indikatorlarni to'g'ri ketma-ketlikda ishga tushirish va IndicatorService uchun tayyor Indicator Context yaratishdir.
IndicatorEngine indikator formulalarini hisoblamaydi.
IndicatorEngine signal yaratmaydi.
IndicatorEngine AI ishlatmaydi.
IndicatorEngine faqat Indicator Pipeline'ni boshqaradi.
---
# Objective
IndicatorEngine quyidagi vazifalarni bajaradi:
• Indicator Pipeline Management
• Module Orchestration
• Execution Scheduling
• Dependency Resolution
• Indicator Validation Trigger
• Runtime State Management
• Error Handling
• Indicator Context Preparation
---
# Layer Position
```text
Market Context
↓
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
```
---
# Responsibilities
IndicatorEngine:
✓ Indicator Pipeline boshqaradi
✓ Module Execution boshqaradi
✓ Dependency tekshiradi
✓ Runtime State boshqaradi
✓ Validation boshlaydi
✓ IndicatorService'ga natijalarni uzatadi
---
# Not Responsible
IndicatorEngine:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
IndicatorEngine qabul qiladi:
• Market Context
• Runtime Configuration
• Indicator Settings
---
# Output
IndicatorEngine yaratadi:
• Indicator Execution Order
• Runtime Status
• Indicator Results
• Execution Events
---
# Workflow
```text
Market Context
↓
Load Configuration
↓
Resolve Dependencies
↓
Execute Indicator Modules
↓
Validate Results
↓
IndicatorService
↓
Indicator Context
```
---
# Golden Rules
1. IndicatorEngine faqat Pipeline boshqaradi.
2. Indicator hisoblash modullar ichida bajariladi.
3. Dependency tekshirilishi majburiy.
4. Validation IndicatorService'dan oldin bajariladi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
IndicatorEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
IndicatorEngine Indicator Layer ichidagi barcha indikator modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
