# Templates Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Templates Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Templates modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Templates Configuration
↓
Register Templates with Chart_Core
↓
Templates Ready
```
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
# Error Sequence
```text
Templates Error Detected
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
Reload Templates Configuration
↓
Re-Register with Chart_Core
↓
Templates Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Templates State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. Chart_API natijasi mavjud bo'lishi shart.
2. Templates faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Chart_Core'ga uzatiladi.
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
Chart_API
↓
Templates
↓
Chart_Core
