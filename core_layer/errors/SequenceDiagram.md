# Errors Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Errors Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Barcha Layer'lar
↓
Errors
↓
Process Base Error Hierarchy
↓
Logger / Caller
```
---
# Error Sequence
```text
Errors Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Runtime Rules
1. Barcha Layer'lar natijasi mavjud bo'lishi shart.
2. Errors faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Logger / Caller'ga uzatiladi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
```text
Barcha Layer'lar
↓
Errors
↓
Logger / Caller
```
