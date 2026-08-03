# Data Feed
Status: CANONICAL
---
# Purpose
DataFeed GoldBot Backtesting Layer ichidagi Canonical Data Feed Abstraction moduli hisoblanadi.
Uning asosiy vazifasi "candle qayerdan keladi" degan savolni qolgan barcha mantiqdan ajratishdir.
DataFeed tufayli Strategy, Signal va Context Layer'lari o'zi Live yoki Replay rejimida ishlayotganini bilmaydi.
DataFeed hech qanday tahlil bajarmaydi.
---
# Objective
DataFeed quyidagi vazifalarni bajaradi.
• Data Source Abstraction
• Live / Replay Transparency
• Candle Delivery
• Uniform Feed Contract
---
# Layer Position
```text
BacktestEngine
↓
DataFeed
↓
ReplayEngine
```
---
# Responsibilities
DataFeed
✓ Candle manbasini yagona Contract ortiga yashiradi
✓ Replay va Live manbalar uchun bir xil interfeys taqdim etadi
✓ So'ralgan miqdordagi candle'ni qaytaradi
---
# Not Responsible
DataFeed
✗ Candle Storage
✗ Market Analysis
✗ Signal Generation
✗ Indicator Calculation
✗ Data Validation (01_Data_Layer vazifasi)
---
# Input
DataFeed qabul qiladi.
• Candle Request
• Feed Configuration
---
# Output
DataFeed yaratadi.
• Candle List
• Feed Status
• Feed Metadata
---
# Workflow
```text
BacktestEngine
↓
DataFeed
↓
ReplayEngine
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
DataFeed
├── FeedContract
├── ReplayDataFeed
└── LiveDataFeedAdapter
```
---
# Golden Rules
1. Candle iste'molchisi Live yoki Replay rejimini aniqlay olmasligi shart.
2. Hech qanday joyda 'if backtest ... else ...' shoxlanishi bo'lmaydi.
3. DataFeed candle mazmunini o'zgartirmaydi.
4. DataFeed tahlil bajarmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DataFeed/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
DataFeed candle manbasi bilan qolgan barcha mantiq o'rtasidagi yagona Canonical seam hisoblanadi.
