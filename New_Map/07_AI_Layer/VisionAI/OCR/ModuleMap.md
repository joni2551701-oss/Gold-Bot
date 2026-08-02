# OCR Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat OCR ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VisionAI
↓
OCR
↓
InteractionManager
```
---
# Module Architecture
```text
OCR
      │
      ├── Image Preprocessor
      ├── Text Region Detector
      ├── Character Recognizer
      ├── Language Detector
      ├── Layout Analyzer
      ├── OCR Context Builder
      └── Metadata Generator
```
---
# Internal Components
## Image Preprocessor
Tasvirni OCR uchun tayyorlaydi.
---
## Text Region Detector
Matn joylashgan hududlarni aniqlaydi.
---
## Character Recognizer
Belgilarni o'qiydi.
---
## Language Detector
Matn tilini aniqlaydi.
---
## Layout Analyzer
Sarlavha, jadval va bloklarni aniqlaydi.
---
## OCR Context Builder
AI uchun OCR Context yaratadi.
---
## Metadata Generator
OCR Metadata yaratadi.
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
# Summary
OCR VisionAI ichidagi barcha Text Recognition jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
