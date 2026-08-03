# Volume Indicators
Status: CANONICAL
---
# Purpose
VolumeIndicators Indicator Layer ichidagi Volume Indicator'larni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozordagi hajm (Volume), kapital oqimi (Money Flow) va xaridor/sotuvchilar faolligini baholash hamda Volume Indicator State yaratishdir.
VolumeIndicators signal yaratmaydi.
VolumeIndicators trade ochmaydi.
VolumeIndicators AI ishlatmaydi.
VolumeIndicators faqat Volume Indicator'larni hisoblaydi.
---
# Objective
VolumeIndicators quyidagi vazifalarni bajaradi:
• VWAP Calculation
• VWMA Calculation
• OBV Calculation
• MFI Calculation
• CMF Calculation
• Accumulation/Distribution Line Calculation
• Volume Strength Calculation
• Volume Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
VolumeIndicators
↓
IndicatorService
```
---
# Responsibilities
VolumeIndicators:
✓ VWAP hisoblaydi
✓ VWMA hisoblaydi
✓ OBV hisoblaydi
✓ MFI hisoblaydi
✓ CMF hisoblaydi
✓ Accumulation/Distribution Line hisoblaydi
✓ Volume Strength yaratadi
✓ Volume Indicator State yaratadi
---
# Not Responsible
VolumeIndicators:
✗ Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
VolumeIndicators qabul qiladi:
• Market Context
• OHLC Data
• Volume Data
• Historical Data
---
# Output
VolumeIndicators yaratadi:
• VWAP
• VWMA
• OBV
• MFI
• CMF
• Accumulation/Distribution Line
• Volume Strength
• Volume Indicator State
---
# Workflow
```text
Market Context
↓
Load Price & Volume Data
↓
Calculate Volume Indicators
↓
Validate Indicators
↓
Generate Volume Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Volume Indicator'lar faqat Market Context asosida hisoblanadi.
2. Volume Data mavjud bo'lishi shart.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
VolumeIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
VolumeIndicators GoldBot Indicator Layer ichidagi barcha Volume Indicator'larni hisoblaydigan Canonical modul hisoblanadi.
