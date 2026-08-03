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
```text
GoldBot Core
↓
Chart_API
↓
Chart_Core
```
---
# Responsibilities
Chart_API
✓ Tashqi so'rovlarni qabul qiladi
✓ GoldBot Core natijalarini (Market Context, Indicator Context, Signal, Decision, Trade) qabul qiladi
✓ Chart_Core'ga uzatadi
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
• Market Context
• Indicator Context
• Signal
• Decision
• Trade
• External API Request
---
# Output
Chart_API yaratadi.
• Chart Response
• Chart Event
• Plugin Context
• API Metadata
---
# Golden Rules
1. Chart_API faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Chart_API/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Chart_API GoldBot Chart Layer ichidagi Chart API vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
