# Pattern Recognition Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PatternRecognition ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VisionAI
↓
PatternRecognition
↓
InteractionManager
```
---
# Module Architecture
```text
PatternRecognition
        │
        ├── Image Preprocessor
        ├── Candlestick Detector
        ├── Chart Pattern Detector
        ├── Structure Detector
        ├── Shape Detector
        ├── Confidence Evaluator
        └── Pattern Context Builder
```
---
# Internal Components
## Image Preprocessor
Tasvirni Pattern Detection uchun tayyorlaydi.
---
## Candlestick Detector
Candlestick Patternlarni aniqlaydi.
---
## Chart Pattern Detector
Triangle, Flag, Wedge, Head & Shoulders va boshqa Chart Patternlarni aniqlaydi.
---
## Structure Detector
Vizual Market Structure elementlarini aniqlaydi.
---
## Shape Detector
Grafik obyektlar va geometrik shakllarni aniqlaydi.
---
## Confidence Evaluator
Pattern ishonchlilik darajasini hisoblaydi.
---
## Pattern Context Builder
AI uchun Pattern Context yaratadi.
---
# Allowed Dependencies
✓ VisionAI
✓ InteractionManager
---
# Forbidden Dependencies
✗ OCR
✗ ChartVision
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
PatternRecognition VisionAI ichidagi barcha Visual Pattern Detection jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
