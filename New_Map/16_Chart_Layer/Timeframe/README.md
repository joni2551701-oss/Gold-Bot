# Timeframe
Status: BLUEPRINT
---
# Purpose
Timeframe GoldBot Chart Layer ichidagi Canonical Timeframe moduli hisoblanadi.
M1, M5, M15, H1, H4, D1, W1 kabi Timeframe'larni boshqaruvchi Canonical Timeframe moduli.
Timeframe Signal yaratmaydi.
Timeframe BOS/CHoCH hisoblamaydi.
Timeframe AI ishlatmaydi.
Timeframe Risk hisoblamaydi.
---
# Objective
Timeframe quyidagi vazifalarni bajaradi.
• Timeframe Management
• Timeframe Aggregation
• Custom Timeframe
• Timeframe Synchronization
---
# Layer Position
```text
Chart_API
↓
Timeframe
↓
Chart_Data
```
---
# Responsibilities
Timeframe
✓ Timeframe tanlovini boshqaradi
✓ Candle'larni tanlangan Timeframe'ga aggregatsiya qiladi
---
# Not Responsible
Timeframe
✗ Rendering
✗ Signal Generation
✗ Data Calculation (aggregation'dan boshqa)
✗ AI Analysis
---
# Input
Timeframe qabul qiladi.
• Timeframe Request
• Raw Candle Data
---
# Output
Timeframe yaratadi.
• Timeframe Context
• Aggregated Candles
---
# Golden Rules
1. Timeframe faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Timeframe/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Timeframe GoldBot Chart Layer ichidagi Timeframe vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
