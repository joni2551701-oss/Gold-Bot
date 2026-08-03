# OCR Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat OCR Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Image
↓
OCR
↓
Detect Text Regions
↓
Recognize Characters
↓
Detect Language
↓
Extract Text
↓
Generate OCR Context
↓
VisionAI
```
---
# Runtime Rules
1. Image qabul qilinishi shart.
2. Text Region aniqlanishi shart.
3. Character Recognition bajarilishi shart.
4. OCR Context yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Detecting Text
↓
Recognizing
↓
Building Context
↓
Completed
or
Recognition Failed
```
---
# Summary
Image
↓
OCR
↓
OCR Context
↓
VisionAI
