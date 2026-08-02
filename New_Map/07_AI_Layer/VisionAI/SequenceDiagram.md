# Vision AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat VisionAI Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Image
↓
VisionAI
↓
Detect Image Type
↓
ChartVision / OCR /
PatternRecognition /
ImageAnalysis
↓
Generate Vision Context
↓
InteractionManager
↓
PersonalAI
```
---
# Runtime Rules
1. Image Type aniqlanishi shart.
2. Faqat kerakli Vision Module ishlaydi.
3. Vision Context yaratilishi shart.
4. InteractionManager'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving Image
↓
Analyzing
↓
Generating Context
↓
Completed
or
Analysis Failed
```
---
# Summary
Image
↓
VisionAI
↓
Vision Context
↓
PersonalAI
