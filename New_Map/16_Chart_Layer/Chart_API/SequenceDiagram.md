# Chart API Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_API Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart_API modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
GoldBot Core
↓
Chart_API
↓
Process Public API Exposure
↓
Chart_Core
```
---
# Runtime Rules
1. GoldBot Core natijasi mavjud bo'lishi shart.
2. Chart_API faqat o'z mas'uliyat doirasida ishlaydi.
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
GoldBot Core
↓
Chart_API
↓
Chart_Core
