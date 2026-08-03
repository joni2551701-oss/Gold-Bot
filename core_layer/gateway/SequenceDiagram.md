# Gateway Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Gateway Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Platform Layer
↓
Gateway
↓
Process Service Registration va Discovery
↓
GoldBot Core Services
```
---
# Error Sequence
```text
Gateway Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Runtime Rules
1. Platform Layer natijasi mavjud bo'lishi shart.
2. Gateway faqat o'z mas'uliyat doirasida ishlaydi.
3. Output GoldBot Core Services'ga uzatiladi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
```text
Platform Layer
↓
Gateway
↓
GoldBot Core Services
```
