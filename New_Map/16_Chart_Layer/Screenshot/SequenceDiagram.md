# Screenshot Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Screenshot modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Screenshot Configuration
↓
Register Screenshot with Chart_Core
↓
Screenshot Ready
```
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
# Error Sequence
```text
Screenshot Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Recovery Sequence
```text
Safe State
↓
Reload Screenshot Configuration
↓
Re-Register with Chart_Core
↓
Screenshot Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Screenshot State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. Alerts natijasi mavjud bo'lishi shart.
2. Screenshot faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Chart_API'ga uzatiladi.
4. Xatolik yuz berganda Error Sequence ishga tushadi, keyin Recovery Sequence orqali tiklanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# State Machine
```text
Idle
↓
Initializing
↓
Ready
↓
Receiving
↓
Processing
↓
Completed
     │
     ├──→ Error ──→ Recovering ──→ Ready
     │
     └──→ Shutting Down ──→ Disposed
```
---
# Summary
Alerts
↓
Screenshot
↓
Chart_API
