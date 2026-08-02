# Image Analysis Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ImageAnalysis ichki arxitekturasini tavsiflaydi.
---
# Module Position
VisionAI
↓
ImageAnalysis
↓
InteractionManager
---
# Module Architecture
ImageAnalysis
│
├── Image Classifier
├── Object Detector
├── Scene Analyzer
├── Color Analyzer
├── Metadata Generator
└── Image Context Builder
---
# Internal Components
## Image Classifier
Rasm turini aniqlaydi.
---
## Object Detector
Rasmdagi obyektlarni aniqlaydi.
---
## Scene Analyzer
Sahna mazmunini tahlil qiladi.
---
## Color Analyzer
Asosiy ranglar va vizual xususiyatlarni aniqlaydi.
---
## Metadata Generator
Image Metadata yaratadi.
---
## Image Context Builder
AI uchun standart Image Context yaratadi.
---
# Allowed Dependencies
✓ VisionAI
✓ InteractionManager
---
# Forbidden Dependencies
✗ OCR
✗ ChartVision
✗ PatternRecognition
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
ImageAnalysis VisionAI ichidagi barcha umumiy Image Analysis jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
