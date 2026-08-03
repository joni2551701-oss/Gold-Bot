# Chart Vision Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ChartVision Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Chart Image
↓
ChartVision
↓
Detect Chart
↓
Detect Symbol
↓
Detect Timeframe
↓
Extract Price
↓
Detect Indicators
↓
Detect Drawings
↓
Generate Chart Context
↓
VisionAI
```
---
# Runtime Rules
1. Chart aniqlanishi shart.
2. Symbol aniqlanishi kerak.
3. Timeframe aniqlanishi kerak.
4. Chart Context yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Analyzing
↓
Extracting
↓
Generating Context
↓
Completed
or
Analysis Failed
```
---
# Summary
Chart Image
↓
ChartVision
↓
Chart Context
↓
VisionAI
