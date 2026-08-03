# Vision AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VisionAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
User
↓
VisionAI
↓
InteractionManager
↓
PersonalAI
```
---
# Module Architecture
```text
VisionAI
        │
        ├── ChartVision
        ├── OCR
        ├── PatternRecognition
        ├── ImageAnalysis
        ├── Vision Context Builder
        └── Image Preprocessor
```
---
# Internal Components
## ChartVision
Trading chartlarini tahlil qiladi.
---
## OCR
Rasmdagi matnni aniqlaydi.
---
## PatternRecognition
Vizual Patternlarni aniqlaydi.
---
## ImageAnalysis
Umumiy rasm tahlilini bajaradi.
---
## Vision Context Builder
AI uchun Vision Context yaratadi.
---
## Image Preprocessor
Tasvirni Vision modullariga tayyorlaydi.
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
# Summary
VisionAI GoldBot AI ichidagi barcha Vision Processing modullarini boshqaruvchi Canonical modul hisoblanadi.
