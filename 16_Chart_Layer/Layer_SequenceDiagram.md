# Chart Layer Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart Layer uchun Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence — Execution Order (Render Loop, not token-passing)
```text
GoldBot Core
↓
Chart_API (Entry)
↓
Chart_Core
↓
Chart_Data · Chart_Interaction · Objects        (parallel)
↓
Shared Render State
↓
Drawing_Tools · Indicators · Analysis_Overlay   (parallel)
↓
Chart_Renderer   (har frame Shared Render State'ni o'qib chizadi)
↓
Screenshot · Alerts                              (parallel)
↓
Chart_API (Exit)
↓
User
```
---
# Runtime Rules
1. Chart_API Chart Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
2. Chart_Core barcha ichki modullarni orkestratsiya qiladi.
3. Chart_Renderer ketma-ket modul Output'ini emas, har frame joriy Shared Render State'ni chizadi (Render Loop Rule).
4. Analysis_Overlay GoldBot Core natijalarini (Chart_API orqali) faqat vizualizatsiya qiladi.
5. Replay, Templates, Layout, Timeframe, Symbols, Theme, Settings, Plugins mustaqil parallel yordamchi modullar sifatida ishlaydi.
6. Yuqoridagi ketma-ketlik execution order — Input→Output ownership zanjiri emas (Chart Runtime Rule).
7. Circular Dependency qat'iyan taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Loading Data
↓
Rendering
↓
Interactive
↓
Updating
↓
Completed
```
---
# Summary
GoldBot Core
↓
Chart Layer
↓
User
