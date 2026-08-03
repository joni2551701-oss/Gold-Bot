# Chart Core Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Core Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart_Core modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Chart_Core Configuration
↓
Register Chart_Core with Chart_Core
↓
Chart_Core Ready
```
---
# Runtime Sequence
```text
Chart_API
↓
Chart_Core
↓
Process Chart Lifecycle Management
↓
Chart_Data
```
---
# Error Sequence
```text
Chart_Core Error Detected
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
Reload Chart_Core Configuration
↓
Re-Register with Chart_Core
↓
Chart_Core Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Chart_Core State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. Chart_API natijasi mavjud bo'lishi shart.
2. Chart_Core faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Chart_Data'ga uzatiladi.
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
Chart_Core
↓
Chart_Data
