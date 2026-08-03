# Screenshot Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Screenshot modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Alerts
↓
Screenshot
↓
Process PNG Export
↓
Chart_API
```
---
# Runtime Rules
1. Alerts natijasi mavjud bo'lishi shart.
2. Screenshot faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Chart_API'ga uzatiladi.
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
Alerts
↓
Screenshot
↓
Chart_API
