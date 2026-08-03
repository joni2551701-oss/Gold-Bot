# Templates Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Templates Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Templates modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Chart_API
↓
Templates
↓
Process Workspace Management
↓
Chart_Core
```
---
# Runtime Rules
1. Chart_API natijasi mavjud bo'lishi shart.
2. Templates faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Chart_Core'ga uzatiladi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Processing
↓
Completed
```
---
# Summary
Chart_API
↓
Templates
↓
Chart_Core
