# Chart Layer Data Flow
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer ichidagi ma'lumot oqimini (Data Flow) tavsiflaydi.
Bu implementatsiya emas.
Bu Chart Layer uchun Canonical Data Flow hisoblanadi.
---
# Data Flow — Execution Order (NOT a token-passing chain)
Chart Shared State Rule: Chart modullari Chart State va Render State orqali muloqot qiladi. Quyidagi diagramma execution order'ni bildiradi — bironta modul yuqoridagi modulning Output'ini o'zining Input'i sifatida olmaydi (Chart_Renderer va undan keyingi modullar bundan mustasno emas: ular Shared Render State'ni o'qiydi, ketma-ket Output'ni emas).
```text
GoldBot Core
(Market Context, Indicator Context, Signal, Decision, Trade)
        │
        ▼
Chart_API (Entry)
        │
        ▼
Chart_Core
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
   Chart_Data     Chart_Interaction  Objects        (parallel)
        │              │              │
        └──────────────┴──────────────┘
                        │
                        ▼
              Shared Render State
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  Drawing_Tools    Indicators    Analysis_Overlay    (parallel)
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
                 Chart_Renderer            (har frame Shared Render State'ni o'qiydi)
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
   Screenshot                        Alerts          (parallel)
        │                               │
        └───────────────┬───────────────┘
                        ▼
                Chart_API (Exit)
                        │
                        ▼
                      User
```
---
# Supporting / Cross-Cutting Modules
```text
Chart_API
        │
        ├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼              ▼              ▼              ▼
   Replay         Templates        Layout        Timeframe        Symbols         Theme         Settings       Plugins
        │              │              │              │              │              │              │              │
        └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                                              │
                                              ▼
                                        Chart_Core / Chart_Data / Chart_Renderer
```
Replay, Templates, Layout, Timeframe, Symbols, Theme, Settings va Plugins bir-birining natijasiga bog'liq emas — mustaqil, parallel yordamchi modullar sifatida Chart_Core/Chart_Data/Chart_Renderer bilan ishlaydi.
---
# Input Sources
• GoldBot Core (Market Context, Indicator Context, Signal, Decision, Trade)
• Historical Candles (Data Layer'dan)
• User Interaction (Mouse, Keyboard, Touch)
• Plugin Requests
---
# Output
• Rendered Chart Frame
• Drawing Objects
• Overlay Visualization
• Alert Triggers
• Exported Files (PNG/JPG/PDF)
---
# Data Flow Rules
1. Chart faqat Data Layer'dan tarixiy ma'lumot va GoldBot Core'dan tahlil natijalarini oladi.
2. GoldBot Core natijalari faqat Chart_API orqali kiradi (Entry), va foydalanuvchiga faqat Chart_API orqali qaytadi (Exit).
3. Chart_Renderer hisob-kitob bajarmaydi, faqat Shared Render State'ni har frame chizadi.
4. Analysis_Overlay tahlil qilmaydi, faqat vizualizatsiya qiladi.
5. Yuqoridagi diagramma execution order — ownership yoki token-passing zanjiri emas (Chart Shared State Rule).
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
Chart Layer GoldBot arxitekturasidagi Canonical Visualization Data Flow hisoblanadi — GoldBot Core natijalarini Chart_API orqali qabul qilib, Chart_Renderer orqali foydalanuvchiga taqdim etadi.
