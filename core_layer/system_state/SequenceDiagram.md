# System State Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SystemState Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Owner Command / Emergency
↓
SystemState
↓
Process Operating Mode Vocabulary
↓
Runtime Consumers
```
---
# Error Sequence
```text
SystemState Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Runtime Rules
1. Owner Command / Emergency natijasi mavjud bo'lishi shart.
2. SystemState faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Runtime Consumers'ga uzatiladi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
```text
Owner Command / Emergency
↓
SystemState
↓
Runtime Consumers
```
