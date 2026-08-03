# Chart API
Status: BLUEPRINT
---
# Purpose
Chart_API GoldBot Chart Layer ichidagi Canonical Chart API moduli hisoblanadi.
Chart Layer uchun yagona Public API, Event API va Plugin API Boundary Gateway moduli.
Chart_API Signal yaratmaydi.
Chart_API BOS/CHoCH hisoblamaydi.
Chart_API AI ishlatmaydi.
Chart_API Risk hisoblamaydi.
---
# Objective
Chart_API quyidagi vazifalarni bajaradi.
• Public API Exposure
• Event API Management
• Plugin API Management
• Renderer API Exposure
• Data API Exposure
• Request Validation
---
# Layer Position
Chart_API Chart Layer'ning yagona **Entry va Exit** nuqtasi (majburiy — Chart Runtime Rule).
```text
Entry:  GoldBot Core ↓ Chart_API ↓ Chart_Core
Exit:   Chart_Renderer ↓ Screenshot / Alerts ↓ Chart_API ↓ User
```
---
# Responsibilities
Chart_API
✓ (Entry) Tashqi so'rovlarni qabul qiladi
✓ (Entry) GoldBot Core natijalarini (Market Context, Indicator Context, Signal, Decision, Trade) qabul qiladi va Chart_Core'ga uzatadi
✓ (Exit) Chart_Renderer/Screenshot/Alerts natijalarini yig'ib, foydalanuvchiga/tashqi tizimga qaytaradi
✓ Event'larni tashqi tinglovchilarga yuboradi
✓ Plugin'lar uchun API taqdim etadi
---
# Not Responsible
Chart_API
✗ Rendering
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Input
Chart_API qabul qiladi.
Entry tomondan:
• Market Context
• Indicator Context
• Signal
• Decision
• Trade
• External API Request
Exit tomondan:
• Rendered Frame (Chart_Renderer)
• Export File (Screenshot)
• Alert Trigger (Alerts)
---
# Output
Chart_API yaratadi.
Entry tomondan (Chart_Core'ga):
• Chart Request
• Chart Configuration
Exit tomondan (Userga):
• Chart Response
• Chart Event
• Plugin Context
• API Metadata
---
# Workflow
```text
Entry:  GoldBot Core ↓ Chart_API ↓ Chart_Core
Exit:   Chart_Renderer / Screenshot / Alerts ↓ Chart_API ↓ User
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Chart_API
├── PublicAPI/
├── EventAPI/
├── PluginAPI/
├── RendererAPI/
└── DataAPI/
```
---
# Golden Rules
1. Chart_API faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Chart_API/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Entry — Predecessor: GoldBot Core · Successor: Chart_Core
Exit — Predecessor: Chart_Renderer / Screenshot / Alerts · Successor: User
---
# Summary
Chart_API GoldBot Chart Layer ichidagi Chart API vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
