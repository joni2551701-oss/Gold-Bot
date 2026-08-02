# Vision AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VisionAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
VisionAI quyidagilar uchun javobgar.
✓ Image Analysis
✓ Chart Analysis
✓ OCR
✓ Pattern Recognition
✓ Vision Context Generation
✓ Image Metadata
VisionAI bajarmaydi.
✗ Signal Generation
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
✗ Learning
✗ AI Analysis
---
# Module Boundary
```text
Image
↓
VisionAI
↓
InteractionManager
↓
PersonalAI
```
---
# Input Contract
• Image
• Screenshot
• Chart
• Camera Frame
---
# Output Contract
• Vision Context
• OCR Result
• Pattern Result
• Image Metadata
---
# Allowed Dependencies
✓ InteractionManager
✓ PersonalAI
---
# Forbidden Dependencies
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Image Type avtomatik aniqlanishi shart.
2. Tegishli Vision Module tanlanishi shart.
3. Vision Context yaratilishi shart.
4. Image o'zgartirilmaydi.
5. VisionAI Signal yaratmaydi.
6. VisionAI Decision qabul qilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Image qabul qilinadi.
✓ Image Type aniqlanadi.
✓ Vision Analysis bajariladi.
✓ Vision Context yaratiladi.
✓ InteractionManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VisionAI Contract GoldBot AI ichidagi barcha Computer Vision jarayonlarini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
