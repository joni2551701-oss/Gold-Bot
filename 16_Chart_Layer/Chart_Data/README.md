# Chart Data
Status: BLUEPRINT
---
# Purpose
Chart_Data GoldBot Chart Layer ichidagi Canonical Chart Data moduli hisoblanadi.
Candle, Tick, OHLCV, Session va Symbol ma'lumotlarini boshqaruvchi Canonical Chart Data Cache moduli.
Chart_Data Signal yaratmaydi.
Chart_Data BOS/CHoCH hisoblamaydi.
Chart_Data AI ishlatmaydi.
Chart_Data Risk hisoblamaydi.
---
# Objective
Chart_Data quyidagi vazifalarni bajaradi.
• Candle Data Management
• Tick Data Management
• OHLCV Aggregation
• Volume Data Management
• Session Data Management
• Symbol Data Cache
---
# Layer Position
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Responsibilities
Chart_Data
✓ Candle ma'lumotlarini saqlaydi
✓ Tick ma'lumotlarini saqlaydi
✓ OHLCV'ni birlashtiradi
✓ Session ma'lumotlarini boshqaradi
✓ Symbol Cache yaratadi
---
# Not Responsible
Chart_Data
✗ Rendering
✗ Indicator Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ Historical Data Fetching (GoldBot Core vazifasi)
---
# Input
Chart_Data qabul qiladi.
• Historical Candles (GoldBot Core'dan)
• Live Candle Stream
• Symbol Info
• Timeframe
---
# Output
Chart_Data yaratadi.
• Candle Data
• Tick Data
• OHLCV
• Session Data
• Symbol Cache
---
# Workflow
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Chart_Data
├── CandleData/
├── TickData/
├── OHLCV/
├── VolumeData/
├── SessionData/
├── SymbolData/
└── DataCache/
```
---
# Golden Rules
1. Chart_Data faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Chart_Data/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_Core · Successor: Chart_Renderer
---
# Summary
Chart_Data GoldBot Chart Layer ichidagi Chart Data vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
