# Chart Vision Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ChartVision ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VisionAI
↓
ChartVision
↓
InteractionManager
```
---
# Module Architecture
```text
ChartVision
        │
        ├── Chart Detector
        ├── Symbol Detector
        ├── Timeframe Detector
        ├── Price Extractor
        ├── Indicator Detector
        ├── Drawing Detector
        ├── Structure Analyzer
        └── Chart Context Builder
```
---
# Internal Components
## Chart Detector
Trading chartni aniqlaydi.
---
## Symbol Detector
Instrumentni aniqlaydi.
---
## Timeframe Detector
Timeframe'ni aniqlaydi.
---
## Price Extractor
Narx va candlestick ma'lumotlarini ajratadi.
---
## Indicator Detector
Indicatorlarni aniqlaydi.
---
## Drawing Detector
Trendline, Rectangle, Fibonacci va boshqa chizmalarni aniqlaydi.
---
## Structure Analyzer
Chart strukturasini aniqlaydi.
---
## Chart Context Builder
AI uchun standart Chart Context yaratadi.
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
# Summary
ChartVision VisionAI ichidagi barcha Trading Chart Analysis jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
