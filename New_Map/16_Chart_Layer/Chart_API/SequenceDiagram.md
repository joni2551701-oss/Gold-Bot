# Chart API Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_API Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart_API modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Chart_API Configuration
↓
Register Chart_API with Chart_Core
↓
Chart_API Ready
```
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
# Error Sequence
```text
Chart_API Error Detected
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
Reload Chart_API Configuration
↓
Re-Register with Chart_Core
↓
Chart_API Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Chart_API State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. GoldBot Core natijasi mavjud bo'lishi shart.
2. Chart_API faqat o'z mas'uliyat doirasida ishlaydi.
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
GoldBot Core
↓
Chart_API
↓
Chart_Core
