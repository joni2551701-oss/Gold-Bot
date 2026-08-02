# Market Repository
Status: CANONICAL
---
# Purpose
MarketRepository GoldBot Database Layer ichidagi Canonical Market Data Persistence moduli hisoblanadi.
Uning asosiy vazifasi Market Data, Candle, Tick, Indicator, Context va Signal History ma'lumotlarini Database'da saqlash, yangilash va o'qishdir.
MarketRepository Business Logic bajarmaydi.
MarketRepository Signal yaratmaydi.
MarketRepository faqat Market Domain ma'lumotlari bilan ishlaydi.
---
# Objective
MarketRepository quyidagi vazifalarni bajaradi.
• Market Data Storage
• Candle Storage
• Tick Storage
• Indicator Storage
• Context Storage
• Signal History Storage
---
# Layer Position
```text
DatabaseManager
↓
MarketRepository
↓
Database Storage
```
---
# Responsibilities
MarketRepository
✓ Candle saqlaydi
✓ Tick saqlaydi
✓ Indicator saqlaydi
✓ Market Context saqlaydi
✓ Signal History saqlaydi
✓ Market Query bajaradi
---
# Not Responsible
MarketRepository
✗ Trading Decision
✗ Strategy Analysis
✗ AI Analysis
✗ Trade Storage
✗ User Storage
✗ Cache Management
---
# Input
MarketRepository qabul qiladi.
• Candle Record
• Tick Record
• Indicator Record
• Context Record
• Query Request
---
# Output
MarketRepository yaratadi.
• Market Result
• Historical Data
• Query Result
• Repository Metadata
---
# Workflow
```text
Receive Repository Request
↓
Validate Market Data
↓
Save / Update / Query
↓
Return Repository Result
```
---
# Golden Rules
1. Market Data vaqt bo'yicha tartiblangan bo'lishi shart.
2. Candle ma'lumotlari immutable saqlanadi.
3. Tick Data ketma-ketligi saqlanishi shart.
4. Signal History o'chirilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MarketRepository/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MarketRepository GoldBot Database Layer ichidagi Candle, Tick, Indicator, Context va Signal History ma'lumotlarini boshqaruvchi Canonical Repository moduli hisoblanadi.
