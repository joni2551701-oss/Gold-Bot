# Chart Vision
Status: CANONICAL
---
# Purpose
ChartVision GoldBot VisionAI ichidagi Canonical Trading Chart Analysis moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchi yuborgan trading chartlarni tahlil qilish va AI uchun standart Vision Context yaratishdir.
ChartVision chartni o'qiydi.
ChartVision Signal yaratmaydi.
ChartVision Trade ochmaydi.
ChartVision Decision qabul qilmaydi.
---
# Objective
ChartVision quyidagi vazifalarni bajaradi.
• Chart Detection
• Timeframe Detection
• Symbol Detection
• Price Extraction
• Indicator Detection
• Drawing Detection
• Structure Recognition
• Vision Context Generation
---
# Layer Position
```text
Chart Image
↓
ChartVision
↓
VisionAI
↓
InteractionManager
↓
PersonalAI
```
---
# Responsibilities
ChartVision
✓ Trading chartni aniqlaydi
✓ Symbol aniqlaydi
✓ Timeframe aniqlaydi
✓ Candlesticklarni o'qiydi
✓ Indicatorlarni aniqlaydi
✓ Drawing Toollarni aniqlaydi
✓ Vision Context yaratadi
---
# Not Responsible
ChartVision
✗ OCR
✗ General Image Analysis
✗ Pattern Decision
✗ Signal Generation
✗ Trade Execution
✗ Learning
---
# Input
ChartVision qabul qiladi.
• Trading Chart
• Screenshot
• User Context
---
# Output
ChartVision yaratadi.
• Chart Context
• Symbol
• Timeframe
• Price Data
• Detected Indicators
• Detected Drawings
• Chart Metadata
---
# Workflow
```text
Receive Chart
↓
Detect Chart
↓
Extract Information
↓
Recognize Structure
↓
Generate Chart Context
↓
VisionAI
```
---
# Golden Rules
1. Chart o'zgartirilmaydi.
2. Faqat vizual ma'lumot olinadi.
3. Signal yaratilmaydi.
4. Decision qabul qilinmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ChartVision/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ChartVision GoldBot VisionAI ichidagi trading chartlarni o'qish va AI uchun standart Chart Context yaratishga javob beruvchi Canonical modul hisoblanadi.
