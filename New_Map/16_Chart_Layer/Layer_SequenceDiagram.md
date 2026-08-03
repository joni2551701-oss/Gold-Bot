# Chart Layer Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Chart Layer uchun Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
GoldBot Core
↓
Chart_API (Entry)
↓
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
↓
Objects
↓
Drawing_Tools
↓
Indicators
↓
Analysis_Overlay
↓
Alerts
↓
Screenshot
↓
Chart_API (Exit)
↓
User
```
---
# Runtime Rules
1. Chart_API Chart Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
2. Chart_Core barcha ichki modullarni orkestratsiya qiladi.
3. Chart_Renderer faqat oldingi bosqichlar tayyorlagan ma'lumotlarni chizadi.
4. Analysis_Overlay GoldBot Core natijalarini (Chart_API orqali) faqat vizualizatsiya qiladi.
5. Replay, Templates, Layout, Timeframe, Symbols, Theme, Settings, Plugins mustaqil parallel yordamchi modullar sifatida ishlaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
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
