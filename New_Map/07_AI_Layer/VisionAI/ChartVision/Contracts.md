# Chart Vision Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ChartVision modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ChartVision quyidagilar uchun javobgar.
✓ Chart Detection
✓ Symbol Detection
✓ Timeframe Detection
✓ Price Extraction
✓ Indicator Detection
✓ Drawing Detection
✓ Structure Analysis
✓ Chart Context Generation
ChartVision bajarmaydi.
✗ OCR
✗ General Image Analysis
✗ Signal Generation
✗ Decision Making
✗ Trade Execution
✗ Learning
---
# Module Boundary
```text
Chart Image
↓
ChartVision
↓
VisionAI
↓
InteractionManager
```
---
# Input Contract
• Trading Chart
• Screenshot
• User Context
---
# Output Contract
• Chart Context
• Symbol
• Timeframe
• Price Information
• Indicators
• Drawings
• Chart Metadata
---
# Allowed Dependencies
✓ VisionAI
✓ InteractionManager
---
# Forbidden Dependencies
✗ OCR
✗ PatternRecognition
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Chart turi aniqlanishi shart.
2. Symbol aniqlanishi shart.
3. Timeframe aniqlanishi shart.
4. Narx ma'lumotlari ajratilishi shart.
5. Indicator va Drawing mavjud bo'lsa aniqlanishi kerak.
6. Chart Context yaratilishi shart.
7. ChartVision Signal yoki Decision yaratmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Chart aniqlanadi.
✓ Symbol aniqlanadi.
✓ Timeframe aniqlanadi.
✓ Price ma'lumotlari olinadi.
✓ Indicator va Drawing aniqlanadi.
✓ Chart Context yaratiladi.
✓ VisionAI'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ChartVision Contract GoldBot VisionAI ichidagi trading chartlarni tahlil qilish, ularning asosiy elementlarini aniqlash va AI uchun standart Chart Context yaratishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
