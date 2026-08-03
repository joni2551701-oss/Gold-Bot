# Plugins Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Plugins Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Plugins modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Chart_API
↓
Plugins
↓
Process Indicator Plugin Support
↓
Chart_Core
```
---
# Runtime Rules
1. Chart_API natijasi mavjud bo'lishi shart.
2. Plugins faqat o'z mas'uliyat doirasida ishlaydi.
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
Plugins
↓
Chart_Core
