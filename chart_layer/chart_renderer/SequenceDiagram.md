# Chart Renderer Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Renderer Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart_Renderer modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Chart_Core Boot
↓
Load Chart_Renderer Configuration
↓
Register Chart_Renderer with Chart_Core
↓
Chart_Renderer Ready
```
---
# Runtime Sequence
```text
Read Shared Render State (every frame)
↓
Chart_Renderer
↓
Process Canvas Rendering
↓
Screenshot / Alerts / Chart_API
```
---
# Error Sequence
```text
Chart_Renderer Error Detected
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
Reload Chart_Renderer Configuration
↓
Re-Register with Chart_Core
↓
Chart_Renderer Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Chart_Renderer State
↓
Unregister from Chart_Core
↓
Dispose
```
---
# Runtime Rules
1. Shared Render State mavjud bo'lishi shart (bo'sh bo'lsa ham, boshlang'ich holatda).
2. Chart_Renderer faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Screenshot/Alerts/Chart_API'ga uzatiladi.
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
Shared Render State
↓
Chart_Renderer
↓
Screenshot / Alerts / Chart_API
