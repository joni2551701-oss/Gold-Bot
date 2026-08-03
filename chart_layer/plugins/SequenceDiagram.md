# Plugins Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Plugins Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Plugins modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Plugins Configuration
↓
Register Plugins with Chart_Core
↓
Plugins Ready
```
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
# Error Sequence
```text
Plugins Error Detected
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
Reload Plugins Configuration
↓
Re-Register with Chart_Core
↓
Plugins Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Plugins State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. Chart_API natijasi mavjud bo'lishi shart.
2. Plugins faqat o'z mas'uliyat doirasida ishlaydi.
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
Plugins
↓
Chart_Core
