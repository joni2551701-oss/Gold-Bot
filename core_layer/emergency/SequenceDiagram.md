# Emergency Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Emergency Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Owner Command
↓
Emergency
↓
Process Emergency State Management (Pause / Kill / Maintenance / Resume)
↓
Pipeline / Runtime
```
---
# Error Sequence
```text
Emergency Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Runtime Rules
1. Owner Command natijasi mavjud bo'lishi shart.
2. Emergency faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Pipeline / Runtime'ga uzatiladi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
```text
Owner Command
↓
Emergency
↓
Pipeline / Runtime
```
