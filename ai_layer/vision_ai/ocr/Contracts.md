# OCR Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat OCR modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
OCR quyidagilar uchun javobgar.
✓ Text Detection
✓ Character Recognition
✓ Language Detection
✓ Layout Analysis
✓ OCR Context Generation
✓ OCR Metadata
OCR bajarmaydi.
✗ Chart Analysis
✗ Pattern Recognition
✗ Image Classification
✗ Signal Generation
✗ Decision Making
✗ Learning
---
# Module Boundary
```text
Image
↓
OCR
↓
VisionAI
↓
InteractionManager
```
---
# Input Contract
• Image
• Screenshot
• Chart
• Document
---
# Output Contract
• Extracted Text
• Text Blocks
• Detected Language
• OCR Context
• OCR Metadata
---
# Allowed Dependencies
✓ VisionAI
✓ InteractionManager
---
# Forbidden Dependencies
✗ ChartVision
✗ PatternRecognition
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Text Region aniqlanishi shart.
2. Character Recognition bajarilishi shart.
3. Language Detection qo'llab-quvvatlanishi shart.
4. OCR Context yaratilishi shart.
5. Image o'zgartirilmaydi.
6. OCR Signal yoki Decision yaratmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Image qabul qilinadi.
✓ Text aniqlanadi.
✓ Belgilar o'qiladi.
✓ Til aniqlanadi.
✓ OCR Context yaratiladi.
✓ VisionAI'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
OCR Contract GoldBot VisionAI ichidagi barcha Text Recognition jarayonlarini boshqarish, matnni standart formatga o'tkazish va AI uchun OCR Context yaratishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
